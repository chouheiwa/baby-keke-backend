-- ================================================
-- 用户会话表
-- ================================================

CREATE TABLE IF NOT EXISTS `user_sessions` (
  `id` INT(11) NOT NULL AUTO_INCREMENT COMMENT '会话ID',
  `user_id` INT(11) NOT NULL COMMENT '用户ID',
  `openid` VARCHAR(64) NOT NULL COMMENT '微信OpenID',
  `session_key` VARCHAR(128) NOT NULL COMMENT '微信会话密钥',
  `unionid` VARCHAR(64) DEFAULT NULL COMMENT '微信UnionID',
  `expires_at` TIMESTAMP NOT NULL COMMENT '过期时间',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_openid` (`openid`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_expires_at` (`expires_at`),
  CONSTRAINT `fk_user_sessions_user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户会话表';

