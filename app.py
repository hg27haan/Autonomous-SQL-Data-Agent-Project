import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine, text

# Import core modules
from core.sql_generator import generate_sql
from core.sql_executor import execute_sql
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
    num_cols = df.select_dtypes(include=['float', 'int']).columns.tolist()
    cat_cols = df.select_dtypes(include=['object', 'string']).columns.tolist()
    date_cols = df.select_dtypes(include=['datetime']).columns.tolist()
    chart = None
    if len(cat_cols) >= 1 and len(num_cols) >= 1:
        chart = px.bar(df, x=cat_cols[0], y=num_cols[0], title=f"{num_cols[0]} by {cat_cols[0]}", template="plotly_white", color=num_cols[0])
    elif len(date_cols) >= 1 and len(num_cols) >= 1:
        chart = px.line(df, x=date_cols[0], y=num_cols[0], title="Trend over Time")
    return chart

# --- LOGIC CHAT ---
if prompt := st.chat_input("Hỏi gì đó về dữ liệu..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # Gọi hàm generate_sql với engine hiện tại (Mặc định hoặc CSV Upload)
        sql_query = generate_sql(prompt, engine=current_engine)
        
        if not sql_query:
            st.error("Không thể tạo SQL.")
            st.stop()
            
        st.code(sql_query, language="sql")
        
        # Thực thi SQL với engine hiện tại
        result = execute_sql(sql_query, engine=current_engine)

        response_text = ""
        chart_obj = None
        
        if isinstance(result, str):
            response_text = f"⚠️ Lỗi: {result}"
            st.markdown(response_text)
        elif isinstance(result, pd.DataFrame):
            if result.empty:
                response_text = "Không tìm thấy dữ liệu."
                st.markdown(response_text)
            else:
                st.dataframe(result, use_container_width=True)
                
                # --- TÍNH NĂNG MỚI: DOWNLOAD KẾT QUẢ ---
                csv_data = result.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Tải kết quả (CSV)",
                    data=csv_data,
                    file_name="query_result.csv",
                    mime="text/csv",
                )
                
                chart_obj = auto_visualize(result)
                if chart_obj:
                    st.plotly_chart(chart_obj, use_container_width=True)
                
                response_text = f"Tìm thấy **{len(result)}** dòng dữ liệu."
                st.markdown(response_text)

        msg_data = {"role": "assistant", "content": response_text}
        if isinstance(result, pd.DataFrame) and not result.empty:
            msg_data["data"] = result
        if chart_obj:
            msg_data["chart"] = chart_obj
        st.session_state.messages.append(msg_data)