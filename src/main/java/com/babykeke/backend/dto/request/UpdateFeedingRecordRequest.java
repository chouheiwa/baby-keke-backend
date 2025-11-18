package com.babykeke.backend.dto.request;

import com.babykeke.backend.entity.BreastSide;
import com.babykeke.backend.entity.BottleContent;
import com.babykeke.backend.entity.FeedingType;
import lombok.Data;

import java.time.LocalDateTime;

/**
 * 更新喂养记录请求
 */
@Data
public class UpdateFeedingRecordRequest {

    private FeedingType feedingType;
    private String feedingSequence;
    private BreastSide breastSide;
    private Integer amount;
    private BottleContent bottleContent;
    private String foodName;
    private LocalDateTime startTime;
    private LocalDateTime endTime;
    private String notes;
}
