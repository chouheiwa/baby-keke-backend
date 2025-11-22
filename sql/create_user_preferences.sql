-- 创建用户偏好设置表
CREATE TABLE IF NOT EXISTS user_preferences (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id INT(11) NOT NULL,
    preference_key VARCHAR(100) NOT NULL,
    preference_value JSON NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT unique_user_preference UNIQUE(user_id, preference_key),
    CONSTRAINT fk_user_preferences_user_id FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 创建索引以提高查询性能
CREATE INDEX idx_user_preferences_user_id ON user_preferences(user_id);

-- 添加注释
ALTER TABLE user_preferences COMMENT = '用户偏好设置表，存储用户的个性化配置';
ALTER TABLE user_preferences MODIFY COLUMN preference_key VARCHAR(100) NOT NULL COMMENT '偏好设置的键，如 quick_actions_order, quick_actions_expanded';
ALTER TABLE user_preferences MODIFY COLUMN preference_value JSON NOT NULL COMMENT '偏好设置的值，JSON格式存储灵活的数据结构';
