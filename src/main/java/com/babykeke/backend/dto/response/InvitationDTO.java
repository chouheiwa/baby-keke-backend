package com.babykeke.backend.dto.response;

import com.babykeke.backend.entity.InvitationStatus;
import lombok.Data;

import java.time.LocalDateTime;

/**
 * 邀请码响应
 */
@Data
public class InvitationDTO {
    private Integer id;
    private Integer babyId;
    private String babyName;
    private String inviteCode;
    private Integer createdBy;
    private LocalDateTime expireAt;
    private InvitationStatus status;
    private Integer usedBy;
    private LocalDateTime usedAt;
    private LocalDateTime createdAt;
}
