package com.babykeke.backend.entity;

import jakarta.persistence.*;
import lombok.Data;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.LocalDateTime;

/**
 * 用户会话实体 - 存储微信登录会话信息
 */
@Data
@Entity
@Table(name = "user_sessions")
public class UserSession {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id", columnDefinition = "INT COMMENT '会话ID'")
    private Integer id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false, foreignKey = @ForeignKey(name = "fk_user_session_user"))
    private User user;

    @Column(name = "openid", nullable = false, unique = true, length = 64, columnDefinition = "VARCHAR(64) COMMENT '微信OpenID'")
    private String openid;

    @Column(name = "session_key", nullable = false, length = 128, columnDefinition = "VARCHAR(128) COMMENT '微信会话密钥'")
    private String sessionKey;

    @Column(name = "unionid", length = 64, columnDefinition = "VARCHAR(64) COMMENT '微信UnionID'")
    private String unionid;

    @Column(name = "expires_at", nullable = false, columnDefinition = "TIMESTAMP COMMENT '过期时间'")
    private LocalDateTime expiresAt;

    @CreationTimestamp
    @Column(name = "created_at", nullable = false, updatable = false, columnDefinition = "TIMESTAMP COMMENT '创建时间'")
    private LocalDateTime createdAt;

    @UpdateTimestamp
    @Column(name = "updated_at", nullable = false, columnDefinition = "TIMESTAMP COMMENT '更新时间'")
    private LocalDateTime updatedAt;
}
