-- ================================================
-- 家庭邀请表
-- ================================================

CREATE TABLE IF NOT EXISTS `invitations` (
  `id` INT(11) NOT NULL AUTO_INCREMENT COMMENT '邀请ID',
  `baby_id` INT(11) NOT NULL COMMENT '宝宝ID',
  `invite_code` VARCHAR(64) NOT NULL COMMENT '邀请码（加密字符串）',
  `created_by` INT(11) NOT NULL COMMENT '创建人用户ID',
  `expire_at` TIMESTAMP NOT NULL COMMENT '过期时间',
  `status` ENUM('active', 'expired', 'used') NOT NULL DEFAULT 'active' COMMENT '状态: active-有效, expired-已过期, used-已使用',
  `used_by` INT(11) DEFAULT NULL COMMENT '使用者用户ID',
  `used_at` TIMESTAMP NULL DEFAULT NULL COMMENT '使用时间',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_invite_code` (`invite_code`),
  KEY `idx_baby_id` (`baby_id`),
  KEY `idx_status_expire` (`status`, `expire_at`),
  KEY `idx_created_by` (`created_by`),
  CONSTRAINT `fk_invitation_baby` FOREIGN KEY (`baby_id`) REFERENCES `babies` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_invitation_creator` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`),
  CONSTRAINT `fk_invitation_user` FOREIGN KEY (`used_by`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='家庭邀请表';
