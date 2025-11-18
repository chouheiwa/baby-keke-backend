package com.babykeke.backend.config;

import com.babykeke.backend.security.WeChatAuthInterceptor;
import lombok.RequiredArgsConstructor;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

/**
 * Web MVC 配置
 */
@Configuration
@RequiredArgsConstructor
public class WebConfig implements WebMvcConfigurer {

    private final WeChatAuthInterceptor weChatAuthInterceptor;

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(weChatAuthInterceptor)
                .addPathPatterns("/**")
                .excludePathPatterns(
                        "/auth/**",          // 认证相关接口不需要拦截
                        "/policies/**",      // 政策协议接口不需要拦截
                        "/actuator/**",      // 健康检查接口不需要拦截
                        "/error"             // 错误页面不需要拦截
                );
    }
}
