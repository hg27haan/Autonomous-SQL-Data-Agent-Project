import pandas as pd
import re
from sqlalchemy import text
from models import init_db

def is_safe_sql(sql_query: str) -> bool:
    """
    Hàm kiểm tra bảo mật đơn giản (Rule-based).
    Chỉ cho phép câu lệnh SELECT. Chặn DROP, DELETE, INSERT, UPDATE.
    """
    # Chuyển về chữ hoa để check cho dễ
    sql_upper = sql_query.upper()
    
    # Các từ khóa cấm (Forbidden keywords)
    forbidden_keywords = [
        "DROP TABLE", "DELETE FROM", "INSERT INTO", 
        "UPDATE ", "ALTER TABLE", "TRUNCATE"
    ]
    
    for keyword in forbidden_keywords:
        if keyword in sql_upper:
            print(f"⚠️ CẢNH BÁO: Phát hiện từ khóa nguy hiểm '{keyword}'")
            return False
            
    return True

def execute_sql(sql_query: str):
    """
    Input: Câu lệnh SQL (String)
    Output: 
        - Nếu thành công: Trả về Pandas DataFrame
        - Nếu thất bại: Trả về chuỗi thông báo lỗi (String)
    """
    # 1. Check an toàn trước khi kết nối DB
    if not is_safe_sql(sql_query):
        return "ERROR: Câu lệnh SQL bị từ chối vì lý do bảo mật."
    
    # 2. Kết nối DB
    engine = init_db()
    
    try:
        # Sử dụng pandas để đọc SQL. Đây là cách clean nhất cho Data Project.
        # Dùng connection context để tự động đóng kết nối
        with engine.connect() as connection:
            df = pd.read_sql(text(sql_query), connection)
            
        # Kiểm tra nếu kết quả rỗng
        if df.empty:
            return "Query chạy thành công nhưng không tìm thấy dữ liệu nào."
            
        return df
        
    except Exception as e:
        # Bắt lỗi cú pháp SQL (Ví dụ: AI bịa ra tên cột không tồn tại)
        error_msg = str(e)
        # Rút gọn lỗi cho dễ đọc (Lấy phần gốc từ SQLite)
        if "(sqlite3.OperationalError)" in error_msg:
            return f"SQL Error: {error_msg.split('(sqlite3.OperationalError)')[1].strip()}"
        return f"System Error: {error_msg}"

# --- Test Unit ---
if __name__ == "__main__":
    # Test 1: Query an toàn
    print("--- Test 1: Safe Query ---")
    safe_sql = "SELECT * FROM machines LIMIT 2"
    result = execute_sql(safe_sql)
    print(result)
    print("\n")

    # Test 2: Query nguy hiểm (Giả lập tấn công)
    print("--- Test 2: Unsafe Query ---")
    unsafe_sql = "DROP TABLE technicians"
    result = execute_sql(unsafe_sql)
    print(result)
    print("\n")
    
    # Test 3: Query sai cú pháp
    print("--- Test 3: Invalid Syntax ---")
    broken_sql = "SELECT ten_may FROM machines" # Cột 'ten_may' không tồn tại
    result = execute_sql(broken_sql)
    print(result)