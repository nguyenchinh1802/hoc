# app.py
import os
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Tên file cơ sở dữ liệu SQLite (đặt cùng thư mục để tiện quản lý)
DB_NAME = "expense_tracker.db"

def khoi_tao_db():
    """Khởi tạo cơ sở dữ liệu nếu chưa có file."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ngay TEXT NOT NULL,
            danh_muc TEXT NOT NULL,
            so_tien REAL NOT NULL,
            ghi_chu TEXT
        )
    """)
    # Kiểm tra dữ liệu mẫu giống như bản console
    cursor.execute("SELECT COUNT(*) FROM expenses")
    count = cursor.fetchone()[0]
    if count == 0:
        mau_data = [
            ("2026-06-10", "Ăn uống", 55000, "Ăn trưa bún chả"),
            ("2026-06-10", "Di chuyển", 30000, "Đổ xăng xe máy"),
            ("2026-06-11", "Học tập", 150000, "Mua sách tự học Python")
        ]
        cursor.executemany("""
            INSERT INTO expenses (ngay, danh_muc, so_tien, ghi_chu)
            VALUES (?, ?, ?, ?)
        """, mau_data)
    conn.commit()
    conn.close()

# Hàm bổ trợ định dạng tiền tệ trong Jinja2 template
@app.template_filter('format_money')
def format_money(value):
    try:
        return f"{value:,.0f} đ".replace(",", ".")
    except (ValueError, TypeError):
        return value

@app.route("/")
def index():
    khoi_tao_db()
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # 1. Lấy danh sách chi tiêu chi tiết
    cursor.execute("SELECT id, ngay, danh_muc, so_tien, ghi_chu FROM expenses ORDER BY ngay DESC, id DESC")
    expenses = cursor.fetchall()
    
    # 2. Lấy thống kê theo danh mục
    cursor.execute("SELECT danh_muc, SUM(so_tien) FROM expenses GROUP BY danh_muc ORDER BY SUM(so_tien) DESC")
    stats = cursor.fetchall()
    
    # 3. Tính tổng tất cả chi tiêu
    cursor.execute("SELECT SUM(so_tien) FROM expenses")
    total_sum = cursor.fetchone()[0] or 0
    
    conn.close()
    
    # Render ra trang HTML và truyền dữ liệu vào
    return render_template(
        "index.html", 
        expenses=expenses, 
        stats=stats, 
        total_sum=total_sum,
        today=datetime.now().strftime("%Y-%m-%d")
    )

@app.route("/add", methods=["POST"])
def add_expense():
    # Nhận dữ liệu từ Form gửi lên
    ngay = request.form.get("ngay")
    danh_muc = request.form.get("danh_muc", "Khác").strip()
    so_tien_raw = request.form.get("so_tien", "0")
    ghi_chu = request.form.get("ghi_chu", "").strip()
    
    # Định dạng lại ngày nếu bị trống
    if not ngay:
        ngay = datetime.now().strftime("%Y-%m-%d")
        
    # Làm sạch số tiền (loại bỏ ký tự không phải số)
    try:
        so_tien = float(so_tien_raw.replace(".", "").replace(",", "").strip())
    except ValueError:
        so_tien = 0
        
    if so_tien > 0:
        # Ghi vào SQLite
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO expenses (ngay, danh_muc, so_tien, ghi_chu)
            VALUES (?, ?, ?, ?)
        """, (ngay, danh_muc, so_tien, ghi_chu))
        conn.commit()
        conn.close()
        
    return redirect(url_for("index"))

@app.route("/delete/<int:expense_id>")
def delete_expense(expense_id):
    # Xóa dòng chi tiêu theo ID
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

@app.route("/bao-gia")
def bao_gia():
    # Route phục vụ trang tính báo giá xây dựng
    return render_template("bao_gia.html")

@app.route("/phap-ly")
def phap_ly():
    # Route phục vụ trang kiểm tra quy định xây dựng pháp lý
    return render_template("phap_ly.html")

if __name__ == "__main__":
    # Khởi chạy server ở chế độ debug để tự động tải lại code khi sửa đổi
    print("🚀 Web server đang chạy tại địa chỉ: http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
