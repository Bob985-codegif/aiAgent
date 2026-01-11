const mysql = require('mysql2/promise');

async function run() {
    const connection = await mysql.createConnection({
        host: '192.168.242.128',
        user: 'root',
        password: 'root',
        database: 'book'
    });

    try {
        console.log('Connecting to database...');
        // Set Auto Increment to 10000
        await connection.query('ALTER TABLE imooc_ebook AUTO_INCREMENT = 10000');
        console.log('✅ Success! Next book ID will start from 10000.');
        console.log('Please add a new book in the frontend to see the effect.');
    } catch (err) {
        console.error('❌ Error:', err.message);
    } finally {
        await connection.end();
    }
}

run();
