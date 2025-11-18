package com.babykeke.backend.config;

import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Contact;
import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.info.License;
import io.swagger.v3.oas.models.servers.Server;
import io.swagger.v3.oas.models.security.SecurityRequirement;
import io.swagger.v3.oas.models.security.SecurityScheme;
import io.swagger.v3.oas.models.Components;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.List;

/**
 * Swagger/OpenAPI 配置
 */
@Configuration
public class SwaggerConfig {

    @Bean
    public OpenAPI customOpenAPI() {
        return new OpenAPI()
                .info(new Info()
                        .title("可可宝宝记 API 文档")
                        .description("基于 Spring Boot + JPA 的宝宝成长记录后端服务")
                        .version("1.0.0")
                        .contact(new Contact()
                                .name("Baby Keke Team")
                                .email("support@babykeke.com"))
                        .license(new License()
                                .name("MIT License")
                                .url("https://opensource.org/licenses/MIT")))
                .servers(List.of(
                        new Server().url("http://localhost:8000").description("开发环境"),
                        new Server().url("https://api.babykeke.com").description("生产环境")))
                .components(new Components()
                        .addSecuritySchemes("X-Wx-Openid", new SecurityScheme()
                                .type(SecurityScheme.Type.APIKEY)
                                .in(SecurityScheme.In.HEADER)
                                .name("X-Wx-Openid")
                                .description("微信云托管自动注入的 OpenID")))
                .addSecurityItem(new SecurityRequirement().addList("X-Wx-Openid"));
    }
}
