-- Create feeding_ongoing table for synchronized timer
CREATE TABLE IF NOT EXISTS `feeding_ongoing` (
  `id` INT NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `baby_id` INT NOT NULL COMMENT '宝宝ID',
  `start_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '本次喂养开始时间',
  `current_side` ENUM('left', 'right', 'paused') NOT NULL DEFAULT 'paused' COMMENT '当前状态',
  `last_action_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最后一次操作时间',
  `accumulated_left` INT NOT NULL DEFAULT 0 COMMENT '左侧累计时长(秒)',
  `accumulated_right` INT NOT NULL DEFAULT 0 COMMENT '右侧累计时长(秒)',
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_baby` (`baby_id`),
  CONSTRAINT `fk_ongoing_baby` FOREIGN KEY (`baby_id`) REFERENCES `babies` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='正在进行的喂养记录';
