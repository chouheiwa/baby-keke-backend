package com.babykeke.backend.entity;

import jakarta.persistence.*;
import lombok.Data;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.LocalDateTime;
import java.util.List;

/**
 * 用户实体 - 微信用户
 */
@Data
@Entity
@Table(name = "users")
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id", columnDefinition = "INT COMMENT '用户ID'")
    private Integer id;

    @Column(name = "openid", nullable = false, unique = true, length = 64, columnDefinition = "VARCHAR(64) COMMENT '微信OpenID'")
    private String openid;

    @Column(name = "nickname", length = 100, columnDefinition = "VARCHAR(100) COMMENT '用户昵称'")
    private String nickname;

    @Column(name = "phone", length = 20, columnDefinition = "VARCHAR(20) COMMENT '手机号'")
    private String phone;

    @CreationTimestamp
    @Column(name = "created_at", nullable = false, updatable = false, columnDefinition = "TIMESTAMP COMMENT '创建时间'")
    private LocalDateTime createdAt;

    @UpdateTimestamp
    @Column(name = "updated_at", nullable = false, columnDefinition = "TIMESTAMP COMMENT '更新时间'")
    private LocalDateTime updatedAt;

    @OneToMany(mappedBy = "user", cascade = CascadeType.ALL)
    private List<BabyFamily> babies;

    @OneToMany(mappedBy = "user", cascade = CascadeType.ALL)
    private List<UserSession> sessions;
}
