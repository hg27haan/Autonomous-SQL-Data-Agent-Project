import pandas as pd
from sql_generator import generate_sql
from sql_executor import execute_sql

def chat_with_data(user_question):
    print(f"User: {user_question}")
    print("🤖 AI đang suy nghĩ và viết code...")
    
    # Bước 1: Text -> SQL
    sql_query = generate_sql(user_question)
    
    if not sql_query:
        print("❌ AI không thể tạo ra câu lệnh SQL.")
        return

    print(f"Generated SQL: {sql_query}")
    
    # Bước 2: SQL -> Data
    print("⚡ Đang thực thi truy vấn...")
    result = execute_sql(sql_query)
    
    # Bước 3: Hiển thị kết quả
    if isinstance(result, pd.DataFrame):
        print("\n✅ KẾT QUẢ TÌM ĐƯỢC:")
        # In đẹp hơn với to_markdown (nếu cài tabulate) hoặc to_string
        print(result.to_string(index=False))
        print(f"\n(Tìm thấy {len(result)} bản ghi)")
    else:
        print(f"\n❌ LỖI THỰC THI: {result}")

if __name__ == "__main__":
    # Vòng lặp chat liên tục
    print("=== HỆ THỐNG TRUY VẤN DỮ LIỆU KỸ THUẬT (Gõ 'exit' để thoát) ===")
    
    while True:
        question = input("\nNhập câu hỏi của bạn: ")
        if question.lower() in ['exit', 'quit']:
            break
        
        chat_with_data(question)