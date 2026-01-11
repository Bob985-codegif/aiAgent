// 数据库操作工具类
const { promisePool } = require('../config/dbConfig');

class DatabaseUtil {
  /**
   * 执行查询
   * @param {string} sql - SQL查询语句
   * @param {Array} params - 查询参数
   * @returns {Promise} 查询结果
   */
  static async query(sql, params = []) {
    try {
      const [results] = await promisePool.execute(sql, params);
      return results;
    } catch (error) {
      console.error('数据库查询错误:', error.message);
      throw error;
    }
  }

  /**
   * 查询单条记录
   * @param {string} sql - SQL查询语句
   * @param {Array} params - 查询参数
   * @returns {Promise} 单条记录或null
   */
  static async findOne(sql, params = []) {
    const results = await this.query(sql, params);
    return results.length > 0 ? results[0] : null;
  }

  /**
   * 查询多条记录
   * @param {string} sql - SQL查询语句
   * @param {Array} params - 查询参数
   * @returns {Promise} 记录数组
   */
  static async findAll(sql, params = []) {
    return await this.query(sql, params);
  }

  /**
   * 插入数据
   * @param {string} table - 表名
   * @param {Object} data - 要插入的数据对象
   * @returns {Promise} 插入结果
   */
  static async insert(table, data) {
    const keys = Object.keys(data);
    const values = Object.values(data);
    const placeholders = keys.map(() => '?').join(',');

    const sql = `INSERT INTO \`${table}\` (${keys.map(key => `\`${key}\``).join(',')}) VALUES (${placeholders})`;
    
    return await this.query(sql, values);
  }

  /**
   * 更新数据
   * @param {string} table - 表名
   * @param {Object} data - 要更新的数据
   * @param {string} where - WHERE条件
   * @param {Array} whereParams - WHERE条件参数
   * @returns {Promise} 更新结果
   */
  static async update(table, data, where = '', whereParams = []) {
    const keys = Object.keys(data);
    const values = Object.values(data);
    const setClause = keys.map(key => `\`${key}\` = ?`).join(', ');

    let sql = `UPDATE \`${table}\` SET ${setClause}`;
    if (where) {
      sql += ` WHERE ${where}`;
    }
    
    return await this.query(sql, [...values, ...whereParams]);
  }

  /**
   * 删除数据
   * @param {string} table - 表名
   * @param {string} where - WHERE条件
   * @param {Array} whereParams - WHERE条件参数
   * @returns {Promise} 删除结果
   */
  static async delete(table, where = '', whereParams = []) {
    let sql = `DELETE FROM \`${table}\``;
    if (where) {
      sql += ` WHERE ${where}`;
    }
    
    return await this.query(sql, whereParams);
  }

  /**
   * 根据ID查找记录
   * @param {string} table - 表名
   * @param {number} id - 记录ID
   * @returns {Promise} 记录或null
   */
  static async findById(table, id) {
    const sql = `SELECT * FROM \`${table}\` WHERE id = ?`;
    return await this.findOne(sql, [id]);
  }
}

module.exports = DatabaseUtil;