package com.babykeke.backend.controller;

import com.babykeke.backend.dto.request.LoginRequest;
import com.babykeke.backend.dto.response.ApiResponse;
import com.babykeke.backend.dto.response.LoginResponse;
import com.babykeke.backend.service.AuthService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * 认证控制器
 */
@Slf4j
@RestController
@RequestMapping("/auth")
@RequiredArgsConstructor
public class AuthController {

    private final AuthService authService;

    /**
     * 微信小程序登录
     */
    @PostMapping("/login")
    public ApiResponse<LoginResponse> login(@Valid @RequestBody LoginRequest request) {
        log.info("收到登录请求");
        LoginResponse response = authService.login(request.getCode());
        return ApiResponse.success("登录成功", response);
    }
}
