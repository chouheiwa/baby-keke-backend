package com.babykeke.backend.entity;

import jakarta.persistence.*;
import lombok.Data;
import org.hibernate.annotations.CreationTimestamp;

import java.time.LocalDateTime;

/**
 * 宝宝-家庭成员关系实体
 */
@Data
@Entity
@Table(name = "baby_family", indexes = {
    @Index(name = "idx_baby_user", columnList = "baby_id,user_id")
})
public class BabyFamily {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "baby_id", nullable = false, foreignKey = @ForeignKey(name = "fk_baby_family_baby"))
    private Baby baby;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false, foreignKey = @ForeignKey(name = "fk_baby_family_user"))
    private User user;

    @Column(name = "relation", length = 20, columnDefinition = "VARCHAR(20) COMMENT '关系(爸爸/妈妈/爷爷/奶奶等)'")
    private String relation;

    @Column(name = "relation_display", length = 50, columnDefinition = "VARCHAR(50) COMMENT '角色显示名称'")
    private String relationDisplay;

    @Column(name = "is_admin", columnDefinition = "INT DEFAULT 0 COMMENT '是否为管理员(0否1是)'")
    private Integer isAdmin = 0;

    @CreationTimestamp
    @Column(name = "created_at", nullable = false, updatable = false, columnDefinition = "TIMESTAMP COMMENT '创建时间'")
    private LocalDateTime createdAt;
}
