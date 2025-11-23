CREATE TABLE `jaundice_records` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `baby_id` int(11) NOT NULL COMMENT '宝宝ID',
  `user_id` int(11) NOT NULL COMMENT '记录人ID',
  `record_date` datetime NOT NULL COMMENT '记录时间',
  `value` decimal(5,2) NOT NULL COMMENT '黄疸值(mg/dL)',
  `photo_url` varchar(255) DEFAULT NULL COMMENT '照片URL',
  `notes` text COMMENT '备注',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_baby_date` (`baby_id`,`record_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='黄疸记录表';
