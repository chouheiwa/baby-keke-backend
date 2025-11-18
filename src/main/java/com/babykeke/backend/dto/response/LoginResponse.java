package com.babykeke.backend.dto.response;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * 登录响应
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class LoginResponse {

    /**
     * 用户ID
     */
    private Integer userId;

    /**
     * 微信 OpenID
     */
    private String openid;

    /**
     * 是否新用户
     */
    private Boolean isNewUser;
}
