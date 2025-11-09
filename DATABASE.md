# 数据库设计文档

## 数据库信息

- **数据库类型**: MySQL 5.7+
- **字符集**: utf8mb4
- **排序规则**: utf8mb4_unicode_ci
- **引擎**: InnoDB

---

## 表结构设计

### 1. 用户相关表

#### 1.1 users - 用户表

存储微信用户基本信息。

| 字段名 | 类型 | 约束 | 说明 |
|-------|------|------|------|
| id | INT | PK, AUTO_INCREMENT | 用户ID |
| openid | VARCHAR(64) | UNIQUE, NOT NULL | 微信OpenID |
| nickname | VARCHAR(100) | NULL | 用户昵称 |
| avatar_url | VARCHAR(500) | NULL | 头像URL |
| phone | VARCHAR(20) | NULL | 手机号 |
| created_at | TIMESTAMP | NOT NULL | 创建时间 |
| updated_at | TIMESTAMP | NOT NULL | 更新时间 |

**索引**:
- PRIMARY KEY: `id`
- UNIQUE KEY: `openid`

---

#### 1.2 babies - 宝宝信息表

存储宝宝的基本信息。

| 字段名 | 类型 | 约束 | 说明 |
|-------|------|------|------|
| id | INT | PK, AUTO_INCREMENT | 宝宝ID |
| name | VARCHAR(50) | NOT NULL | 宝宝姓名 |
| gender | ENUM('male','female','unknown') | DEFAULT 'unknown' | 性别 |
| birthday | TIMESTAMP | NOT NULL | 出生日期 |
| avatar_url | VARCHAR(500) | NULL | 宝宝头像 |
| notes | TEXT | NULL | 备注 |
| created_by | INT | FK(users.id), NOT NULL | 创建人ID |
| created_at | TIMESTAMP | NOT NULL | 创建时间 |
| updated_at | TIMESTAMP | NOT NULL | 更新时间 |

**索引**:
- PRIMARY KEY: `id`
- FOREIGN KEY: `created_by` → `users(id)`

---

#### 1.3 baby_family - 宝宝-家庭成员关系表

管理宝宝和家庭成员的关联关系，支持多人照顾一个宝宝。

| 字段名 | 类型 | 约束 | 说明 |
|-------|------|------|------|
| id | INT | PK, AUTO_INCREMENT | 关系ID |
| baby_id | INT | FK(babies.id), NOT NULL | 宝宝ID |
| user_id | INT | FK(users.id), NOT NULL | 用户ID |
| relation | VARCHAR(20) | NULL | 关系(爸爸/妈妈/爷爷/奶奶等) |
| is_admin | TINYINT(1) | DEFAULT 0 | 是否为管理员(0否1是) |
| created_at | TIMESTAMP | NOT NULL | 创建时间 |

**索引**:
- PRIMARY KEY: `id`
- INDEX: `baby_id, user_id`
- FOREIGN KEY: `baby_id` → `babies(id)` ON DELETE CASCADE
- FOREIGN KEY: `user_id` → `users(id)`

---

### 2. 记录相关表

#### 2.1 feeding_records - 喂养记录表

记录宝宝的喂养信息（母乳、奶粉、辅食）。

| 字段名 | 类型 | 约束 | 说明 |
|-------|------|------|------|
| id | INT | PK, AUTO_INCREMENT | 记录ID |
| baby_id | INT | FK(babies.id), NOT NULL | 宝宝ID |
| user_id | INT | FK(users.id), NOT NULL | 记录人ID |
| feeding_type | ENUM('breast','formula','solid') | NOT NULL | 喂养类型 |
| breast_side | ENUM('left','right','both') | NULL | 哺乳侧 |
| duration_left | INT | NULL | 左侧时长(分钟) |
| duration_right | INT | NULL | 右侧时长(分钟) |
| amount | INT | NULL | 奶量(ml)或食量(g) |
| food_name | VARCHAR(100) | NULL | 食物名称 |
| start_time | TIMESTAMP | NOT NULL | 开始时间 |
| end_time | TIMESTAMP | NULL | 结束时间 |
| notes | TEXT | NULL | 备注 |
| created_at | TIMESTAMP | NOT NULL | 创建时间 |
| updated_at | TIMESTAMP | NOT NULL | 更新时间 |

**索引**:
- PRIMARY KEY: `id`
- INDEX: `baby_id, start_time`
- FOREIGN KEY: `baby_id` → `babies(id)` ON DELETE CASCADE

**字段说明**:
- `feeding_type='breast'`: 母乳喂养，使用 `breast_side`, `duration_left`, `duration_right`
- `feeding_type='formula'`: 奶粉喂养，使用 `amount`
- `feeding_type='solid'`: 辅食，使用 `food_name`, `amount`

---

#### 2.2 diaper_records - 排便记录表

记录宝宝的排便情况。

| 字段名 | 类型 | 约束 | 说明 |
|-------|------|------|------|
| id | INT | PK, AUTO_INCREMENT | 记录ID |
| baby_id | INT | FK(babies.id), NOT NULL | 宝宝ID |
| user_id | INT | FK(users.id), NOT NULL | 记录人ID |
| diaper_type | ENUM('pee','poop','both') | NOT NULL | 类型 |
| poop_amount | ENUM('少量','适中','大量') | NULL | 大便量 |
| poop_color | VARCHAR(20) | NULL | 大便颜色 |
| poop_texture | ENUM('稀','正常','干燥') | NULL | 大便性状 |
| record_time | TIMESTAMP | NOT NULL | 记录时间 |
| notes | TEXT | NULL | 备注 |
| created_at | TIMESTAMP | NOT NULL | 创建时间 |
| updated_at | TIMESTAMP | NOT NULL | 更新时间 |

