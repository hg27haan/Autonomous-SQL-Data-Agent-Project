import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine, text

# Import core modules
from core.sql_generator import generate_sql
from core.sql_executor import execute_sql
from core.smart_agent import process_question_with_retry
from core.database import init_db

# --- CẤU HÌNH TRANG WEB ---
st.set_page_config(page_title="Engineering AI Assistant", page_icon="🤖", layout="wide")
st.title("🏗️ Engineering Data Assistant")

# --- SIDEBAR: CẤU HÌNH DỮ LIỆU ---
st.sidebar.header("📂 Nguồn Dữ Liệu")
data_source = st.sidebar.radio("Chọn nguồn dữ liệu:", ("Database Mặc định (Factory)", "Upload File CSV"))

current_engine = None

if data_source == "Upload File CSV":
    uploaded_file = st.sidebar.file_uploader("Tải lên file CSV của bạn", type=["csv"])
    if uploaded_file:
        # 1. Đọc file CSV
        df_uploaded = pd.read_csv(uploaded_file)
        st.sidebar.success(f"Đã tải lên: {df_uploaded.shape[0]} dòng")
        
        # 2. Tạo Database tạm trong RAM (In-memory SQLite)
        temp_engine = create_engine('sqlite:///:memory:')
        
        # 3. Đẩy dữ liệu CSV vào bảng tên là 'my_table'
        df_uploaded.to_sql('my_data', temp_engine, index=False, if_exists='replace')
        
        current_engine = temp_engine
        st.info("💡 Mẹo: Dữ liệu của bạn đang ở trong bảng tên là **`my_data`**.")
        with st.expander("Xem dữ liệu thô"):
            st.dataframe(df_uploaded.head())
else:
    # Dùng DB mặc định
    st.sidebar.info("Đang sử dụng dữ liệu giả lập từ `factory.db`")
    current_engine = None # Core sẽ tự load init_db()

# --- QUẢN LÝ SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "data" in message:
            st.dataframe(message["data"])
        if "chart" in message:
            st.plotly_chart(message["chart"], use_container_width=True)

# --- HÀM VẼ BIỂU ĐỒ (Giữ nguyên) ---
def auto_visualize(df):
    if df.empty or len(df) < 2: return None
    
    # 1. Logic vẽ biểu đồ Dự báo (Nếu có cột 'Type')
    if 'Type' in df.columns and 'Forecast' in df['Type'].values:
        # Tìm cột ngày và số
        date_cols = df.select_dtypes(include=['datetime']).columns
        num_cols = df.select_dtypes(include=['float', 'int']).columns
        val_col = [c for c in num_cols if c != 'date_ordinal'][0] # Loại bỏ cột phụ nếu có
        
        chart = px.line(
            df, 
            x=date_cols[0], 
            y=val_col, 
            color='Type', # Chia màu theo Lịch sử/Dự báo
            title=f"Forecast Analysis: {val_col}",
            markers=True,
            line_dash='Type' # Nét đứt cho dự báo
        )
        return chart

    # 2. Logic vẽ biểu đồ thường (Cũ)
    num_cols = df.select_dtypes(include=['float', 'int']).columns.tolist()
    cat_cols = df.select_dtypes(include=['object', 'string']).columns.tolist()
    date_cols = df.select_dtypes(include=['datetime']).columns.tolist()
    
    if len(cat_cols) >= 1 and len(num_cols) >= 1:
        return px.bar(df, x=cat_cols[0], y=num_cols[0], title=f"{num_cols[0]} by {cat_cols[0]}")
    elif len(date_cols) >= 1 and len(num_cols) >= 1:
        return px.line(df, x=date_cols[0], y=num_cols[0], title="Trend over Time")
        
    return None

# --- LOGIC CHAT ---
if prompt := st.chat_input("Hỏi gì đó về dữ liệu..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # GỌI SMART AGENT
        with st.status("🤖 AI đang xử lý...", expanded=True) as status:
            st.write("Đang phân tích và truy vấn...")
            
            # Gọi hàm xử lý có vòng lặp
            result = process_question_with_retry(prompt, engine=current_engine, max_retries=3)
            
            if isinstance(result, pd.DataFrame):
                status.update(label="Thành công!", state="complete", expanded=False)
            else:
                status.update(label="Gặp sự cố", state="error", expanded=True)

        # HIỂN THỊ KẾT QUẢ
        response_text = ""
        chart_obj = None
        
        if isinstance(result, str):
            # Trường hợp lỗi cuối cùng
            response_text = f"⚠️ {result}"
            st.error(response_text)
        
        elif isinstance(result, pd.DataFrame):
            if result.empty:
                response_text = "Truy vấn thành công nhưng không có dữ liệu."
                st.info(response_text)
            else:
                # Hiển thị SQL cuối cùng (nếu muốn debug)
                if 'final_sql' in result.attrs:
                    with st.expander("Xem câu lệnh SQL đã chạy"):
                        st.code(result.attrs['final_sql'], language="sql")

                st.dataframe(result, use_container_width=True)
                
                # Nút download
                csv_data = result.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Tải kết quả (CSV)", csv_data, "data.csv", "text/csv")
                
                chart_obj = auto_visualize(result)
                if chart_obj:
                    st.plotly_chart(chart_obj, use_container_width=True)
                
                response_text = f"Tìm thấy **{len(result)}** dòng dữ liệu."

        # Lưu lịch sử chat
        msg_data = {"role": "assistant", "content": response_text}
        if isinstance(result, pd.DataFrame) and not result.empty:
            msg_data["data"] = result
        if chart_obj:
            msg_data["chart"] = chart_obj
        st.session_state.messages.append(msg_data)