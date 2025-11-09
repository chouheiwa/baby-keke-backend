-- ================================================
-- 可可宝宝记 - 数据库初始化脚本
-- 数据库版本: MySQL 5.7
-- 字符集: utf8mb4
-- ================================================

-- 创建数据库（如果不存在）
CREATE DATABASE IF NOT EXISTS `baby_record`
DEFAULT CHARACTER SET utf8mb4
DEFAULT COLLATE utf8mb4_unicode_ci;

USE `baby_record`;

-- ================================================
-- 用户相关表
-- ================================================

-- 用户表
CREATE TABLE IF NOT EXISTS `users` (
  `id` INT(11) NOT NULL AUTO_INCREMENT COMMENT '用户ID',
  `openid` VARCHAR(64) NOT NULL COMMENT '微信OpenID',
  `nickname` VARCHAR(100) DEFAULT NULL COMMENT '用户昵称',
  `avatar_url` VARCHAR(500) DEFAULT NULL COMMENT '头像URL',
  `phone` VARCHAR(20) DEFAULT NULL COMMENT '手机号',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_openid` (`openid`),
  KEY `idx_openid` (`openid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';

-- 宝宝信息表
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

-- 宝宝-家庭成员关系表
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

-- ================================================
-- 记录相关表
-- ================================================

-- 喂养记录表
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

-- 排便记录表
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='排便记录表';

-- 睡眠记录表
CREATE TABLE IF NOT EXISTS `sleep_records` (
  `id` INT(11) NOT NULL AUTO_INCREMENT COMMENT '记录ID',
  `baby_id` INT(11) NOT NULL COMMENT '宝宝ID',
  `user_id` INT(11) NOT NULL COMMENT '记录人ID',
  `sleep_type` ENUM('night','nap') NOT NULL COMMENT '睡眠类型(night夜间/nap小睡)',
  `start_time` TIMESTAMP NOT NULL COMMENT '入睡时间',
  `end_time` TIMESTAMP NULL DEFAULT NULL COMMENT '醒来时间',
  `duration` INT(11) DEFAULT NULL COMMENT '睡眠时长(分钟)',
  `quality` ENUM('good','normal','poor') DEFAULT NULL COMMENT '睡眠质量',
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

-- 生长发育记录表
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

-- ================================================
-- 示例表（保留用于测试）
-- ================================================

CREATE TABLE IF NOT EXISTS `counters` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `count` INT(11) NOT NULL DEFAULT 1,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='计数器表(示例)';

-- ================================================
-- 初始化完成
-- ================================================
