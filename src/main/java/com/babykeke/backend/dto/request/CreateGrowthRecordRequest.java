package com.babykeke.backend.dto.request;

import jakarta.validation.constraints.NotNull;
import lombok.Data;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Data
public class CreateGrowthRecordRequest {
    @NotNull(message = "记录日期不能为空")
    private LocalDateTime recordDate;
    private BigDecimal weight;
    private BigDecimal height;
    private BigDecimal headCircumference;
    private String notes;
}
