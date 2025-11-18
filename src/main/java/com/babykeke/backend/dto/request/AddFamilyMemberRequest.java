package com.babykeke.backend.dto.request;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.Data;

/**
 * 添加家庭成员请求
 */
@Data
public class AddFamilyMemberRequest {

    @NotNull(message = "用户ID不能为空")
    private Integer userId;

    @NotBlank(message = "关系不能为空")
    private String relation;

    private String relationDisplay;

    private Integer isAdmin = 0;
}
