package com.babykeke.backend.dto.request;

import lombok.Data;

/**
 * 创建邀请码请求
 */
@Data
public class CreateInvitationRequest {
    /**
     * 有效期（天数），默认7天
     */
    private Integer validDays = 7;
}
