import pymysql

# 配置
MYSQL_CONFIG = {
    'host': '192.168.242.128',
    'port': 3306,
    'user': 'root',
    'password': 'root',
    'charset': 'utf8mb4',
}


def test_connection():
    """测试基本连接"""
    print("=" * 60)
    print("测试 MySQL 连接")
    print("=" * 60)

    try:
        conn = pymysql.connect(**MYSQL_CONFIG)
        print("✅ 连接成功！\n")

        cursor = conn.cursor()

        # 1. 查看版本
        print("1️⃣ MySQL 版本：")
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print(f"   {version[0]}\n")

        # 2. 列出所有数据库
        print("2️⃣ 数据库列表：")
        cursor.execute("SHOW DATABASES")
        databases = cursor.fetchall()
        for db in databases:
            print(f"   - {db[0]}")
        print()

        # 3. 使用 test 数据库
        print("3️⃣ 使用 test 数据库：")
        cursor.execute("USE test")
        print("   ✅ 已切换到 test 数据库\n")

        # 4. 列出表
        print("4️⃣ test 数据库的表：")
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        if tables:
            for table in tables:
                print(f"   - {table[0]}")
        else:
            print("   (暂无表)")
        print()

        # 5. 创建测试表
        print("5️⃣ 创建测试表：")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS test_users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(50) NOT NULL,
                email VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        print("   ✅ 表 test_users 已创建\n")

        # 6. 插入数据
        print("6️⃣ 插入测试数据：")
        cursor.execute("""
            INSERT INTO test_users (name, email) VALUES 
            ('Alice', 'alice@test.com'),
            ('Bob', 'bob@test.com')
        """)
        conn.commit()
        print(f"   ✅ 插入了 {cursor.rowcount} 条记录\n")

        # 7. 查询数据
        print("7️⃣ 查询数据：")
        cursor.execute("SELECT * FROM test_users")
        users = cursor.fetchall()
        for user in users:
            print(f"   ID: {user[0]}, Name: {user[1]}, Email: {user[2]}")
        print()

        cursor.close()
        conn.close()

        print("=" * 60)
        print("✅ 所有测试通过！")
        print("=" * 60)

    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_connection()
