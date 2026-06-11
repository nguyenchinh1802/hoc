# vnexpress_scraper_save.py
import requests
import csv
from bs4 import BeautifulSoup

# 1. Định cấu hình
url = "https://vnexpress.net"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

print(f"🌐 Đang gửi yêu cầu truy cập trang web: {url}...")

try:
    # 2. Lấy HTML của trang web
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    # 3. Phân tích cú pháp HTML
    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.find_all("h3", class_="title-news")
    
    tin_tuc_list = []
    
    # 4. Trích xuất dữ liệu
    for idx, article in enumerate(articles[:15], 1):
        a_tag = article.find("a")
        if a_tag:
            title = a_tag.get_text(strip=True)
            link = a_tag.get("href")
            tin_tuc_list.append({"stt": idx, "tieu_de": title, "lien_ket": link})

    # --- LƯU FILE 1: FILE VĂN BẢN THUẦN (.txt) ---
    txt_filename = "vnexpress_news.txt"
    print(f"💾 Đang ghi dữ liệu vào file văn bản: {txt_filename}...")
    
    with open(txt_filename, "w", encoding="utf-8") as txt_file:
        txt_file.write("=======================================\n")
        txt_file.write(" DANH SÁCH 15 TIN MỚI NHẤT TRÊN VNEXPRESS\n")
        txt_file.write("=======================================\n\n")
        for item in tin_tuc_list:
            txt_file.write(f"{item['stt']:02d}. 📰 {item['tieu_de']}\n")
            txt_file.write(f"    🔗 Link: {item['lien_ket']}\n")
            txt_file.write("-" * 50 + "\n")

    # --- LƯU FILE 2: FILE CSV (Mở được trực tiếp bằng Excel - .csv) ---
    csv_filename = "vnexpress_news.csv"
    print(f"💾 Đang ghi dữ liệu vào file CSV: {csv_filename}...")
    
    with open(csv_filename, "w", newline="", encoding="utf-8-sig") as csv_file:
        # Sử dụng utf-8-sig để Excel nhận dạng đúng tiếng Việt không bị lỗi font
        fieldnames = ["STT", "Tiêu đề", "Liên kết"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        
        # Ghi dòng tiêu đề cột
        writer.writeheader()
        
        # Ghi các dòng dữ liệu
        for item in tin_tuc_list:
            writer.writerow({
                "STT": item["stt"],
                "Tiêu đề": item["tieu_de"],
                "Liên kết": item["lien_ket"]
            })

    print("\n✅ Hoàn thành! Đã lưu trữ tin tức thành công vào 2 tệp tin:")
    print(f"   1. File văn bản: {txt_filename}")
    print(f"   2. File Excel/CSV: {csv_filename}\n")

except Exception as e:
    print(f"❌ Đã xảy ra lỗi: {e}")
