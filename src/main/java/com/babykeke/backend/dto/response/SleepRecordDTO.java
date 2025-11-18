package com.babykeke.backend.dto.response;

import com.babykeke.backend.entity.SleepPosition;
import com.babykeke.backend.entity.SleepQuality;
import com.babykeke.backend.entity.SleepSource;
import com.babykeke.backend.entity.SleepStatus;
import lombok.Data;

import java.time.LocalDateTime;

@Data
public class SleepRecordDTO {
    private Integer id;
    private Integer babyId;
    private Integer userId;
    private SleepStatus status;
    private LocalDateTime startTime;
    private LocalDateTime endTime;
    private Integer duration;
    private SleepQuality quality;
    private SleepPosition position;
    private Integer wakeCount;
    private String notes;
    private LocalDateTime autoClosedAt;
    private SleepSource source;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
}
