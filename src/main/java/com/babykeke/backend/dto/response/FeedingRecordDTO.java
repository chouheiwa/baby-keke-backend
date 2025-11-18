package com.babykeke.backend.dto.response;

import com.babykeke.backend.entity.BreastSide;
import com.babykeke.backend.entity.BottleContent;
import com.babykeke.backend.entity.FeedingType;
import lombok.Data;

import java.time.LocalDateTime;

/**
 * 喂养记录响应
 */
@Data
public class FeedingRecordDTO {

    private Integer id;
    private Integer babyId;
    private Integer userId;
    private FeedingType feedingType;
    private String feedingSequence;
    private BreastSide breastSide;
    private Integer amount;
    private BottleContent bottleContent;
    private String foodName;
    private LocalDateTime startTime;
    private LocalDateTime endTime;
    private String notes;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
}
