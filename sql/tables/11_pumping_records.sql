-- ================================================
-- 吸奶记录表
-- ================================================

CREATE TABLE IF NOT EXISTS `pumping_records` (
  `id` INT(11) NOT NULL AUTO_INCREMENT COMMENT '记录ID',
  `baby_id` INT(11) NOT NULL COMMENT '宝宝ID',
  `user_id` INT(11) NOT NULL COMMENT '记录人ID',

  -- 吸奶量字段
  `left_amount` INT(11) DEFAULT NULL COMMENT '左侧吸奶量(ml)',
  `right_amount` INT(11) DEFAULT NULL COMMENT '右侧吸奶量(ml)',
  `total_amount` INT(11) NOT NULL COMMENT '总吸奶量(ml)',

  -- 时间和备注
  `record_time` TIMESTAMP NOT NULL COMMENT '记录时间',
  `notes` TEXT COMMENT '备注',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',

  PRIMARY KEY (`id`),
  KEY `idx_baby_record_time` (`baby_id`, `record_time`),
  KEY `idx_user_id` (`user_id`),
  CONSTRAINT `fk_pumping_baby` FOREIGN KEY (`baby_id`) REFERENCES `babies` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_pumping_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='吸奶记录表';
