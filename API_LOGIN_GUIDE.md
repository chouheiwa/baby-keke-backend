# 登录接口使用指南

## 快捷登录接口

### 接口信息

- **URL**: `POST /api/users/login`
- **功能**: 小程序快捷登录，自动注册新用户
- **响应**: 返回用户信息

### 请求示例

```json
POST /api/users/login
Content-Type: application/json

{
  "openid": "oABCD1234567890abcdef",
  "nickname": "可可妈妈",
  "avatar_url": "https://thirdwx.qlogo.cn/mmopen/xxx"
}
```

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| openid | string | 是 | 微信OpenID |
| nickname | string | 否 | 用户昵称（首次登录时可提供） |
| avatar_url | string | 否 | 用户头像URL（首次登录时可提供） |

### 响应示例

```json
{
  "id": 1,
  "openid": "oABCD1234567890abcdef",
  "nickname": "可可妈妈",
  "avatar_url": "https://thirdwx.qlogo.cn/mmopen/xxx",
  "phone": null,
  "created_at": "2024-11-09T12:30:00",
  "updated_at": "2024-11-09T12:30:00"
}
```

### 登录逻辑

1. **首次登录**
   - 传入 openid、nickname、avatar_url
   - 系统自动创建新用户
   - 返回用户信息

2. **再次登录**
   - 传入 openid
   - 系统查找已存在的用户
   - 返回用户信息

### 微信小程序端示例代码

```javascript
// 小程序登录示例
async function login() {
  try {
    // 1. 调用微信登录获取 code
    const loginRes = await wx.cloud.callFunction({
      name: 'login',  // 云函数获取 openid
    });

    const openid = loginRes.result.openid;

    // 2. 获取用户信息
    const userInfo = await wx.getUserProfile({
      desc: '用于完善用户资料',
    });

    // 3. 调用后台登录接口
    const response = await wx.request({
      url: 'https://your-domain.com/api/users/login',
      method: 'POST',
      data: {
        openid: openid,
        nickname: userInfo.userInfo.nickName,
        avatar_url: userInfo.userInfo.avatarUrl,
      },
    });

    // 4. 保存用户信息到本地
    wx.setStorageSync('userInfo', response.data);

    console.log('登录成功', response.data);
  } catch (error) {
    console.error('登录失败', error);
  }
}
```

## 后续API调用

登录成功后，小程序端的其他API调用会自动带上 openid（微信云托管自动注入 `X-Wx-Openid` 请求头），后端会自动识别当前用户。

### 示例：获取当前用户信息

```javascript
// 无需手动传递 openid，云托管会自动注入请求头
const userInfo = await wx.request({
  url: 'https://your-domain.com/api/users/me',
  method: 'GET',
});
```

### 示例：创建宝宝

```javascript
const baby = await wx.request({
  url: 'https://your-domain.com/api/babies/',
  method: 'POST',
  data: {
    name: '可可',
    gender: 'female',
    birthday: '2024-01-01T00:00:00',
  },
});
```

## 权限验证说明

所有需要登录的接口都会：

1. 从请求头获取 `X-Wx-Openid`
2. 查询数据库获取对应的用户ID
3. 验证用户权限（如果需要）

如果用户未登录或 openid 无效，会返回 401 错误：

```json
{
  "detail": "用户不存在，请先登录"
}
```

## 测试接口

你可以使用 Swagger UI 测试登录接口：

1. 访问 `http://localhost:8000/docs`
2. 找到 `POST /api/users/login`
3. 点击 "Try it out"
4. 输入测试数据：
   ```json
   {
     "openid": "test_openid_001",
     "nickname": "测试用户",
     "avatar_url": "https://example.com/avatar.jpg"
   }
   ```
5. 点击 "Execute"

## 注意事项

1. **openid 唯一性**
   - 同一个 openid 只会创建一次用户
   - 重复调用登录接口会返回已存在的用户信息

2. **微信云托管环境**
   - 在微信云托管环境下，`X-Wx-Openid` 会自动注入
   - 本地开发时需要手动添加此请求头进行测试

3. **安全建议**
   - 不要在客户端存储敏感信息
   - 使用 HTTPS 传输数据
   - 定期更新用户信息

## 本地开发测试

如果在本地开发环境测试，需要手动添加 `X-Wx-Openid` 请求头：

```bash
curl -X POST "http://localhost:8000/api/users/login" \
  -H "Content-Type: application/json" \
  -d '{
    "openid": "test_openid_001",
    "nickname": "测试用户",
    "avatar_url": "https://example.com/avatar.jpg"
  }'

# 后续调用其他接口时，添加 X-Wx-Openid 请求头
curl -X GET "http://localhost:8000/api/users/me" \
  -H "X-Wx-Openid: test_openid_001"
```

## 完整流程图

```
┌─────────────┐
│ 小程序启动  │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│ 调用登录接口    │
│ POST /login     │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐     是      ┌──────────────┐
│ 用户是否存在？  ├──────────────▶ 返回用户信息 │
└──────┬──────────┘              └──────────────┘
       │ 否
       ▼
┌─────────────────┐
│ 创建新用户      │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ 返回用户信息    │
└─────────────────┘
       │
       ▼
┌─────────────────┐
│ 保存到本地存储  │
└─────────────────┘
       │
       ▼
┌─────────────────┐
│ 跳转到主页      │
└─────────────────┘
```

## 相关API文档

- 获取当前用户信息: `GET /api/users/me`
- 更新用户信息: `PATCH /api/users/me`
- 获取我的宝宝列表: `GET /api/babies/my`

完整的API文档请访问: `http://localhost:8000/docs`
