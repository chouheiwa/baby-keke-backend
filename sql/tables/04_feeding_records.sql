-- ================================================
-- 喂养记录表
-- ================================================

CREATE TABLE IF NOT EXISTS `feeding_records` (
  `id` INT(11) NOT NULL AUTO_INCREMENT COMMENT '记录ID',
  `baby_id` INT(11) NOT NULL COMMENT '宝宝ID',
  `user_id` INT(11) NOT NULL COMMENT '记录人ID',
  `feeding_type` ENUM('breast','formula','solid') NOT NULL COMMENT '喂养类型(breast母乳/formula奶粉/solid辅食)',

  -- 母乳喂养字段
  `feeding_sequence` JSON DEFAULT NULL COMMENT '喂养序列(母乳交替记录)',
  `breast_side` ENUM('left','right','both','unknown') DEFAULT NULL COMMENT '哺乳侧(用于快速记录模式)',

  -- 奶粉/辅食字段
  `bottle_content` ENUM('breast','formula') DEFAULT NULL COMMENT '奶瓶内容(母乳/奶粉)',
  `amount` INT(11) DEFAULT NULL COMMENT '奶量(ml)或食量(g)',
  `food_name` VARCHAR(100) DEFAULT NULL COMMENT '食物名称',
  `start_time` TIMESTAMP NOT NULL COMMENT '开始时间',
  `end_time` TIMESTAMP NULL DEFAULT NULL COMMENT '结束时间',
  `notes` TEXT COMMENT '备注',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_baby_time` (`baby_id`, `start_time`),
  KEY `idx_user_id` (`user_id`),
  CONSTRAINT `fk_feeding_baby` FOREIGN KEY (`baby_id`) REFERENCES `babies` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_feeding_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='喂养记录表';
