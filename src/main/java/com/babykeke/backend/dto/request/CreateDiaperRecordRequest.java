package com.babykeke.backend.dto.request;

import com.babykeke.backend.entity.DiaperType;
import com.babykeke.backend.entity.PoopAmount;
import com.babykeke.backend.entity.PoopTexture;
import jakarta.validation.constraints.NotNull;
import lombok.Data;

import java.time.LocalDateTime;

@Data
public class CreateDiaperRecordRequest {
    @NotNull(message = "类型不能为空")
    private DiaperType diaperType;
    private PoopAmount poopAmount;
    private String poopColor;
    private PoopTexture poopTexture;
    @NotNull(message = "记录时间不能为空")
    private LocalDateTime recordTime;
    private String notes;
}
