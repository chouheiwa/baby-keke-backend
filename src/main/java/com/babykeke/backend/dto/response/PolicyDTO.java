package com.babykeke.backend.dto.response;

import com.babykeke.backend.entity.PolicyFormat;
import com.babykeke.backend.entity.PolicyStatus;
import com.babykeke.backend.entity.PolicyType;
import lombok.Data;

import java.time.LocalDateTime;

/**
 * 政策协议响应
 */
@Data
public class PolicyDTO {
    private Integer id;
    private PolicyType type;
    private String version;
    private String title;
    private String content;
    private PolicyFormat format;
    private String locale;
    private PolicyStatus status;
    private LocalDateTime effectiveAt;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
}
