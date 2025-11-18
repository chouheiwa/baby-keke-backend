package com.babykeke.backend.entity;

import jakarta.persistence.*;
import lombok.Data;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.LocalDateTime;

/**
 * 政策协议实体
 */
@Data
@Entity
@Table(name = "policies",
    uniqueConstraints = {
        @UniqueConstraint(name = "uq_policy_type_version_locale", columnNames = {"type", "version", "locale"})
    },
    indexes = {
        @Index(name = "idx_type", columnList = "type"),
        @Index(name = "idx_locale", columnList = "locale"),
        @Index(name = "idx_status", columnList = "status")
    }
)
public class Policy {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Enumerated(EnumType.STRING)
    @Column(name = "type", nullable = false, columnDefinition = "ENUM('terms', 'privacy')")
    private PolicyType type;

    @Column(name = "version", nullable = false, length = 32, columnDefinition = "VARCHAR(32)")
    private String version;

    @Column(name = "title", length = 200, columnDefinition = "VARCHAR(200)")
    private String title;

    @Column(name = "content", nullable = false, columnDefinition = "TEXT")
    private String content;

    @Enumerated(EnumType.STRING)
    @Column(name = "format", nullable = false, columnDefinition = "ENUM('markdown', 'html', 'text') DEFAULT 'markdown'")
    private PolicyFormat format = PolicyFormat.markdown;

    @Column(name = "locale", nullable = false, length = 16, columnDefinition = "VARCHAR(16) DEFAULT 'zh-CN'")
    private String locale = "zh-CN";

    @Enumerated(EnumType.STRING)
    @Column(name = "status", nullable = false, columnDefinition = "ENUM('draft', 'published', 'archived') DEFAULT 'draft'")
    private PolicyStatus status = PolicyStatus.draft;

    @Column(name = "effective_at", columnDefinition = "TIMESTAMP")
    private LocalDateTime effectiveAt;

    @CreationTimestamp
    @Column(name = "created_at", nullable = false, updatable = false, columnDefinition = "TIMESTAMP")
    private LocalDateTime createdAt;

    @UpdateTimestamp
    @Column(name = "updated_at", nullable = false, columnDefinition = "TIMESTAMP")
    private LocalDateTime updatedAt;
}