**索引**:
- PRIMARY KEY: `id`
- INDEX: `baby_id, record_time`
- FOREIGN KEY: `baby_id` → `babies(id)` ON DELETE CASCADE

---

#### 2.3 sleep_records - 睡眠记录表

记录宝宝的睡眠情况。

| 字段名 | 类型 | 约束 | 说明 |
|-------|------|------|------|
| id | INT | PK, AUTO_INCREMENT | 记录ID |
| baby_id | INT | FK(babies.id), NOT NULL | 宝宝ID |
| user_id | INT | FK(users.id), NOT NULL | 记录人ID |
| sleep_type | ENUM('night','nap') | NOT NULL | 睡眠类型 |
| start_time | TIMESTAMP | NOT NULL | 入睡时间 |
| end_time | TIMESTAMP | NULL | 醒来时间 |
| duration | INT | NULL | 睡眠时长(分钟) |
| quality | ENUM('good','normal','poor') | NULL | 睡眠质量 |
| wake_count | INT | DEFAULT 0 | 夜醒次数 |
| notes | TEXT | NULL | 备注 |
| created_at | TIMESTAMP | NOT NULL | 创建时间 |
| updated_at | TIMESTAMP | NOT NULL | 更新时间 |

**索引**:
- PRIMARY KEY: `id`
- INDEX: `baby_id, start_time`
- FOREIGN KEY: `baby_id` → `babies(id)` ON DELETE CASCADE

---

#### 2.4 growth_records - 生长发育记录表

记录宝宝的体重、身高等生长指标。

| 字段名 | 类型 | 约束 | 说明 |
|-------|------|------|------|
| id | INT | PK, AUTO_INCREMENT | 记录ID |
| baby_id | INT | FK(babies.id), NOT NULL | 宝宝ID |
| user_id | INT | FK(users.id), NOT NULL | 记录人ID |
| record_date | TIMESTAMP | NOT NULL | 记录日期 |
| weight | DECIMAL(5,2) | NULL | 体重(kg) |
| height | DECIMAL(5,2) | NULL | 身高/身长(cm) |
| head_circumference | DECIMAL(5,2) | NULL | 头围(cm) |
| notes | TEXT | NULL | 备注 |
| created_at | TIMESTAMP | NOT NULL | 创建时间 |
| updated_at | TIMESTAMP | NOT NULL | 更新时间 |

**索引**:
- PRIMARY KEY: `id`
- INDEX: `baby_id, record_date`
- FOREIGN KEY: `baby_id` → `babies(id)` ON DELETE CASCADE

---

## 数据库初始化

### 方式1: 使用SQL脚本（推荐）

```bash
# 连接到MySQL
mysql -u root -p

# 执行SQL脚本
source /path/to/sql/init_all_tables.sql
```

### 方式2: 使用Python脚本

```bash
# 激活虚拟环境
source venv/bin/activate

# 配置环境变量（.env文件）
# 确保数据库连接信息正确

# 运行初始化脚本
python init_database.py
```

### 方式3: 通过FastAPI自动创建

启动应用时，会自动调用 `init_db()` 创建所有表。

```bash
python run.py 0.0.0.0 8000
```

---

## ER 图

```
┌─────────────┐
│    users    │
└──────┬──────┘
       │
       │ 1:N
       │
┌──────▼──────┐        ┌─────────────┐
│baby_family  │───────▶│   babies    │
└─────────────┘  N:1   └──────┬──────┘
                              │
                              │ 1:N
                              │
            ┌─────────────────┼─────────────────┬────────────────┐
            │                 │                 │                │
     ┌──────▼──────┐  ┌───────▼──────┐  ┌──────▼──────┐  ┌──────▼──────┐
     │  feeding    │  │   diaper     │  │   sleep     │  │   growth    │
     │  _records   │  │  _records    │  │  _records   │  │  _records   │
     └─────────────┘  └──────────────┘  └─────────────┘  └─────────────┘
```

---

## 数据库使用注意事项

### 1. 字符编码
- 所有表使用 `utf8mb4` 字符集
- 支持emoji表情存储

### 2. 时区设置
- 所有时间字段使用 `TIMESTAMP` 类型
- 建议MySQL服务器设置为 UTC 时区
- 应用层处理时区转换

### 3. 级联删除
- 删除宝宝时，会自动删除该宝宝的所有记录
- 删除用户不会级联删除宝宝和记录

### 4. 索引优化
- 查询时优先使用 `baby_id` + 时间字段的组合索引
- `openid` 字段建立唯一索引，用于用户登录

### 5. 数据备份
- 建议定期备份数据库
- 重要数据删除前做好备份

---

## 后续扩展

未来版本可能新增的表：

- `milestones` - 成长里程碑表
- `vaccines` - 疫苗接种记录表
- `medical_records` - 就医记录表
- `reminders` - 提醒设置表
- `photos` - 照片记录表
