import os
import google.generativeai as genai
from dotenv import load_dotenv
from sqlalchemy import inspect
from core.database import init_db

# 1. Load biến môi trường & Cấu hình Google AI
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("❌ Chưa tìm thấy GOOGLE_API_KEY trong file .env")

genai.configure(api_key=api_key)

def get_schema_string(engine):
    """
    Hàm tự động quét Database để lấy tên bảng và tên cột.
    """
    inspector = inspect(engine)
    schema_lines = []
    
    for table_name in inspector.get_table_names():
        columns = inspector.get_columns(table_name)
        # Lấy tên cột và kiểu dữ liệu (VD: id (INTEGER), name (VARCHAR))
        col_desc = [f"{col['name']} ({str(col['type'])})" for col in columns]
        schema_lines.append(f"Table: {table_name}")
        schema_lines.append(f"Columns: {', '.join(col_desc)}")
        schema_lines.append("") 
        
    return "\n".join(schema_lines)

def generate_sql(question: str):
    """
    Input: Câu hỏi tiếng Việt
    Output: Câu lệnh SQL sạch
    """
    # Bước A: Lấy Schema thực tế
    engine = init_db()
    schema_text = get_schema_string(engine)
    
    # Bước B: Tạo cấu hình cho Model
    # Chúng ta dùng 'gemini-1.5-flash' vì nó nhanh và rẻ (free), code tốt.
    generation_config = {
        "temperature": 0.1,  # Thấp để AI ít "chém gió", tập trung vào code chính xác
        "top_p": 0.95,
        "max_output_tokens": 8192,
    }

    # Bước C: Thiết lập Prompt (Chỉ dẫn hệ thống)
    system_instruction = f"""
    Bạn là một chuyên gia SQL Engineer (SQLite Dialect).
    Nhiệm vụ: Chuyển câu hỏi tự nhiên thành câu lệnh SQL để truy vấn dữ liệu.

    Database Schema hiện tại:
    {schema_text}

    Quy tắc TUYỆT ĐỐI:
    1. Chỉ trả về duy nhất mã SQL. KHÔNG giải thích, KHÔNG chào hỏi.
    2. KHÔNG được dùng Markdown block (tức là không được có ```sql ở đầu).
    3. Luôn sử dụng Alias cho bảng (ví dụ: `machines m`, `maintenance_logs l`) để ngắn gọn.
    4. Chỉ tạo câu lệnh `SELECT`. Cấm các lệnh `DROP`, `DELETE`, `UPDATE`.
    """

    model = genai.GenerativeModel(
        model_name="gemini-flash-latest",
        generation_config=generation_config,
        system_instruction=system_instruction
    )

    # Bước D: Gọi AI
    try:
        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(question)
        
        sql_query = response.text.strip()
        
        # Clean code (Phòng hờ Gemini vẫn thêm markdown)
        sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
        
        return sql_query

    except Exception as e:
        print(f"❌ Lỗi khi gọi Google AI: {e}")
        return ""

# --- Phần test chạy thử ---
if __name__ == "__main__":
    # Câu hỏi test
    test_questions = [
        "Liệt kê 3 máy móc được lắp đặt gần đây nhất",
        "Kỹ sư nào sửa chữa tốn nhiều tiền nhất?"
    ]

    print("🚀 Đang khởi động Google Gemini...\n")
    
    for q in test_questions:
        print(f"User: {q}")
        sql = generate_sql(q)
        print(f"Gemini SQL: {sql}")
        print("-" * 50)