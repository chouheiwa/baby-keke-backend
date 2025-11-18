package com.babykeke.backend;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;

/**
 * 可可宝宝记后端应用主启动类
 */
@SpringBootApplication
@EnableJpaRepositories
public class BabyKekeBackendApplication {

    public static void main(String[] args) {
        SpringApplication.run(BabyKekeBackendApplication.java, args);
    }
}
