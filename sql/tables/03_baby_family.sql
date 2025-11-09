-- ================================================
-- 宝宝-家庭成员关系表
-- ================================================

CREATE TABLE IF NOT EXISTS `baby_family` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `baby_id` INT(11) NOT NULL COMMENT '宝宝ID',
  `user_id` INT(11) NOT NULL COMMENT '用户ID',
  `relation` VARCHAR(20) DEFAULT NULL COMMENT '关系(爸爸/妈妈/爷爷/奶奶等)',
  `is_admin` TINYINT(1) NOT NULL DEFAULT 0 COMMENT '是否为管理员(0否1是)',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `idx_baby_user` (`baby_id`, `user_id`),
  KEY `idx_user_id` (`user_id`),
  CONSTRAINT `fk_baby_family_baby` FOREIGN KEY (`baby_id`) REFERENCES `babies` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_baby_family_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='宝宝-家庭成员关系表';
