package com.babykeke.backend.config;

import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Configuration;

/**
 * 应用配置属性
 */
@Data
@Configuration
@ConfigurationProperties(prefix = "app")
public class AppProperties {

    /**
     * 应用名称
     */
    private String name = "可可宝宝记";

    /**
     * 是否调试模式
     */
    private boolean debug = false;

    /**
     * 管理员令牌
     */
    private String adminToken;
}
