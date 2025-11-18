package com.babykeke.backend.dto.response;

import lombok.Data;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Data
public class GrowthRecordDTO {
    private Integer id;
    private Integer babyId;
    private Integer userId;
    private LocalDateTime recordDate;
    private BigDecimal weight;
    private BigDecimal height;
    private BigDecimal headCircumference;
    private String notes;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
}
