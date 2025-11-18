package com.babykeke.backend.dto.request;

import com.babykeke.backend.entity.Gender;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.Data;

import java.time.LocalDateTime;

/**
 * 创建宝宝请求
 */
@Data
public class CreateBabyRequest {

    @NotBlank(message = "宝宝姓名不能为空")
    private String name;

    private String nickname;

    private Gender gender = Gender.unknown;

    @NotNull(message = "出生日期不能为空")
    private LocalDateTime birthday;

    private Integer birthWeight;

    private Integer birthHeight;

    private String notes;

    /**
     * 创建人与宝宝的关系
     */
    private String relation;

    private String relationDisplay;
}
