from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.book import book_bp
import os

def create_app():
    app = Flask(__name__)
    
    # 配置
    app.config['SECRET_KEY'] = 'your-secret-key-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///library.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # 初始化扩展
    from app.book.models import db
    db.init_app(app)
    
    # 注册蓝图
    app.register_blueprint(book_bp, url_prefix='/admin')
    
    # 创建数据库表
    with app.app_context():
        db.create_all()
    
    # 主页路由
    @app.route('/')
    def index():
        return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>图书管理系统</title>
            <meta charset="utf-8">
            <style>
                body {
                    font-family: Arial, sans-serif;
                    text-align: center;
                    margin-top: 100px;
                    background-color: #f5f5f5;
                }
                .container {
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }
                .btn {
                    display: inline-block;
                    padding: 15px 30px;
                    background-color: #007bff;
                    color: white;
                    text-decoration: none;
                    border-radius: 5px;
                    margin: 10px;
                }
                .btn:hover {
                    background-color: #0056b3;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>欢迎使用图书管理系统</h1>
                <p>这是一个功能完善的图书管理平台</p>
                <a href="/admin/books" class="btn">进入图书管理</a>
            </div>
        </body>
        </html>
        '''
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)