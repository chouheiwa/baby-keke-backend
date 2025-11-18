package com.babykeke.backend.entity;

import jakarta.persistence.*;
import lombok.Data;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.LocalDateTime;

/**
 * 微信Access Token缓存实体
 */
@Data
@Entity
@Table(name = "wechat_access_tokens",
    uniqueConstraints = {
        @UniqueConstraint(name = "uk_wechat_appid", columnNames = {"appid"})
    }
)
public class WeChatAccessToken {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column(name = "appid", nullable = false, length = 64, columnDefinition = "VARCHAR(64)")
    private String appid;

    @Column(name = "token", nullable = false, length = 512, columnDefinition = "VARCHAR(512)")
    private String token;

    @Column(name = "expires_at", nullable = false, columnDefinition = "TIMESTAMP")
    private LocalDateTime expiresAt;

    @UpdateTimestamp
    @Column(name = "updated_at", nullable = false, columnDefinition = "TIMESTAMP")
    private LocalDateTime updatedAt;
}
