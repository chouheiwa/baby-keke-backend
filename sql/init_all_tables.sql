-- ================================================
-- 可可宝宝记 - 数据库初始化脚本（全部表）
-- 数据库版本: MySQL 5.8
-- 字符集: utf8mb4
-- ================================================

-- 创建数据库（如果不存在）
CREATE DATABASE IF NOT EXISTS `baby_record`
DEFAULT CHARACTER SET utf8mb4
DEFAULT COLLATE utf8mb4_unicode_ci;

USE `baby_record`;

-- ================================================
-- 按顺序执行表创建
-- 注意：有外键依赖关系的表必须按顺序创建
-- ================================================

-- 1. 用户表（基础表，无外键依赖）
SOURCE tables/01_users.sql;

-- 2. 宝宝信息表（依赖 users 表）
SOURCE tables/02_babies.sql;

-- 3. 宝宝-家庭成员关系表（依赖 users 和 babies 表）
-- 使用优化版本，支持角色显示名称和更多角色类型
SOURCE tables/03_baby_family_v2.sql;

-- 4. 喂养记录表（依赖 babies 和 users 表）
SOURCE tables/04_feeding_records.sql;

-- 5. 排便记录表（依赖 babies 和 users 表）
SOURCE tables/05_diaper_records.sql;

-- 6. 睡眠记录表（依赖 babies 和 users 表）
SOURCE tables/06_sleep_records.sql;

-- 7. 生长发育记录表（依赖 babies 和 users 表）
SOURCE tables/07_growth_records.sql;

-- 8. 家庭邀请表（依赖 babies 和 users 表）
SOURCE tables/08_invitations.sql;

-- 9. 用户会话表（依赖 users 表）
SOURCE tables/09_user_sessions.sql;

-- ================================================
-- 初始化完成
-- ================================================
SELECT '✅ 数据库初始化完成！' AS status;
