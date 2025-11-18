package com.babykeke.backend.entity;

import jakarta.persistence.*;
import lombok.Data;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.math.BigDecimal;
import java.time.LocalDateTime;

/**
 * 生长发育记录实体
 */
@Data
@Entity
@Table(name = "growth_records", indexes = {
    @Index(name = "idx_baby_record_date", columnList = "baby_id,record_date")
})
public class GrowthRecord {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id", columnDefinition = "INT COMMENT '记录ID'")
    private Integer id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "baby_id", nullable = false, foreignKey = @ForeignKey(name = "fk_growth_baby"))
    private Baby baby;

    @Column(name = "user_id", nullable = false, columnDefinition = "INT COMMENT '记录人ID'")
    private Integer userId;

    @Column(name = "record_date", nullable = false, columnDefinition = "TIMESTAMP COMMENT '记录日期'")
    private LocalDateTime recordDate;

    @Column(name = "weight", precision = 5, scale = 2, columnDefinition = "DECIMAL(5,2) COMMENT '体重(kg)'")
    private BigDecimal weight;

    @Column(name = "height", precision = 5, scale = 2, columnDefinition = "DECIMAL(5,2) COMMENT '身高/身长(cm)'")
    private BigDecimal height;

    @Column(name = "head_circumference", precision = 5, scale = 2, columnDefinition = "DECIMAL(5,2) COMMENT '头围(cm)'")
    private BigDecimal headCircumference;

    @Column(name = "notes", columnDefinition = "TEXT COMMENT '备注'")
    private String notes;

    @CreationTimestamp
    @Column(name = "created_at", nullable = false, updatable = false, columnDefinition = "TIMESTAMP COMMENT '创建时间'")
    private LocalDateTime createdAt;

    @UpdateTimestamp
    @Column(name = "updated_at", nullable = false, columnDefinition = "TIMESTAMP COMMENT '更新时间'")
    private LocalDateTime updatedAt;
}
