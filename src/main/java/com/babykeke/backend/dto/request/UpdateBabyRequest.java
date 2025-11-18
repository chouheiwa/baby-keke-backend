package com.babykeke.backend.dto.request;

import com.babykeke.backend.entity.Gender;
import lombok.Data;

import java.time.LocalDateTime;

/**
 * 更新宝宝请求
 */
@Data
public class UpdateBabyRequest {

    private String name;

    private String nickname;

    private Gender gender;

    private LocalDateTime birthday;

    private Integer birthWeight;

    private Integer birthHeight;

    private String notes;
}
