package com.babykeke.backend.dto.request;

import jakarta.validation.constraints.NotBlank;
import lombok.Data;

/**
 * 加入家庭请求
 */
@Data
public class JoinFamilyRequest {
    @NotBlank(message = "邀请码不能为空")
    private String inviteCode;

    @NotBlank(message = "关系不能为空")
    private String relation;

    private String relationDisplay;
}
