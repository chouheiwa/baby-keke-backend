CREATE TABLE `album_records` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `baby_id` int(11) NOT NULL COMMENT '宝宝ID',
  `user_id` int(11) NOT NULL COMMENT '上传者ID',
  `file_id` varchar(255) NOT NULL COMMENT '云存储文件ID',
  `media_type` varchar(20) NOT NULL DEFAULT 'image' COMMENT '媒体类型: image, video',
  `description` text COMMENT '描述/备注',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_baby_id` (`baby_id`),
  KEY `idx_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='成长相册表';
