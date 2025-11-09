-- ================================================
-- 排便/排尿记录表（尿不湿记录）
-- ================================================

CREATE TABLE IF NOT EXISTS `diaper_records` (
  `id` INT(11) NOT NULL AUTO_INCREMENT COMMENT '记录ID',
  `baby_id` INT(11) NOT NULL COMMENT '宝宝ID',
  `user_id` INT(11) NOT NULL COMMENT '记录人ID',
  `diaper_type` ENUM('pee','poop','both') NOT NULL COMMENT '类型(pee尿/poop便/both两者都有)',
  `poop_amount` ENUM('少量','适中','大量') DEFAULT NULL COMMENT '大便量',
  `poop_color` VARCHAR(20) DEFAULT NULL COMMENT '大便颜色(黄色/绿色/褐色等)',
  `poop_texture` ENUM('稀','正常','干燥') DEFAULT NULL COMMENT '大便性状',
  `record_time` TIMESTAMP NOT NULL COMMENT '记录时间',
  `notes` TEXT COMMENT '备注',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_baby_record_time` (`baby_id`, `record_time`),
  KEY `idx_user_id` (`user_id`),
  CONSTRAINT `fk_diaper_baby` FOREIGN KEY (`baby_id`) REFERENCES `babies` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_diaper_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='排便/排尿记录表';
