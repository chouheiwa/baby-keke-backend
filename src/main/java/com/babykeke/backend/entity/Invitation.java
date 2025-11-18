package com.babykeke.backend.entity;

import jakarta.persistence.*;
import lombok.Data;
import org.hibernate.annotations.CreationTimestamp;

import java.time.LocalDateTime;

/**
 * 邀请码实体
 */
@Data
@Entity
@Table(name = "invitations")
public class Invitation {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "baby_id", nullable = false, foreignKey = @ForeignKey(name = "fk_invitation_baby"))
    private Baby baby;

    @Column(name = "invite_code", nullable = false, unique = true, length = 64, columnDefinition = "VARCHAR(64)")
    private String inviteCode;

    @Column(name = "created_by", nullable = false, columnDefinition = "INT")
    private Integer createdBy;

    @Column(name = "expire_at", nullable = false, columnDefinition = "TIMESTAMP")
    private LocalDateTime expireAt;

    @Enumerated(EnumType.STRING)
    @Column(name = "status", nullable = false, columnDefinition = "ENUM('active', 'expired', 'used') DEFAULT 'active'")
    private InvitationStatus status = InvitationStatus.active;

    @Column(name = "used_by", columnDefinition = "INT")
    private Integer usedBy;

    @Column(name = "used_at", columnDefinition = "TIMESTAMP")
    private LocalDateTime usedAt;

    @CreationTimestamp
    @Column(name = "created_at", nullable = false, updatable = false, columnDefinition = "TIMESTAMP")
    private LocalDateTime createdAt;
}
