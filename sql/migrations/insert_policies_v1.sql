CREATE TABLE IF NOT EXISTS `policies` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `type` ENUM('terms','privacy') NOT NULL,
  `version` VARCHAR(32) NOT NULL,
  `title` VARCHAR(200) DEFAULT NULL,
  `content` LONGTEXT NOT NULL,
  `format` ENUM('markdown','html','text') NOT NULL DEFAULT 'markdown',
  `locale` VARCHAR(16) NOT NULL DEFAULT 'zh-CN',
  `status` ENUM('draft','published','archived') NOT NULL DEFAULT 'draft',
  `effective_at` TIMESTAMP NULL DEFAULT NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_policy_type_version_locale` (`type`,`version`,`locale`),
  KEY `idx_policy_type` (`type`),
  KEY `idx_policy_locale` (`locale`),
  KEY `idx_policy_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `policies` (`type`, `version`, `title`, `content`, `format`, `locale`, `status`, `effective_at`) VALUES (
  'terms',
  '1.0.0',
  '可可宝宝记用户协议（V1.0.0）',
  '# 可可宝宝记用户协议（V1.0.0）\n本协议是您（用户）与“可可宝宝记”之间关于使用本应用及服务的法律文件。您注册、登录或使用本应用，即视为您同意本协议全部条款。\n\n## 账户与使用\n- 保证信息真实、准确、完整并及时更新。\n- 妥善保管账户，不得用于违法或异常用途。\n- 未经授权不得逆向工程、抓取、批量导出等。\n\n## 服务内容与变更\n- 提供宝宝成长记录：喂养、如厕、睡眠、生长发育、成员关联与共享等。\n- 我们可根据运营与法律要求进行调整或升级，并通过公告或版本更新提示。\n\n## 用户行为规范\n- 不得上传、发布或传输违法、侵权、低俗内容；不扰乱平台秩序。\n- 不得未经许可用于商业采集、数据销售或衍生服务。\n\n## 数据与隐私\n- 依《隐私政策》处理您的个人信息与记录数据。\n- 您有权访问、更正与删除合法范围内的个人数据。\n\n## 知识产权\n- 本应用的代码、设计、文档等知识产权归我们所有；未经授权不得使用、复制、修改或分发。\n\n## 免责声明与责任限制\n- 因不可抗力、第三方或网络环境导致的服务中断、数据差异，我们不承担超出法定范围的责任。\n- 记录数据仅供参考，不构成医疗建议。\n\n## 终止与违约处理\n- 如您违反本协议或相关法律，我们有权中止或终止服务并保留追责权利。\n\n## 适用法律与争议解决\n- 适用中华人民共和国法律；争议由我们所在地人民法院管辖。\n\n## 联系方式\n- 应用内反馈或客服渠道。\n\n## 生效日期\n- 生效日期：发布之日；版本号：V1.0.0',
  'markdown',
  'zh-CN',
  'published',
  NOW()
) ON DUPLICATE KEY UPDATE `title`=VALUES(`title`), `content`=VALUES(`content`), `format`=VALUES(`format`), `status`=VALUES(`status`), `effective_at`=VALUES(`effective_at`);

INSERT INTO `policies` (`type`, `version`, `title`, `content`, `format`, `locale`, `status`, `effective_at`) VALUES (
  'privacy',
  '1.0.0',
  '可可宝宝记隐私政策（V1.0.0）',
  '# 可可宝宝记隐私政策（V1.0.0）\n我们重视您的隐私与数据安全，说明如何收集、使用、存储、共享与保护您的个人信息，以及您如何管理与控制这些信息。\n\n## 收集的信息\n- 账户信息：微信 OpenID、昵称、手机号（如您提供）。\n- 使用数据：宝宝喂养、如厕、睡眠、生长发育记录及时间戳。\n- 设备与日志：请求头中的 OpenID、访问时间、基础网络信息。\n\n## 信息的使用\n- 提供与维护服务功能、记录同步、账户管理与登录校验。\n- 保障安全、风控与服务质量优化。\n- 在授权或法律允许范围内，用于数据分析与功能迭代。\n\n## 信息的共享与公开\n- 不向第三方出售您的个人信息。\n- 法律要求或执法机关合法请求时可能披露必要信息。\n- 家庭成员功能涉及关联用户间记录可见性；需经管理员授权。\n\n## 存储与保护\n- 数据存储于受控数据库，采用访问控制与审计。\n- 采取合理技术与管理措施防止泄漏、损坏或丢失。\n- 除法律另有规定外，保存期限以实现目的所需的最短时间为原则。\n\n## 您的权利\n- 访问与更正：在应用内查看和更新个人资料及记录。\n- 删除与撤回：可申请删除个人信息或撤回授权；部分功能可能受限。\n- 投诉与申诉：通过客服渠道提交投诉，我们在法定或合理期限内处理。\n\n## 未成年人保护\n- 服务对象包含监护人记录宝宝信息；监护人应确保记录与共享合法、适当。\n\n## 跨境传输\n- 目前不进行跨境传输；如未来涉及，将按法律要求评估与告知。\n\n## 政策更新\n- 我们可能更新本政策，并在发布后生效。可通过“当前生效版本”接口获知最新版本。\n\n## 联系方式\n- 应用内客服或反馈渠道。\n\n## 生效日期\n- 生效日期：发布之日；版本号：V1.0.0',
  'markdown',
  'zh-CN',
  'published',
  NOW()
) ON DUPLICATE KEY UPDATE `title`=VALUES(`title`), `content`=VALUES(`content`), `format`=VALUES(`format`), `status`=VALUES(`status`), `effective_at`=VALUES(`effective_at`);