package com.babykeke.backend.dto.response;

import com.babykeke.backend.entity.DiaperType;
import com.babykeke.backend.entity.PoopAmount;
import com.babykeke.backend.entity.PoopTexture;
import lombok.Data;

import java.time.LocalDateTime;

@Data
public class DiaperRecordDTO {
    private Integer id;
    private Integer babyId;
    private Integer userId;
    private DiaperType diaperType;
    private PoopAmount poopAmount;
    private String poopColor;
    private PoopTexture poopTexture;
    private LocalDateTime recordTime;
    private String notes;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
}
