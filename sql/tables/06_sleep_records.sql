-- ================================================
-- 睡眠记录表
-- ================================================

CREATE TABLE IF NOT EXISTS `sleep_records` (
  `id` INT(11) NOT NULL AUTO_INCREMENT COMMENT '记录ID',
  `baby_id` INT(11) NOT NULL COMMENT '宝宝ID',
  `user_id` INT(11) NOT NULL COMMENT '记录人ID',
  `start_time` DATETIME NOT NULL COMMENT '入睡时间',
  `end_time` DATETIME NULL DEFAULT NULL COMMENT '醒来时间',
  `duration` INT(11) DEFAULT NULL COMMENT '睡眠时长(分钟)',
  `quality` ENUM('good','normal','poor') DEFAULT NULL COMMENT '睡眠质量',
  `position` ENUM('left','middle','right') DEFAULT NULL COMMENT '睡眠姿势(左/中/右)',
  `wake_count` INT(11) NOT NULL DEFAULT 0 COMMENT '夜醒次数',
  `notes` TEXT COMMENT '备注',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_baby_start_time` (`baby_id`, `start_time`),
  KEY `idx_user_id` (`user_id`),
  CONSTRAINT `fk_sleep_baby` FOREIGN KEY (`baby_id`) REFERENCES `babies` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_sleep_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='睡眠记录表';
