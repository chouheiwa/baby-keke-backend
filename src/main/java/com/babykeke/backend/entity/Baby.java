package com.babykeke.backend.entity;

import jakarta.persistence.*;
import lombok.Data;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.LocalDateTime;
import java.util.List;

/**
 * 宝宝信息实体
 */
@Data
@Entity
@Table(name = "babies")
public class Baby {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id", columnDefinition = "INT COMMENT '宝宝ID'")
    private Integer id;

    @Column(name = "name", nullable = false, length = 50, columnDefinition = "VARCHAR(50) COMMENT '宝宝姓名'")
    private String name;

    @Column(name = "nickname", length = 100, columnDefinition = "VARCHAR(100) COMMENT '宝宝昵称'")
    private String nickname;

    @Enumerated(EnumType.STRING)
    @Column(name = "gender", columnDefinition = "ENUM('male', 'female', 'unknown') DEFAULT 'unknown' COMMENT '性别'")
    private Gender gender = Gender.unknown;

    @Column(name = "birthday", nullable = false, columnDefinition = "TIMESTAMP COMMENT '出生日期'")
    private LocalDateTime birthday;

    @Column(name = "birth_weight", columnDefinition = "INT COMMENT '出生体重(g)'")
    private Integer birthWeight;

    @Column(name = "birth_height", columnDefinition = "INT COMMENT '出生身长(cm)'")
    private Integer birthHeight;

    @Column(name = "notes", columnDefinition = "TEXT COMMENT '备注'")
    private String notes;

    @Column(name = "created_by", nullable = false, columnDefinition = "INT COMMENT '创建人ID'")
    private Integer createdBy;

    @CreationTimestamp
    @Column(name = "created_at", nullable = false, updatable = false, columnDefinition = "TIMESTAMP COMMENT '创建时间'")
    private LocalDateTime createdAt;

    @UpdateTimestamp
    @Column(name = "updated_at", nullable = false, columnDefinition = "TIMESTAMP COMMENT '更新时间'")
    private LocalDateTime updatedAt;

    @OneToMany(mappedBy = "baby", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<BabyFamily> familyMembers;

    @OneToMany(mappedBy = "baby", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<FeedingRecord> feedingRecords;

    @OneToMany(mappedBy = "baby", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<DiaperRecord> diaperRecords;

    @OneToMany(mappedBy = "baby", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<SleepRecord> sleepRecords;

    @OneToMany(mappedBy = "baby", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<GrowthRecord> growthRecords;
}
