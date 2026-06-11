# expense_tracker.py
import sqlite3
from datetime import datetime

# Tên file cơ sở dữ liệu SQLite
DB_NAME = "expense_tracker.db"

def khoi_tao_db():
    """Khởi tạo cơ sở dữ liệu và tạo bảng nếu chưa tồn tại."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Tạo bảng expenses (chi tiêu)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ngay TEXT NOT NULL,
            danh_muc TEXT NOT NULL,
            so_tien REAL NOT NULL,
            ghi_chu TEXT
        )
    """)
    
    # Kiểm tra xem bảng có dữ liệu chưa
    cursor.execute("SELECT COUNT(*) FROM expenses")
    count = cursor.fetchone()[0]
    
    if count == 0:
        # Nếu chưa có dữ liệu, thêm một số dòng mẫu
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

def them_chi_tieu(ngay, danh_muc, so_tien, ghi_chu):
    """Thêm một khoản chi tiêu mới vào cơ sở dữ liệu."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Sử dụng các dấu chấm hỏi (?) làm placeholder để tránh lỗi SQL Injection (bảo mật)
    cursor.execute("""
        INSERT INTO expenses (ngay, danh_muc, so_tien, ghi_chu)
        VALUES (?, ?, ?, ?)
    """, (ngay, danh_muc, so_tien, ghi_chu))
    
    conn.commit()
    conn.close()
    print("✅ Đã ghi nhận khoản chi tiêu mới thành công!")

def xem_danh_sach():
    """Lấy danh sách tất cả các khoản chi tiêu."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, ngay, danh_muc, so_tien, ghi_chu FROM expenses ORDER BY ngay DESC")
    rows = cursor.fetchall() # Lấy tất cả kết quả trả về
    
    conn.close()
    return rows

def thong_ke_theo_danh_muc():
    """Tính tổng chi tiêu nhóm theo từng danh mục."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Sử dụng hàm tính tổng SUM và nhóm GROUP BY trong SQL
    cursor.execute("""
        SELECT danh_muc, SUM(so_tien) 
        FROM expenses 
        GROUP BY danh_muc 
        ORDER BY SUM(so_tien) DESC
    """)
    rows = cursor.fetchall()
    
    conn.close()
    return rows

def xoa_chi_tieu(id_xoa):
    """Xóa khoản chi tiêu dựa vào ID khóa chính."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Kiểm tra xem ID có tồn tại hay không trước khi xóa
    cursor.execute("SELECT id FROM expenses WHERE id = ?", (id_xoa,))
    if not cursor.fetchone():
        print(f"❌ Không tìm thấy khoản chi tiêu nào có ID = {id_xoa}!")
        conn.close()
        return False
        
    cursor.execute("DELETE FROM expenses WHERE id = ?", (id_xoa,))
    conn.commit()
    conn.close()
    print(f"🗑️ Đã xóa khoản chi tiêu có ID = {id_xoa} thành công!")
    return True

def format_money(amount):
    """Định dạng số tiền sang chuẩn hiển thị dễ đọc (ví dụ: 100,000 đ)."""
    return f"{amount:,.0f} đ".replace(",", ".")

def main():
    khoi_tao_db()
    
    while True:
        print("\n==============================================")
        print(" 💵 PHẦN MỀM QUẢN LÝ CHI TIÊU CÁ NHÂN (SQLITE) ")
        print("==============================================")
        print("1. Thêm khoản chi tiêu mới")
        print("2. Xem danh sách chi tiêu")
        print("3. Xem báo cáo thống kê theo danh mục")
        print("4. Xóa một khoản chi tiêu (theo ID)")
        print("5. Thoát chương trình")
        print("==============================================")
        
        chon = input("👉 Chọn chức năng (1-5): ").strip()
        
        if chon == "1":
            print("\n➕ THÊM CHI TIÊU MỚI:")
            
            # 1. Nhập ngày
            ngay_nhap = input("Nhập ngày (định dạng YYYY-MM-DD, bỏ trống lấy hôm nay): ").strip()
            if not ngay_nhap:
                ngay_nhap = datetime.now().strftime("%Y-%m-%d")
            else:
                try:
                    # Kiểm tra xem ngày nhập vào có đúng định dạng không
                    datetime.strptime(ngay_nhap, "%Y-%m-%d")
                except ValueError:
                    print("❌ Sai định dạng ngày! Mặc định lấy ngày hôm nay.")
                    ngay_nhap = datetime.now().strftime("%Y-%m-%d")
            
            # 2. Nhập danh mục
            print("Gợi ý danh mục: Ăn uống, Di chuyển, Mua sắm, Nhà cửa, Học tập, Giải trí...")
            danh_muc = input("Danh mục chi tiêu: ").strip()
            if not danh_muc:
                danh_muc = "Khác"
                
            # 3. Nhập số tiền
            try:
                so_tien = float(input("Số tiền chi tiêu: ").replace(".", "").replace(",", "").strip())
            except ValueError:
                print("❌ Số tiền không hợp lệ! Vui lòng thực hiện lại.")
                continue
                
            # 4. Nhập ghi chú
            ghi_chu = input("Ghi chú/Mô tả thêm (nếu có): ").strip()
            
            # Gọi hàm ghi vào SQLite
            them_chi_tieu(ngay_nhap, danh_muc, so_tien, ghi_chu)
            
        elif chon == "2":
            print("\n📋 DANH SÁCH CHI TIÊU:")
            danh_sach = xem_danh_sach()
            
            if not danh_sach:
                print("📭 Chưa có khoản chi tiêu nào được lưu trữ.")
            else:
                print(f"{'ID':<4} | {'Ngày':<10} | {'Danh mục':<12} | {'Số tiền':<15} | {'Ghi chú'}")
                print("-" * 70)
                tong_tat_ca = 0
                for row in danh_sach:
                    id_val, ngay, dm, tien, note = row
                    tong_tat_ca += tien
                    print(f"{id_val:<4} | {ngay:<10} | {dm:<12} | {format_money(tien):<15} | {note or ''}")
                print("-" * 70)
                print(f"💰 TỔNG CHI TIÊU TẤT CẢ: {format_money(tong_tat_ca)}")
                
        elif chon == "3":
            print("\n📊 THỐNG KÊ CHI TIÊU THEO DANH MỤC:")
            thong_ke = thong_ke_theo_danh_muc()
            
            if not thong_ke:
                print("📭 Chưa có dữ liệu thống kê.")
            else:
                print(f"{'Danh mục':<15} | {'Tổng chi tiêu':<18}")
                print("-" * 36)
                for row in thong_ke:
                    dm, tong_tien = row
                    print(f"{dm:<15} | {format_money(tong_tien):<18}")
                print("-" * 36)
                
        elif chon == "4":
            print("\n🗑️ XÓA KHOẢN CHI TIÊU:")
            try:
                id_xoa = int(input("Nhập ID khoản chi tiêu muốn xóa: ").strip())
                xoa_chi_tieu(id_xoa)
            except ValueError:
                print("❌ ID phải là một số nguyên hợp lệ!")
                
        elif chon == "5":
            print("👋 Tạm biệt bạn! Chúc bạn quản lý tài chính hiệu quả.")
            break
        else:
            print("⚠️ Lựa chọn không hợp lệ. Vui lòng chọn số từ 1 đến 5.")

if __name__ == "__main__":
    main()
