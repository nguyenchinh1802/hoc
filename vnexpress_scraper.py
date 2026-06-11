# vnexpress_scraper.py
import requests
from bs4 import BeautifulSoup

# 1. Địa chỉ trang web cần cào dữ liệu
url = "https://vnexpress.net"

# 2. Giả lập trình duyệt (User-Agent) để tránh bị máy chủ chặn truy cập
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

print(f"🌐 Đang gửi yêu cầu truy cập trang web: {url}...")

try:
    # 3. Gửi yêu cầu lấy mã nguồn HTML của trang web
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Đảm bảo kết nối thành công (Status 200 OK)
    
    # 4. Dùng BeautifulSoup để phân tích mã HTML
    soup = BeautifulSoup(response.text, "html.parser")
    
    # 5. Tìm tất cả các thẻ <h3> có thuộc tính class là "title-news"
    # Đây là nơi VnExpress đặt các tiêu đề tin bài
    articles = soup.find_all("h3", class_="title-news")
    
    print(f"\n🔥 Tìm thấy {len(articles)} tin bài mới nhất trên VnExpress:")
    print("=======================================================================")
    
    # 6. Vòng lặp in ra tiêu đề và link của 15 tin bài đầu tiên
    for idx, article in enumerate(articles[:15], 1):
        a_tag = article.find("a")  # Tìm thẻ <a> chứa liên kết bên trong <h3>
        if a_tag:
            title = a_tag.get_text(strip=True)  # Lấy phần chữ (tiêu đề)
            link = a_tag.get("href")           # Lấy thuộc tính href (đường dẫn liên kết)
            
            print(f"{idx:02d}. 📰 {title}")
            print(f"    🔗 Liên kết: {link}")
            print("-" * 71)

except Exception as e:
    print(f"❌ Đã xảy ra lỗi khi cào dữ liệu: {e}")
