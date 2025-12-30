import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import timedelta

def forecast_data(df: pd.DataFrame, time_col: str, value_col: str, months=3):
    """
    Hàm dự báo đơn giản sử dụng Linear Regression.
    Input: DataFrame lịch sử (Ngày, Giá trị)
    Output: DataFrame chứa cả lịch sử + 3 tháng tương lai
    """
    # 1. Chuẩn bị dữ liệu
    df = df.sort_values(by=time_col)
    df[time_col] = pd.to_datetime(df[time_col])
    
    # Chuyển đổi ngày tháng sang dạng số (Ordinal) để máy tính hiểu
    df['date_ordinal'] = df[time_col].apply(lambda x: x.toordinal())
    
    X = df[['date_ordinal']]
    y = df[value_col]
    
    # 2. Train model (Học từ quá khứ)
    model = LinearRegression()
    model.fit(X, y)
    
    # 3. Tạo dữ liệu tương lai
    last_date = df[time_col].max()
    future_dates = []
    for i in range(1, months + 1):
        # Cộng thêm i * 30 ngày
        future_dates.append(last_date + timedelta(days=i*30))
        
    future_df = pd.DataFrame({time_col: future_dates})
    future_df['date_ordinal'] = future_df[time_col].apply(lambda x: x.toordinal())
    
    # 4. Dự báo
    future_pred = model.predict(future_df[['date_ordinal']])
    future_df[value_col] = future_pred
    future_df['Type'] = 'Forecast' # Đánh dấu là dự báo
    
    # 5. Gộp kết quả
    df['Type'] = 'History' # Đánh dấu là lịch sử
    
    # Chỉ lấy các cột cần thiết
    final_df = pd.concat([df[[time_col, value_col, 'Type']], future_df[[time_col, value_col, 'Type']]])
    
    return final_df