package com.babykeke.backend.util;

import com.babykeke.backend.config.WeChatProperties;
import com.babykeke.backend.entity.WeChatAccessToken;
import com.babykeke.backend.exception.WeChatApiException;
import com.babykeke.backend.repository.WeChatAccessTokenRepository;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.Map;

/**
 * 微信小程序 API 客户端
 */
@Slf4j
@Component
public class WeChatApiClient {

    private static final String BASE_URL = "https://api.weixin.qq.com";

    private final WebClient webClient;
    private final WeChatProperties weChatProperties;
    private final WeChatAccessTokenRepository tokenRepository;
    private final ObjectMapper objectMapper;

    public WeChatApiClient(WeChatProperties weChatProperties,
                          WeChatAccessTokenRepository tokenRepository,
                          ObjectMapper objectMapper) {
        this.weChatProperties = weChatProperties;
        this.tokenRepository = tokenRepository;
        this.objectMapper = objectMapper;
        this.webClient = WebClient.builder()
                .baseUrl(BASE_URL)
                .build();

        if (weChatProperties.getAppid() == null || weChatProperties.getAppid().isEmpty() ||
            weChatProperties.getAppsecret() == null || weChatProperties.getAppsecret().isEmpty()) {
            log.warn("微信小程序 AppID 或 AppSecret 未配置");
        }
    }

    /**
     * 登录凭证校验
     *
     * @param code 小程序登录时获取的 code
     * @return 包含 openid, session_key, unionid 的 Map
     */
    public Map<String, String> code2Session(String code) {
        log.info("WeChatAPI.code2session: request begin");

        String response = webClient.get()
                .uri(uriBuilder -> uriBuilder
                        .path("/sns/jscode2session")
                        .queryParam("appid", weChatProperties.getAppid())
                        .queryParam("secret", weChatProperties.getAppsecret())
                        .queryParam("js_code", code)
                        .queryParam("grant_type", "authorization_code")
                        .build())
                .retrieve()
                .bodyToMono(String.class)
                .block();

        try {
            JsonNode data = objectMapper.readTree(response);

            if (data.has("errcode") && data.get("errcode").asInt() != 0) {
                int errcode = data.get("errcode").asInt();
                String errmsg = data.has("errmsg") ? data.get("errmsg").asText() : "未知错误";
                log.error("WeChatAPI.code2session: error errcode={} errmsg={}", errcode, errmsg);
                throw new WeChatApiException(errcode, errmsg);
            }

            log.info("WeChatAPI.code2session: response received openid={}", data.get("openid").asText());

            Map<String, String> result = new HashMap<>();
            result.put("openid", data.get("openid").asText());
            result.put("session_key", data.get("session_key").asText());
            if (data.has("unionid")) {
                result.put("unionid", data.get("unionid").asText());
            }

            return result;
        } catch (Exception e) {
            log.error("WeChatAPI.code2session: parse response error", e);
            throw new WeChatApiException(-1, "解析微信响应失败: " + e.getMessage());
        }
    }

    /**
     * 获取接口调用凭证 access_token（数据库缓存）
     *
     * @return access_token
     */
    public String getAccessToken() {
        // 1. 读缓存
        try {
            var tokenOpt = tokenRepository.findByAppidAndExpiresAtAfter(
                    weChatProperties.getAppid(),
                    LocalDateTime.now()
            );
            if (tokenOpt.isPresent()) {
                return tokenOpt.get().getToken();
            }
        } catch (Exception e) {
            log.warn("读取 access_token 缓存失败", e);
        }

        // 2. 请求微信
        log.info("wechat.token: request begin appid={}", weChatProperties.getAppid());

        String response = webClient.get()
                .uri(uriBuilder -> uriBuilder
                        .path("/cgi-bin/token")
                        .queryParam("grant_type", "client_credential")
                        .queryParam("appid", weChatProperties.getAppid())
                        .queryParam("secret", weChatProperties.getAppsecret())
                        .build())
                .retrieve()
                .bodyToMono(String.class)
                .block();

        try {
            JsonNode data = objectMapper.readTree(response);

            if (data.has("errcode") && data.get("errcode").asInt() != 0) {
                int errcode = data.get("errcode").asInt();
                String errmsg = data.has("errmsg") ? data.get("errmsg").asText() : "未知错误";
                log.error("wechat.token: error errcode={} errmsg={}", errcode, errmsg);
                throw new WeChatApiException(errcode, errmsg);
            }

            String token = data.get("access_token").asText();
            int expiresIn = data.has("expires_in") ? data.get("expires_in").asInt() : 7200;
            LocalDateTime expireAt = LocalDateTime.now().plusSeconds(Math.max(expiresIn - 120, 300));

            log.info("wechat.token: response errcode=0 expires_in={}", expiresIn);

            // 3. 写缓存
            try {
                var tokenEntity = tokenRepository.findByAppid(weChatProperties.getAppid())
                        .orElse(new WeChatAccessToken());
                tokenEntity.setAppid(weChatProperties.getAppid());
                tokenEntity.setToken(token);
                tokenEntity.setExpiresAt(expireAt);
                tokenRepository.save(tokenEntity);
                log.info("wechat.token: cached to db successfully");
            } catch (Exception e) {
                log.warn("wechat.token: cache to db failed, continue without db cache", e);
            }

            return token;
        } catch (Exception e) {
            log.error("wechat.token: parse response error", e);
            throw new WeChatApiException(-1, "解析微信响应失败: " + e.getMessage());
        }
    }

    /**
     * 获取小程序码（无限制）
     *
     * @param scene 自定义场景值（不超过32个可见字符）
     * @param page  小程序页面路径
     * @param width 图片宽度，默认 430
     * @return PNG 二进制内容
     */
    public byte[] getWxacodeUnlimit(String scene, String page, int width) {
        String accessToken = getAccessToken();
        log.info("wechat.qrcode: request scene={} page={}", scene, page);

        Map<String, Object> payload = new HashMap<>();
        payload.put("scene", scene);
        payload.put("page", page);
        payload.put("width", width);
        payload.put("check_path", false);

        byte[] response = webClient.post()
                .uri("/wxa/getwxacodeunlimit?access_token=" + accessToken)
                .bodyValue(payload)
                .retrieve()
                .bodyToMono(byte[].class)
                .block();

        // 检查是否是图片（简单检查前几个字节是否是PNG标识）
        if (response != null && response.length > 4 &&
            response[0] == (byte) 0x89 && response[1] == 0x50 &&
            response[2] == 0x4E && response[3] == 0x47) {
            log.info("wechat.qrcode: success image returned");
            return response;
        }

        // 否则可能是错误响应
        try {
            JsonNode data = objectMapper.readTree(response);
            int errcode = data.has("errcode") ? data.get("errcode").asInt() : -1;
            String errmsg = data.has("errmsg") ? data.get("errmsg").asText() : "获取小程序码失败";
            log.error("wechat.qrcode: error errcode={} errmsg={}", errcode, errmsg);
            throw new WeChatApiException(errcode, errmsg);
        } catch (Exception e) {
            log.error("wechat.qrcode: parse error response failed", e);
            throw new WeChatApiException(-1, "获取小程序码失败");
        }
    }
}
