package com.babykeke.backend.entity;

import jakarta.persistence.*;
import lombok.Data;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.LocalDateTime;

/**
 * 排便/排尿记录实体(尿不湿记录)
 */
@Data
@Entity
@Table(name = "diaper_records", indexes = {
    @Index(name = "idx_baby_record_time", columnList = "baby_id,record_time")
})
public class DiaperRecord {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id", columnDefinition = "INT COMMENT '记录ID'")
    private Integer id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "baby_id", nullable = false, foreignKey = @ForeignKey(name = "fk_diaper_baby"))
    private Baby baby;

    @Column(name = "user_id", nullable = false, columnDefinition = "INT COMMENT '记录人ID'")
    private Integer userId;

    @Enumerated(EnumType.STRING)
    @Column(name = "diaper_type", nullable = false, columnDefinition = "ENUM('pee', 'poop', 'both') COMMENT '类型'")
    private DiaperType diaperType;

    @Enumerated(EnumType.STRING)
    @Column(name = "poop_amount", columnDefinition = "ENUM('少量', '适中', '大量') COMMENT '大便量'")
    private PoopAmount poopAmount;

    @Column(name = "poop_color", length = 20, columnDefinition = "VARCHAR(20) COMMENT '大便颜色'")
    private String poopColor;

    @Enumerated(EnumType.STRING)
    @Column(name = "poop_texture", columnDefinition = "ENUM('稀', '正常', '干燥') COMMENT '大便性状'")
    private PoopTexture poopTexture;

    @Column(name = "record_time", nullable = false, columnDefinition = "TIMESTAMP COMMENT '记录时间'")
    private LocalDateTime recordTime;

    @Column(name = "notes", columnDefinition = "TEXT COMMENT '备注'")
    private String notes;

    @CreationTimestamp
    @Column(name = "created_at", nullable = false, updatable = false, columnDefinition = "TIMESTAMP COMMENT '创建时间'")
    private LocalDateTime createdAt;

    @UpdateTimestamp
    @Column(name = "updated_at", nullable = false, columnDefinition = "TIMESTAMP COMMENT '更新时间'")
    private LocalDateTime updatedAt;
}
