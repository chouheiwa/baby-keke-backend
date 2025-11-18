package com.babykeke.backend.dto.request;

import jakarta.validation.constraints.NotBlank;
import lombok.Data;

/**
 * 登录请求
 */
@Data
public class LoginRequest {

    /**
     * 微信小程序登录凭证 code
     */
    @NotBlank(message = "登录凭证不能为空")
    private String code;
}
