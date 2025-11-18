package com.babykeke.backend.config;

import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.UrlBasedCorsConfigurationSource;
import org.springframework.web.filter.CorsFilter;

import java.util.Arrays;

/**
 * CORS 跨域配置
 */
@Data
@Configuration
@ConfigurationProperties(prefix = "cors")
public class CorsConfig {

    private String allowedOrigins = "*";
    private String allowedMethods = "*";
    private String allowedHeaders = "*";
    private boolean allowCredentials = true;
    private long maxAge = 3600;

    @Bean
    public CorsFilter corsFilter() {
        CorsConfiguration config = new CorsConfiguration();

        // 解析配置
        if ("*".equals(allowedOrigins)) {
            config.addAllowedOriginPattern("*");
        } else {
            Arrays.stream(allowedOrigins.split(","))
                    .map(String::trim)
                    .forEach(config::addAllowedOrigin);
        }

        if ("*".equals(allowedMethods)) {
            config.addAllowedMethod("*");
        } else {
            Arrays.stream(allowedMethods.split(","))
                    .map(String::trim)
                    .forEach(config::addAllowedMethod);
        }

        if ("*".equals(allowedHeaders)) {
            config.addAllowedHeader("*");
        } else {
            Arrays.stream(allowedHeaders.split(","))
                    .map(String::trim)
                    .forEach(config::addAllowedHeader);
        }

        config.setAllowCredentials(allowCredentials);
        config.setMaxAge(maxAge);

        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/**", config);

        return new CorsFilter(source);
    }
}
