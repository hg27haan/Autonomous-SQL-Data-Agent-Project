import pandas as pd
from core.sql_generator import generate_sql, fix_sql_query
from core.sql_executor import execute_sql
from core.forecaster import forecast_data # Import mới

def process_question_with_retry(question: str, engine=None, max_retries=3):
    
    # --- LOGIC ROUTER: PHÁT HIỆN DỰ BÁO ---
    is_forecasting = False
    keywords = ["dự báo", "tương lai", "forecast", "xu hướng", "sắp tới"]
    if any(k in question.lower() for k in keywords):
        is_forecasting = True
        print("🔮 Phát hiện yêu cầu DỰ BÁO. Đang chuyển mode...")
        
        # PROMPT ENGINEERING KỸ THUẬT CAO:
        # Biến câu hỏi dự báo thành câu lệnh lấy dữ liệu lịch sử để train
        # VD: "Dự báo chi phí tháng sau" -> "Lấy tổng chi phí theo từng tháng trong quá khứ"
        question = f"""
        User muốn: "{question}".
        Để dự báo được, tôi cần dữ liệu lịch sử.
        Hãy viết SQL Server query để lấy dữ liệu lịch sử theo thời gian (Group by Month hoặc Day).
        Cần 2 cột: Time (Date) và Value (Number).
        Sắp xếp theo thời gian tăng dần.
        """

    # --- LOGIC CŨ (VÒNG LẶP SỬA LỖI) ---
    current_sql = ""
    last_error = ""
    result_df = None
    
    for attempt in range(1, max_retries + 1):
        # ... (Code vòng lặp cũ giữ nguyên) ...
        # ... (Copy đoạn code sinh SQL và Execute ở Level 2 vào đây) ...
        
        # Tạm viết lại đoạn ngắn gọn để bạn dễ hình dung vị trí chèn:
        if attempt == 1:
            current_sql = generate_sql(question, engine)
        else:
            current_sql = fix_sql_query(question, current_sql, last_error, engine)
            
        if not current_sql: return "Không thể tạo SQL."
        
        res = execute_sql(current_sql, engine)
        
        if isinstance(res, pd.DataFrame):
            result_df = res
            result_df.attrs['final_sql'] = current_sql
            break # Thoát vòng lặp nếu thành công
        else:
            last_error = res
            
    # --- LOGIC XỬ LÝ KẾT QUẢ ---
    if isinstance(result_df, pd.DataFrame) and not result_df.empty:
        # Nếu là Mode Dự báo, ta chạy thêm thuật toán Python
        if is_forecasting:
            try:
                # Tự động tìm cột ngày và cột số
                date_cols = result_df.select_dtypes(include=['datetime']).columns
                num_cols = result_df.select_dtypes(include=['number']).columns
                
                if len(date_cols) > 0 and len(num_cols) > 0:
                    print("📈 Đang chạy thuật toán Linear Regression...")
                    # Gọi module forecaster
                    forecast_df = forecast_data(result_df, date_cols[0], num_cols[0])
                    return forecast_df
                else:
                    return "Không tìm thấy cột Ngày/Tháng để dự báo. SQL trả về chưa đúng định dạng time-series."
            except Exception as e:
                return f"Lỗi khi tính toán dự báo: {str(e)}"
        
        return result_df

    return f"Thất bại sau {max_retries} lần thử. Lỗi: {last_error}"