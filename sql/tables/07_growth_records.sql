-- ================================================
-- 生长发育记录表
-- ================================================

CREATE TABLE IF NOT EXISTS `growth_records` (
  `id` INT(11) NOT NULL AUTO_INCREMENT COMMENT '记录ID',
  `baby_id` INT(11) NOT NULL COMMENT '宝宝ID',
  `user_id` INT(11) NOT NULL COMMENT '记录人ID',
  `record_date` TIMESTAMP NOT NULL COMMENT '记录日期',
  `weight` DECIMAL(5,2) DEFAULT NULL COMMENT '体重(kg)',
  `height` DECIMAL(5,2) DEFAULT NULL COMMENT '身高/身长(cm)',
  `head_circumference` DECIMAL(5,2) DEFAULT NULL COMMENT '头围(cm)',
  `notes` TEXT COMMENT '备注',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_baby_record_date` (`baby_id`, `record_date`),
  KEY `idx_user_id` (`user_id`),
  CONSTRAINT `fk_growth_baby` FOREIGN KEY (`baby_id`) REFERENCES `babies` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_growth_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='生长发育记录表';
