# weather.py
import requests

# 1. Định nghĩa thành phố cần lấy thời tiết
city = "Hanoi"

# Sử dụng API của wttr.in hỗ trợ định dạng JSON và ngôn ngữ Tiếng Việt (lang=vi)
url = f"https://wttr.in/{city}?format=j1&lang=vi"

print(f"Đang tải thông tin thời tiết cho {city} từ internet...")

try:
    # 2. Gửi yêu cầu HTTP GET
    response = requests.get(url)
    response.raise_for_status()  # Kiểm tra lỗi kết nối
    
    # 3. Phân tích cú pháp JSON trả về
    data = response.json()
    
    # 4. Trích xuất thông tin cần thiết từ Dictionary
    current = data["current_condition"][0]
    nhiet_do = current["temp_C"]
    do_am = current["humidity"]
    toc_do_gio = current["windspeedKmph"]
    
    # Lấy mô tả thời tiết bằng tiếng Việt
    mo_ta = "Không rõ"
    if "lang_vi" in current and len(current["lang_vi"]) > 0:
        mo_ta = current["lang_vi"][0]["value"]
    elif "weatherDesc" in current and len(current["weatherDesc"]) > 0:
        mo_ta = current["weatherDesc"][0]["value"]

    # 5. In kết quả đẹp mắt ra màn hình
    print("\n======================================")
    print(f" THỜI TIẾT TẠI {city.upper()} HÔM NAY")
    print("======================================")
    print(f"🌡️  Nhiệt độ:    {nhiet_do}°C")
    print(f"☁️  Trạng thái:  {mo_ta}")
    print(f"💧  Độ ẩm:      {do_am}%")
    print(f"💨  Tốc độ gió:  {toc_do_gio} km/h")
    print("======================================\n")

except Exception as e:
    print(f"❌ Đã xảy ra lỗi khi lấy dữ liệu: {e}")
