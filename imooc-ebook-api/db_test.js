// 数据库连接测试文件
const { pool } = require('./config/dbConfig');

// 测试数据库连接
async function testConnection() {
  try {
    console.log('正在尝试连接到MySQL数据库...');
    
    // 执行一个简单的查询来测试连接
    const [results] = await pool.execute('SELECT 1 + 1 AS solution');
    
    console.log('数据库连接成功！');
    console.log('测试查询结果:', results[0]);
    
    return true;
  } catch (error) {
    console.error('数据库连接失败:', error.message);
    return false;
  }
}

// 列出所有数据库
async function listDatabases() {
  try {
    console.log('\n正在获取数据库列表...');
    const [databases] = await pool.execute('SHOW DATABASES');
    
    console.log('可用数据库:');
    databases.forEach((db, index) => {
      console.log(`${index + 1}. ${db.Database}`);
    });
    
    return databases;
  } catch (error) {
    console.error('获取数据库列表失败:', error.message);
    return [];
  }
}

// 主函数
async function main() {
  console.log('=== 开始数据库连接测试 ===');
  
  // 测试连接
  const isConnected = await testConnection();
  
  if (isConnected) {
    // 获取数据库列表
    await listDatabases();
  }
  
  // 关闭连接池
  pool.end((err) => {
    if (err) {
      console.error('关闭连接池时发生错误:', err);
    } else {
      console.log('\n连接池已关闭');
    }
  });
}

// 如果此文件被直接运行，则执行主函数
if (require.main === module) {
  main();
}

module.exports = {
  pool,
  testConnection,
  listDatabases
};