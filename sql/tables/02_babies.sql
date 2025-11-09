-- ================================================
-- 宝宝信息表
-- ================================================

CREATE TABLE IF NOT EXISTS `babies` (
  `id` INT(11) NOT NULL AUTO_INCREMENT COMMENT '宝宝ID',
  `name` VARCHAR(50) NOT NULL COMMENT '宝宝姓名',
  `gender` ENUM('male','female','unknown') NOT NULL DEFAULT 'unknown' COMMENT '性别',
  `birthday` TIMESTAMP NOT NULL COMMENT '出生日期',
  `avatar_url` VARCHAR(500) DEFAULT NULL COMMENT '宝宝头像',
  `notes` TEXT COMMENT '备注',
  `created_by` INT(11) NOT NULL COMMENT '创建人ID',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_created_by` (`created_by`),
  CONSTRAINT `fk_baby_creator` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='宝宝信息表';
