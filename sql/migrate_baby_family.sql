-- ================================================
-- 数据库迁移脚本: baby_family 表升级
-- 从旧版本迁移到支持角色显示名称的新版本
-- ================================================

USE `baby_record`;

-- 备份旧表
CREATE TABLE IF NOT EXISTS `baby_family_backup` LIKE `baby_family`;
INSERT INTO `baby_family_backup` SELECT * FROM `baby_family`;

-- 删除旧表
DROP TABLE IF EXISTS `baby_family`;

-- 创建新表（使用 v2 版本）
CREATE TABLE IF NOT EXISTS `baby_family` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `baby_id` INT(11) NOT NULL COMMENT '宝宝ID',
  `user_id` INT(11) NOT NULL COMMENT '用户ID',
  `relation` ENUM('mom', 'dad', 'grandpa_p', 'grandma_p', 'grandpa_m', 'grandma_m', 'other') DEFAULT NULL COMMENT '关系: mom-妈妈, dad-爸爸, grandpa_p-爷爷, grandma_p-奶奶, grandpa_m-外公, grandma_m-外婆, other-其他',
  `relation_display` VARCHAR(50) DEFAULT NULL COMMENT '角色显示名称（用于自定义角色或特殊称呼）',
  `is_admin` TINYINT(1) NOT NULL DEFAULT 0 COMMENT '是否为管理员(0否1是)',
  `joined_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '加入时间',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_baby_user` (`baby_id`, `user_id`) COMMENT '同一用户在同一家庭中只能有一个角色',
  KEY `idx_baby_relation` (`baby_id`, `relation`),
  KEY `idx_user_id` (`user_id`),
  CONSTRAINT `fk_baby_family_baby` FOREIGN KEY (`baby_id`) REFERENCES `babies` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_baby_family_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='宝宝-家庭成员关系表';

-- 数据迁移
-- 将旧表的关系字段映射到新的 ENUM 值
INSERT INTO `baby_family` (baby_id, user_id, relation, relation_display, is_admin, created_at)
SELECT
  baby_id,
  user_id,
  CASE
    WHEN relation = '妈妈' THEN 'mom'
    WHEN relation = '爸爸' THEN 'dad'
    WHEN relation = '爷爷' THEN 'grandpa_p'
    WHEN relation = '奶奶' THEN 'grandma_p'
    WHEN relation = '外公' THEN 'grandpa_m'
    WHEN relation = '外婆' THEN 'grandma_m'
    ELSE 'other'
  END as relation,
  relation as relation_display, -- 保留原始显示名称
  is_admin,
  created_at
FROM `baby_family_backup`;

-- 验证迁移结果
SELECT
  COUNT(*) as old_count,
  (SELECT COUNT(*) FROM baby_family) as new_count,
  CASE
    WHEN COUNT(*) = (SELECT COUNT(*) FROM baby_family)
    THEN '✅ 迁移成功'
    ELSE '❌ 记录数不一致，请检查'
  END as status
FROM `baby_family_backup`;

-- 显示迁移后的数据示例
SELECT
  bf.id,
  b.nickname as baby_name,
  u.nickname as user_name,
  bf.relation,
  bf.relation_display,
  bf.is_admin
FROM baby_family bf
LEFT JOIN babies b ON bf.baby_id = b.id
LEFT JOIN users u ON bf.user_id = u.id
LIMIT 5;

-- ================================================
-- 迁移完成提示
-- ================================================
-- 如果迁移成功，可以删除备份表：
-- DROP TABLE `baby_family_backup`;
--
-- 如果迁移失败，可以回滚：
-- DROP TABLE `baby_family`;
-- RENAME TABLE `baby_family_backup` TO `baby_family`;
-- ================================================
