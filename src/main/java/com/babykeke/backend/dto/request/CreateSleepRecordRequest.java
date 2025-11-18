package com.babykeke.backend.dto.request;

import com.babykeke.backend.entity.SleepPosition;
import com.babykeke.backend.entity.SleepQuality;
import com.babykeke.backend.entity.SleepStatus;
import jakarta.validation.constraints.NotNull;
import lombok.Data;

import java.time.LocalDateTime;

@Data
public class CreateSleepRecordRequest {
    private SleepStatus status = SleepStatus.completed;
    @NotNull(message = "开始时间不能为空")
    private LocalDateTime startTime;
    private LocalDateTime endTime;
    private Integer duration;
    private SleepQuality quality;
    private SleepPosition position;
    private Integer wakeCount = 0;
    private String notes;
}
