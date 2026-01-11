const express = require('express')
const cors = require('cors')
const mysql = require('mysql2/promise')
const app = express()

// Middleware
app.use(cors())
app.use(express.json())

// Database Connection Pool
const pool = mysql.createPool({
    host: '192.168.242.128', // Verified User IP
    port: 3306,
    user: 'root',
    password: 'root',
    database: 'book',        // Verified User DB Name
    charset: 'utf8mb4',
    waitForConnections: true,
    connectionLimit: 10,
    queueLimit: 0
});

// Helper: Common Response Format
const success = (data, msg = "一切ok") => ({ code: "00000", data, msg });
const fail = (msg = "操作失败") => ({ code: "50000", data: null, msg });

// Helper: Format Date for MySQL (YYYY-MM-DD)
const formatDate = (dateStr) => {
    if (!dateStr) return null;
    // If it's a full ISO string like "2023-01-14T16:00:00.000Z", string split it
    if (typeof dateStr === 'string' && dateStr.includes('T')) {
        return dateStr.split('T')[0];
    }
    return dateStr;
};

// API: File Upload
app.post('/api/v1/files', (req, res) => {
    res.json(success({
        fileUrl: "https://images.unsplash.com/photo-1544947950-fa07a98d237f?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80",
        fileName: "uploaded_cover.jpg",
    }, "文件上传成功"));
});

// Helper: Map DB Row to Frontend Model
const mapToFrontend = (row) => ({
    id: row.id,
    title: row.title,
    author: row.author,
    isbn: row.isbn,
    publisher: row.publisher,
    publishDate: row.publish_date,
    price: row.price,
    stockQuantity: row.stock,
    category: 'technology',
    description: '',
    url: row.link,
    cover: row.cover
});

// API: Book List
app.get('/api/v1/books', async (req, res) => {
    try {
        let { pageNum = 1, pageSize = 10, keywords } = req.query;
        pageNum = parseInt(pageNum);
        pageSize = parseInt(pageSize);
        const offset = (pageNum - 1) * pageSize;

        let query = 'SELECT * FROM imooc_ebook';
        let countQuery = 'SELECT COUNT(*) as total FROM imooc_ebook';
        let params = [];

        if (keywords) {
            query += ' WHERE title LIKE ? OR author LIKE ?';
            countQuery += ' WHERE title LIKE ? OR author LIKE ?';
            params = [`%${keywords}%`, `%${keywords}%`];
        }

        query += ' ORDER BY id DESC'; // ✅ Sort by newest ID to differentiate from Serial 1,2,3
        query += ' LIMIT ? OFFSET ?';
        const listParams = [...params, pageSize, offset];

        const [rows] = await pool.query(query, listParams);
        const [countResult] = await pool.query(countQuery, params);

        const total = countResult[0].total;
        const list = rows.map(mapToFrontend);

        res.json(success({ list, total }));
    } catch (err) {
        console.error(err);
        res.json(fail("数据库查询失败: " + err.message));
    }
});

// API: Book Detail
app.get('/api/v1/books/:id', async (req, res) => {
    try {
        const id = parseInt(req.params.id);
        const [rows] = await pool.query('SELECT * FROM imooc_ebook WHERE id = ?', [id]);
        if (rows.length > 0) {
            res.json(success(mapToFrontend(rows[0])));
        } else {
            res.json(fail("未找到该图书"));
        }
    } catch (err) {
        console.error(err);
        res.json(fail("查询详情失败"));
    }
});

// API: Create Book
app.post('/api/v1/books', async (req, res) => {
    try {
        const body = req.body;
        // Map Frontend -> DB
        const sql = `INSERT INTO imooc_ebook (title, author, isbn, publisher, publish_date, price, stock, link, cover) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)`;
        const values = [
            body.title,
            body.author,
            body.isbn,
            body.publisher,
            formatDate(body.publishDate), // ✅ Format Date Logic applied
            body.price,
            body.stockQuantity,
            body.url,
            body.cover || "https://images.unsplash.com/photo-1589829085413-56de8ae18c73?ixlib=rb-4.0.3&auto=format&fit=crop&w=300&q=80"
        ];

        const [result] = await pool.query(sql, values);
        res.json(success({ id: result.insertId }, "新增成功"));
    } catch (err) {
        console.error(err);
        res.json(fail("新增图书失败: " + err.message));
    }
});

// API: Update Book
app.put('/api/v1/books/:id', async (req, res) => {
    try {
        const id = parseInt(req.params.id);
        const body = req.body;

        const sql = `UPDATE imooc_ebook SET title=?, author=?, isbn=?, publisher=?, publish_date=?, price=?, stock=?, link=?, cover=? WHERE id=?`;
        const values = [
            body.title,
            body.author,
            body.isbn,
            body.publisher,
            formatDate(body.publishDate), // ✅ Format Date Logic applied
            body.price,
            body.stockQuantity,
            body.url,
            body.cover,
            id
        ];

        await pool.query(sql, values);
        res.json(success(null, "修改成功"));
    } catch (err) {
        console.error(err);
        res.json(fail("修改图书失败: " + err.message));
    }
});

// API: Delete Book
app.delete('/api/v1/books/:id', async (req, res) => {
    try {
        const id = parseInt(req.params.id);
        await pool.query('DELETE FROM imooc_ebook WHERE id = ?', [id]);
        res.json(success(null, "删除成功"));
    } catch (err) {
        console.error(err);
        res.json(fail("删除图书失败: " + err.message));
    }
});

// Root
app.get('/', (req, res) => {
    res.send('Backend Connected to MySQL (192.168.242.128)! API at /api/v1/books')
})

const server = app.listen(8000, function () {
    const host = server.address().address
    const port = server.address().port
    console.log('应用启动 successfully http://localhost:%s', port)
})