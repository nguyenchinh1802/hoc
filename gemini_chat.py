# gemini_chat.py
import os
import google.generativeai as genai

# 1. Lấy API Key từ biến môi trường hoặc nhập thủ công
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    print("🔑 Không tìm thấy biến môi trường GEMINI_API_KEY.")
    api_key = input("👉 Vui lòng nhập API Key Gemini của bạn: ").strip()

if not api_key:
    print("❌ Lỗi: Cần có API Key để chương trình hoạt động!")
    exit(1)

# 2. Cấu hình SDK Gemini
genai.configure(api_key=api_key)

# 3. Khởi tạo mô hình Gemini (Sử dụng model gemini-1.5-flash nhanh và miễn phí)
print("⌛ Đang khởi tạo mô hình AI...")
try:
    model = genai.GenerativeModel("gemini-1.5-flash")
    # Khởi tạo phiên trò chuyện để lưu lại lịch sử hội thoại
    chat = model.start_chat(history=[])
except Exception as e:
    print(f"❌ Lỗi cấu hình mô hình: {e}")
    exit(1)

print("\n🤖 Trợ lý AI Gemini đã sẵn sàng! Hãy bắt đầu trò chuyện.")
print("💡 Gõ 'thoat' hoặc 'exit' để dừng chương trình.")
print("================================================================")

# 4. Vòng lặp trò chuyện tương tác
while True:
    try:
        user_message = input("\nBạn: ").strip()
        
        # Bỏ qua nếu người dùng nhấn Enter mà không gõ gì
        if not user_message:
            continue
            
        # Kiểm tra lệnh thoát
        if user_message.lower() in ["exit", "thoat"]:
            print("🤖 Tạm biệt! Hẹn gặp lại bạn lần sau.")
            break
            
        print("🤖 Gemini đang suy nghĩ...")
        
        # Gửi tin nhắn và nhận phản hồi (SDK tự động lưu lịch sử trong đối tượng chat)
        response = chat.send_message(user_message)
        
        print("\n----------------------------------------------------------------")
        print(f"🤖 Gemini: {response.text}")
        print("----------------------------------------------------------------")
        
    except Exception as e:
        print(f"❌ Đã xảy ra lỗi trong cuộc trò chuyện: {e}")
