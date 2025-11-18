package com.babykeke.backend.dto.response;

import com.babykeke.backend.entity.Gender;
import lombok.Data;

import java.time.LocalDateTime;

/**
 * 宝宝信息响应
 */
@Data
public class BabyDTO {

    private Integer id;
    private String name;
    private String nickname;
    private Gender gender;
    private LocalDateTime birthday;
    private Integer birthWeight;
    private Integer birthHeight;
    private String notes;
    private Integer createdBy;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;

    /**
     * 当前用户在该宝宝家庭中的角色
     */
    private String relation;
    private String relationDisplay;
    private Integer isAdmin;
}
