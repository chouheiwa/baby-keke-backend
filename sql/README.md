# SQL 数据库脚本

本目录包含可可宝宝记项目的所有数据库DDL脚本。

## 目录结构

```
sql/
├── README.md                  # 本文件
├── init_all_tables.sql        # 主初始化脚本（执行所有表创建）
└── tables/                    # 各表的DDL脚本
    ├── 01_users.sql           # 用户表
    ├── 02_babies.sql          # 宝宝信息表
    ├── 03_baby_family_v2.sql  # 宝宝-家庭成员关系表
    ├── 04_feeding_records.sql # 喂养记录表
    ├── 05_diaper_records.sql  # 排便记录表
    ├── 06_sleep_records.sql   # 睡眠记录表
    ├── 07_growth_records.sql  # 生长发育记录表
    ├── 08_invitations.sql     # 家庭邀请表
    ├── 09_user_sessions.sql   # 用户会话表
    └── 10_files.sql           # 文件存储表（COS）
```

## 使用方法

### 方式1：执行主脚本（推荐）

在MySQL命令行中执行：

```bash
# 登录MySQL
mysql -u root -p

# 执行主脚本（会自动创建数据库和所有表）
source /path/to/sql/init_all_tables.sql
```

或者一条命令执行：

```bash
mysql -u root -p < /path/to/sql/init_all_tables.sql
```

### 方式2：单独执行某个表

如果只需要创建某个表：

```bash
# 先切换到目标数据库
mysql -u root -p
USE baby_record;

# 执行单个表的DDL
source /path/to/sql/tables/01_users.sql
```

### 方式3：按顺序手动执行

**重要**: 由于表之间有外键依赖关系，必须按照编号顺序执行：

1. 01_users.sql（无依赖）
2. 02_babies.sql（依赖 users）
3. 03_baby_family_v2.sql（依赖 users, babies）
4. 04_feeding_records.sql（依赖 babies, users）
5. 05_diaper_records.sql（依赖 babies, users）
6. 06_sleep_records.sql（依赖 babies, users）
7. 07_growth_records.sql（依赖 babies, users）
8. 08_invitations.sql（依赖 babies, users）
9. 09_user_sessions.sql（依赖 users）
10. 10_files.sql（依赖 users）

## 数据库信息

- **数据库名称**: baby_record
- **字符集**: utf8mb4
- **排序规则**: utf8mb4_unicode_ci
- **引擎**: InnoDB
- **MySQL版本**: 5.8+

## 表说明

### 用户相关表（5张）

1. **users** - 用户表
   - 存储微信用户基本信息
   - 主键: id
   - 唯一键: openid

2. **user_sessions** - 用户会话表
   - 存储微信登录会话信息（openid、session_key）
   - 外键: user_id → users(id)
   - 级联删除: 删除用户时自动删除会话

3. **babies** - 宝宝信息表
   - 存储宝宝基本信息
   - 外键: created_by → users(id)

4. **baby_family** - 宝宝-家庭成员关系表
   - 管理宝宝和家庭成员的多对多关系
   - 外键: baby_id → babies(id), user_id → users(id)
   - 级联删除: 删除宝宝时自动删除关系

5. **invitations** - 家庭邀请表
   - 管理家庭成员邀请
   - 外键: baby_id → babies(id), inviter_id → users(id)
   - 级联删除: 删除宝宝时自动删除邀请

6. **files** - 文件存储表
   - 存储腾讯云COS对象存储的文件元数据
   - 外键: uploaded_by → users(id)
   - 支持关联到不同业务模块（宝宝头像、记录照片等）

### 记录相关表（4张）

6. **feeding_records** - 喂养记录表
   - 记录母乳/奶粉/辅食喂养
   - 外键: baby_id → babies(id), user_id → users(id)
   - 级联删除: 删除宝宝时自动删除记录

7. **diaper_records** - 排便记录表
   - 记录尿/便情况
   - 外键: baby_id → babies(id), user_id → users(id)
   - 级联删除: 删除宝宝时自动删除记录

8. **sleep_records** - 睡眠记录表
   - 记录睡眠时间和质量
   - 外键: baby_id → babies(id), user_id → users(id)
   - 级联删除: 删除宝宝时自动删除记录

9. **growth_records** - 生长发育记录表
   - 记录体重、身高、头围
   - 外键: baby_id → babies(id), user_id → users(id)
   - 级联删除: 删除宝宝时自动删除记录

## 注意事项

1. **外键约束**: 所有记录表都有外键约束，删除宝宝会自动删除相关记录
2. **字符编码**: 使用 utf8mb4 支持emoji表情
3. **时间字段**: 所有表都有 created_at 和 updated_at 自动时间戳
4. **索引优化**: 查询字段已建立索引（baby_id + 时间字段）
5. **级联删除**: 删除 baby 会级联删除所有相关记录

## 删除所有表

如果需要重新初始化数据库，可以执行：

```sql
-- 警告：此操作会删除所有数据！
-- 必须按照外键依赖的逆序删除
DROP TABLE IF EXISTS `feeding_records`;
DROP TABLE IF EXISTS `diaper_records`;
DROP TABLE IF EXISTS `sleep_records`;
DROP TABLE IF EXISTS `growth_records`;
DROP TABLE IF EXISTS `invitations`;
DROP TABLE IF EXISTS `baby_family`;
DROP TABLE IF EXISTS `files`;
DROP TABLE IF EXISTS `babies`;
DROP TABLE IF EXISTS `user_sessions`;
DROP TABLE IF EXISTS `users`;
```

## 备份建议

在生产环境中，建议：

1. 定期备份数据库
2. 执行DDL前先备份
3. 重要操作前测试

```bash
# 备份数据库
mysqldump -u root -p baby_record > backup_$(date +%Y%m%d_%H%M%S).sql
```
