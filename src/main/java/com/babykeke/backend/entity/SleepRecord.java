package com.babykeke.backend.entity;

import jakarta.persistence.*;
import lombok.Data;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.LocalDateTime;

/**
 * 睡眠记录实体
 */
@Data
@Entity
@Table(name = "sleep_records", indexes = {
    @Index(name = "idx_baby_start_time", columnList = "baby_id,start_time")
})
public class SleepRecord {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id", columnDefinition = "INT COMMENT '记录ID'")
    private Integer id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "baby_id", nullable = false, foreignKey = @ForeignKey(name = "fk_sleep_baby"))
    private Baby baby;

    @Column(name = "user_id", nullable = false, columnDefinition = "INT COMMENT '记录人ID'")
    private Integer userId;

    @Enumerated(EnumType.STRING)
    @Column(name = "status", nullable = false, columnDefinition = "ENUM('in_progress', 'completed', 'auto_closed', 'cancelled') DEFAULT 'completed' COMMENT '记录状态'")
    private SleepStatus status = SleepStatus.completed;

    @Column(name = "start_time", nullable = false, columnDefinition = "DATETIME COMMENT '入睡时间'")
    private LocalDateTime startTime;

    @Column(name = "end_time", columnDefinition = "DATETIME COMMENT '醒来时间'")
    private LocalDateTime endTime;

    @Column(name = "duration", columnDefinition = "INT COMMENT '睡眠时长(分钟)'")
    private Integer duration;

    @Enumerated(EnumType.STRING)
    @Column(name = "quality", columnDefinition = "ENUM('good', 'normal', 'poor') COMMENT '睡眠质量'")
    private SleepQuality quality;

    @Enumerated(EnumType.STRING)
    @Column(name = "position", columnDefinition = "ENUM('left', 'middle', 'right') COMMENT '睡眠姿势'")
    private SleepPosition position;

    @Column(name = "wake_count", columnDefinition = "INT DEFAULT 0 COMMENT '夜醒次数'")
    private Integer wakeCount = 0;

    @Column(name = "notes", columnDefinition = "TEXT COMMENT '备注'")
    private String notes;

    @Column(name = "auto_closed_at", columnDefinition = "DATETIME COMMENT '自动关闭时间'")
    private LocalDateTime autoClosedAt;

    @Enumerated(EnumType.STRING)
    @Column(name = "source", nullable = false, columnDefinition = "ENUM('manual', 'auto') DEFAULT 'manual' COMMENT '记录来源'")
    private SleepSource source = SleepSource.manual;

    @CreationTimestamp
    @Column(name = "created_at", nullable = false, updatable = false, columnDefinition = "TIMESTAMP COMMENT '创建时间'")
    private LocalDateTime createdAt;

    @UpdateTimestamp
    @Column(name = "updated_at", nullable = false, columnDefinition = "TIMESTAMP COMMENT '更新时间'")
    private LocalDateTime updatedAt;
}
