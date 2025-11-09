-- ================================================
-- 喂养记录表
-- ================================================

CREATE TABLE IF NOT EXISTS `feeding_records` (
  `id` INT(11) NOT NULL AUTO_INCREMENT COMMENT '记录ID',
  `baby_id` INT(11) NOT NULL COMMENT '宝宝ID',
  `user_id` INT(11) NOT NULL COMMENT '记录人ID',
  `feeding_type` ENUM('breast','formula','solid') NOT NULL COMMENT '喂养类型(breast母乳/formula奶粉/solid辅食)',
  `breast_side` ENUM('left','right','both') DEFAULT NULL COMMENT '哺乳侧(left左/right右/both双侧)',
  `duration_left` INT(11) DEFAULT NULL COMMENT '左侧时长(分钟)',
  `duration_right` INT(11) DEFAULT NULL COMMENT '右侧时长(分钟)',
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
