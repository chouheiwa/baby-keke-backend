package com.babykeke.backend.dto.request;

import lombok.Data;

/**
 * 更新用户信息请求
 */
@Data
public class UpdateUserRequest {
    private String nickname;
    private String phone;
}
