# 数据库迁移说明

## 迁移记录

### 2025-01-15: 移除头像和文件存储功能

**迁移文件**: `remove_avatar_and_files.sql`

**变更内容**:
- 删除 `files` 表
- 从 `users` 表删除 `avatar_url` 字段
- 从 `babies` 表删除 `avatar_url` 字段

**执行方法**:

#### 方法 1: 使用脚本自动执行（推荐）

```bash
# 在项目根目录执行
/tmp/run_migration.sh
```

#### 方法 2: 手动执行

```bash
# 从 .env 文件读取配置后执行
mysql -h<host> -P<port> -u<username> -p<password> < sql/migrations/remove_avatar_and_files.sql
```

#### 方法 3: 直接登录 MySQL 执行

```bash
# 登录 MySQL
mysql -h<host> -P<port> -u<username> -p

# 在 MySQL 命令行中执行
mysql> source /path/to/sql/migrations/remove_avatar_and_files.sql;
```

**注意事项**:
- ⚠️ 此迁移会删除数据，执行前请确认已备份重要数据
- ✅ 删除操作使用了 `IF EXISTS` 保护，重复执行不会报错
- ✅ 如果字段或表不存在，会自动跳过

**回滚**:
此迁移无法直接回滚，如需恢复功能，需要：
1. 重新创建表和字段
2. 恢复相关代码
3. 重新安装 COS SDK

---

## 迁移执行检查清单

执行迁移前：
- [ ] 已备份数据库
- [ ] 已确认 .env 配置正确
- [ ] 已停止正在运行的应用

执行迁移后：
- [ ] 检查迁移是否成功执行
- [ ] 验证表结构是否正确
- [ ] 重启应用并测试基本功能
