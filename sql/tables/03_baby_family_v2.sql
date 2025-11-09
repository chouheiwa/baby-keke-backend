-- ================================================
-- 宝宝-家庭成员关系表（优化版）
-- ================================================

CREATE TABLE IF NOT EXISTS `baby_family` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `baby_id` INT(11) NOT NULL COMMENT '宝宝ID',
  `user_id` INT(11) NOT NULL COMMENT '用户ID',
  `relation` ENUM('mom', 'dad', 'grandpa_p', 'grandma_p', 'grandpa_m', 'grandma_m', 'other') DEFAULT NULL COMMENT '关系: mom-妈妈, dad-爸爸, grandpa_p-爷爷, grandma_p-奶奶, grandpa_m-外公, grandma_m-外婆, other-其他',
  `relation_display` VARCHAR(50) DEFAULT NULL COMMENT '角色显示名称（用于自定义角色或特殊称呼）',
  `is_admin` TINYINT(1) NOT NULL DEFAULT 0 COMMENT '是否为管理员(0否1是)',
  `joined_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '加入时间',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_baby_user` (`baby_id`, `user_id`) COMMENT '同一用户在同一家庭中只能有一个角色',
  KEY `idx_baby_relation` (`baby_id`, `relation`),
  KEY `idx_user_id` (`user_id`),
  CONSTRAINT `fk_baby_family_baby` FOREIGN KEY (`baby_id`) REFERENCES `babies` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_baby_family_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='宝宝-家庭成员关系表';

-- 角色唯一性约束说明：
-- 1. mom, dad, grandpa_p, grandma_p, grandpa_m, grandma_m 在同一家庭中只能有一个
-- 2. other 角色可以有多个，但需要设置不同的 relation_display
-- 3. 建议在应用层面实现角色唯一性检查
