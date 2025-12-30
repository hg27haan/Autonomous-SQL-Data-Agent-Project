# core/smart_agent.py
import pandas as pd
from core.sql_generator import generate_sql, fix_sql_query
from core.sql_executor import execute_sql

def process_question_with_retry(question: str, engine=None, max_retries=3):
    """
    Hàm xử lý câu hỏi thông minh với cơ chế tự sửa lỗi (Self-Correction).
    """
    current_sql = ""
    last_error = ""
    
    # --- VÒNG LẶP SỬA LỖI ---
    for attempt in range(1, max_retries + 1):
        print(f"🔄 Attempt {attempt}/{max_retries}...")
        
        # Bước 1: Sinh SQL
        if attempt == 1:
            # Lần đầu: Sinh SQL từ câu hỏi
            current_sql = generate_sql(question, engine)
        else:
            # Các lần sau: Sửa SQL dựa trên lỗi cũ
            print("   🛠️ AI đang tự sửa code...")
            current_sql = fix_sql_query(question, current_sql, last_error, engine)
            
        if not current_sql:
            return "Không thể tạo câu lệnh SQL."

        # Bước 2: Thực thi SQL
        result = execute_sql(current_sql, engine)
        
        # Bước 3: Kiểm tra kết quả
        if isinstance(result, pd.DataFrame):
            # Thành công! Trả về luôn
            # Gắn thêm thuộc tính để UI biết đây là SQL cuối cùng
            result.attrs['final_sql'] = current_sql 
            return result
        else:
            # Thất bại (result là chuỗi báo lỗi)
            last_error = result
            print(f"   ❌ Lỗi: {last_error}")
            # Tiếp tục vòng lặp để sửa...

    # Nếu hết vòng lặp mà vẫn lỗi
    return f"Đã thử {max_retries} lần nhưng vẫn thất bại. Lỗi cuối cùng: {last_error}"