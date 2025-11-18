package com.babykeke.backend.dto.response;

import lombok.Data;

import java.time.LocalDateTime;

/**
 * 家庭成员信息
 */
@Data
public class FamilyMemberDTO {

    private Integer id;
    private Integer userId;
    private String userNickname;
    private String relation;
    private String relationDisplay;
    private Integer isAdmin;
    private LocalDateTime createdAt;
}
