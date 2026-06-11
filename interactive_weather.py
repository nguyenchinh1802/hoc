# interactive_weather.py
import requests

def lay_thoi_tiet(thanh_pho):
    # Định dạng tên thành phố phù hợp với URL (thay khoảng trắng bằng dấu cộng)
    thanh_pho_url = thanh_pho.strip().replace(" ", "+")
    url = f"https://wttr.in/{thanh_pho_url}?format=j1&lang=vi"
    
    try:
        response = requests.get(url)
        
        # Nếu trang web trả về lỗi 404 (không tìm thấy thành phố)
        if response.status_code == 404:
            print(f"❌ Không tìm thấy thông tin cho '{thanh_pho}'. Hãy thử nhập tên tiếng Anh không dấu (vd: Hanoi, Paris, Tokyo).")
            return
            
        response.raise_for_status()
        data = response.json()
        
        current = data["current_condition"][0]
        nhiet_do = current["temp_C"]
        do_am = current["humidity"]
        toc_do_gio = current["windspeedKmph"]
        
        mo_ta = "Không rõ"
        if "lang_vi" in current and len(current["lang_vi"]) > 0:
            mo_ta = current["lang_vi"][0]["value"]
        elif "weatherDesc" in current and len(current["weatherDesc"]) > 0:
            mo_ta = current["weatherDesc"][0]["value"]

        print("\n======================================")
        print(f" THỜI TIẾT TẠI {thanh_pho.upper()}")
        print("======================================")
        print(f"🌡️  Nhiệt độ:    {nhiet_do}°C")
        print(f"☁️  Trạng thái:  {mo_ta}")
        print(f"💧  Độ ẩm:      {do_am}%")
        print(f"💨  Tốc độ gió:  {toc_do_gio} km/h")
        print("======================================\n")

    except Exception as e:
        print(f"❌ Đã xảy ra lỗi khi kết nối: {e}")

def main():
    print("=== CHƯƠNG TRÌNH TRA CỨU THỜI TIẾT INTERACTIVE ===")
    print("Nhập tên thành phố bằng tiếng Anh không dấu (vd: Hanoi, Saigon, London, Tokyo...)")
    print("Nhập 'thoat' hoặc 'exit' để dừng chương trình.")
    print("==================================================")
    
    while True:
        # Nhập dữ liệu từ bàn phím
        nhap_vao = input("Nhập tên thành phố: ")
        
        # Kiểm tra điều kiện thoát
        if nhap_vao.strip().lower() in ["thoat", "exit"]:
            print("Cảm ơn bạn đã sử dụng chương trình. Tạm biệt!")
            break
            
        # Kiểm tra nếu người dùng không nhập gì
        if not nhap_vao.strip():
            print("⚠️ Vui lòng nhập tên thành phố!")
            continue
            
        # Gọi hàm tra cứu
        lay_thoi_tiet(nhap_vao)

if __name__ == "__main__":
    main()
