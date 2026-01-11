// 数据库配置文件
const mysql = require('mysql2');

// MySQL连接配置
const dbConfig = {
  host: '192.168.242.128',
  port: 3306,
  user: 'root',
  password: 'root',
  charset: 'utf8mb4'
};

// 创建数据库连接池
const pool = mysql.createPool(dbConfig);

// 导出连接池和连接方法
module.exports = {
  pool,
  promisePool: pool.promise(), // 支持Promise的连接池
  getConnection: () => pool.getConnection()
};