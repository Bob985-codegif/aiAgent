# 电商API - 数据库连接说明

## 项目概述
这是一个电商API项目，已配置MySQL数据库连接。

## 数据库配置
数据库连接配置位于 `config/dbConfig.js` 文件中：
- 主机: `192.168.242.128`
- 端口: `3306`
- 用户: `root`
- 密码: `root`
- 字符集: `utf8mb4`

## 数据库工具类
项目中包含了一个数据库工具类 `utils/dbUtils.js`，提供了以下便捷方法：

### DatabaseUtil 类方法
- `query(sql, params)` - 执行任意SQL查询
- `findOne(sql, params)` - 查询单条记录
- `findAll(sql, params)` - 查询多条记录
- `insert(table, data)` - 插入数据
- `update(table, data, where, whereParams)` - 更新数据
- `delete(table, where, whereParams)` - 删除数据
- `findById(table, id)` - 根据ID查找记录

## API路由
- `/` - 主页
- `/api/test-db` - 测试数据库连接
- `/api/databases` - 获取所有数据库列表
- `/api/users` - 示例：获取用户列表

## 使用示例
```javascript
const DatabaseUtil = require('./utils/dbUtils');

// 查询所有商品
const products = await DatabaseUtil.findAll('SELECT * FROM products');

// 插入新用户
const newUser = {
  name: 'John Doe',
  email: 'john@example.com',
  created_at: new Date()
};
await DatabaseUtil.insert('users', newUser);

// 更新用户信息
await DatabaseUtil.update(
  'users', 
  { name: 'Jane Doe' }, 
  'email = ?', 
  ['john@example.com']
);

// 删除用户
await DatabaseUtil.delete('users', 'id = ?', [1]);

// 根据ID查找用户
const user = await DatabaseUtil.findById('users', 1);
```

## 启动项目
```bash
npm run dev
```

服务器将在 `http://localhost:8000` 上运行。