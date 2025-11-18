package com.babykeke.backend.service;

import com.babykeke.backend.dto.response.LoginResponse;
import com.babykeke.backend.entity.User;
import com.babykeke.backend.entity.UserSession;
import com.babykeke.backend.repository.UserRepository;
import com.babykeke.backend.repository.UserSessionRepository;
import com.babykeke.backend.util.WeChatApiClient;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.Map;

/**
 * 认证服务
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class AuthService {

    private final WeChatApiClient weChatApiClient;
    private final UserRepository userRepository;
    private final UserSessionRepository sessionRepository;

    /**
     * 微信小程序登录
     *
     * @param code 微信登录凭证
     * @return 登录响应
     */
    @Transactional
    public LoginResponse login(String code) {
        // 1. 调用微信接口获取 openid 和 session_key
        Map<String, String> sessionData = weChatApiClient.code2Session(code);
        String openid = sessionData.get("openid");
        String sessionKey = sessionData.get("session_key");
        String unionid = sessionData.get("unionid");

        log.info("微信登录: openid={}", openid);

        // 2. 查询或创建用户
        User user = userRepository.findByOpenid(openid)
                .orElseGet(() -> createNewUser(openid));

        boolean isNewUser = user.getCreatedAt().isAfter(LocalDateTime.now().minusSeconds(5));

        // 3. 创建或更新会话
        UserSession session = sessionRepository.findByOpenid(openid)
                .orElseGet(UserSession::new);

        session.setUser(user);
        session.setOpenid(openid);
        session.setSessionKey(sessionKey);
        session.setUnionid(unionid);
        session.setExpiresAt(LocalDateTime.now().plusDays(30)); // 30天有效期

        sessionRepository.save(session);

        log.info("登录成功: userId={}, isNewUser={}", user.getId(), isNewUser);

        return new LoginResponse(user.getId(), openid, isNewUser);
    }

    /**
     * 创建新用户
     */
    private User createNewUser(String openid) {
        User user = new User();
        user.setOpenid(openid);
        user.setNickname("微信用户");
        return userRepository.save(user);
    }
}
