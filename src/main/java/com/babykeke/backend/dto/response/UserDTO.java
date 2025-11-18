package com.babykeke.backend.dto.response;

import lombok.Data;

import java.time.LocalDateTime;

/**
 * 用户信息响应
 */
@Data
public class UserDTO {
    private Integer id;
    private String openid;
    private String nickname;
    private String phone;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
}
