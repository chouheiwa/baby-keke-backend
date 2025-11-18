package com.babykeke.backend.dto.request;

import com.babykeke.backend.entity.BreastSide;
import com.babykeke.backend.entity.BottleContent;
import com.babykeke.backend.entity.FeedingType;
import jakarta.validation.constraints.NotNull;
import lombok.Data;

import java.time.LocalDateTime;

/**
 * 创建喂养记录请求
 */
@Data
public class CreateFeedingRecordRequest {

    @NotNull(message = "喂养类型不能为空")
    private FeedingType feedingType;

    // 母乳喂养字段
    private String feedingSequence;
    private BreastSide breastSide;

    // 奶粉/奶瓶喂养字段
    private Integer amount;
    private BottleContent bottleContent;

    // 辅食字段
    private String foodName;

    @NotNull(message = "开始时间不能为空")
    private LocalDateTime startTime;

    private LocalDateTime endTime;

    private String notes;
}
