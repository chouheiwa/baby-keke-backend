package com.babykeke.backend.entity;

import jakarta.persistence.*;
import lombok.Data;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.LocalDateTime;

/**
 * 喂养记录实体
 */
@Data
@Entity
@Table(name = "feeding_records", indexes = {
    @Index(name = "idx_baby_time", columnList = "baby_id,start_time")
})
public class FeedingRecord {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id", columnDefinition = "INT COMMENT '记录ID'")
    private Integer id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "baby_id", nullable = false, foreignKey = @ForeignKey(name = "fk_feeding_baby"))
    private Baby baby;

    @Column(name = "user_id", nullable = false, columnDefinition = "INT COMMENT '记录人ID'")
    private Integer userId;

    @Enumerated(EnumType.STRING)
    @Column(name = "feeding_type", nullable = false, columnDefinition = "ENUM('breast', 'formula', 'solid') COMMENT '喂养类型'")
    private FeedingType feedingType;

    @Column(name = "feeding_sequence", columnDefinition = "TEXT COMMENT '喂养序列JSON(母乳交替记录)'")
    private String feedingSequence;

    @Enumerated(EnumType.STRING)
    @Column(name = "breast_side", columnDefinition = "ENUM('left', 'right', 'both', 'unknown') COMMENT '哺乳侧'")
    private BreastSide breastSide;

    @Column(name = "amount", columnDefinition = "INT COMMENT '奶量(ml)或食量(g)'")
    private Integer amount;

    @Enumerated(EnumType.STRING)
    @Column(name = "bottle_content", columnDefinition = "ENUM('breast', 'formula') COMMENT '奶瓶内容'")
    private BottleContent bottleContent;

    @Column(name = "food_name", length = 100, columnDefinition = "VARCHAR(100) COMMENT '食物名称'")
    private String foodName;

    @Column(name = "start_time", nullable = false, columnDefinition = "TIMESTAMP COMMENT '开始时间'")
    private LocalDateTime startTime;

    @Column(name = "end_time", columnDefinition = "TIMESTAMP COMMENT '结束时间'")
    private LocalDateTime endTime;

    @Column(name = "notes", columnDefinition = "TEXT COMMENT '备注'")
    private String notes;

    @CreationTimestamp
    @Column(name = "created_at", nullable = false, updatable = false, columnDefinition = "TIMESTAMP COMMENT '创建时间'")
    private LocalDateTime createdAt;

    @UpdateTimestamp
    @Column(name = "updated_at", nullable = false, columnDefinition = "TIMESTAMP COMMENT '更新时间'")
    private LocalDateTime updatedAt;
}
