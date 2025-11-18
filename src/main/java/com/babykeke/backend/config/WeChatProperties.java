package com.babykeke.backend.config;

import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Configuration;

/**
 * 微信小程序配置属性
 */
@Data
@Configuration
@ConfigurationProperties(prefix = "wechat")
public class WeChatProperties {

    /**
     * 微信小程序 AppID
     */
    private String appid;

    /**
     * 微信小程序 AppSecret
     */
    private String appsecret;

    /**
     * HTTP 请求是否验证证书
     */
    private boolean httpVerify = true;

    /**
     * CA证书路径
     */
    private String caBundlePath;
}
