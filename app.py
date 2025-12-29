import streamlit as st
import pandas as pd
import plotly.express as px
import time

# Import các module bạn đã viết ở các giai đoạn trước
from core.sql_generator import generate_sql
from core.sql_executor import execute_sql
from core.database import init_db

# --- CẤU HÌNH TRANG WEB ---
st.set_page_config(
    page_title="Engineering AI Assistant",
    page_icon="🤖",
    layout="wide" # Giao diện rộng để hiển thị bảng to
)

st.title("🏗️ Engineering Data Assistant")
st.markdown("*Hỏi đáp dữ liệu kỹ thuật, tự động truy vấn và trực quan hóa.*")

# --- QUẢN LÝ SESSION STATE (Lưu lịch sử chat) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Hiển thị lịch sử chat cũ
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        # Nếu tin nhắn cũ có kèm dữ liệu (dataframe), hiển thị lại
        if "data" in message:
            st.dataframe(message["data"])
        if "chart" in message:
            st.plotly_chart(message["chart"], use_container_width=True)

# --- HÀM VẼ BIỂU ĐỒ THÔNG MINH (AUTO-PLOT) ---
def auto_visualize(df):
    """
    Hàm này tự động phân tích DataFrame. 
    Nếu thấy có cột Số và cột Chữ -> Vẽ biểu đồ cột.
    Nếu thấy có cột Thời gian -> Vẽ biểu đồ đường.
    """
    if df.empty or len(df) < 2:
        return None

    # Tìm các cột số và cột chữ
    num_cols = df.select_dtypes(include=['float', 'int']).columns.tolist()
    cat_cols = df.select_dtypes(include=['object', 'string']).columns.tolist()
    date_cols = df.select_dtypes(include=['datetime']).columns.tolist()

    chart = None
    
    # Logic vẽ biểu đồ đơn giản
    if len(cat_cols) >= 1 and len(num_cols) >= 1:
        # Biểu đồ cột: Trục X là tên (Category), Trục Y là số (Value)
        chart = px.bar(
            df, x=cat_cols[0], y=num_cols[0], 
            title=f"{num_cols[0]} by {cat_cols[0]}",
            template="plotly_white",
            color=num_cols[0]
        )
    elif len(date_cols) >= 1 and len(num_cols) >= 1:
        # Biểu đồ đường: Trục X là thời gian
        chart = px.line(df, x=date_cols[0], y=num_cols[0], title="Trend over Time")
    
    return chart

# --- LOGIC CHÍNH KHI USER NHẬP LIỆU ---
if prompt := st.chat_input("Hỏi gì đó về dữ liệu máy móc, bảo trì..."):
    # 1. Hiển thị câu hỏi của User
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Xử lý của AI
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # Bước A: Text -> SQL
        with st.status("🤖 Đang suy nghĩ...", expanded=True) as status:
            st.write("🔍 Đang phân tích schema...")
            sql_query = generate_sql(prompt)
            
            if not sql_query:
                st.error("Không thể tạo câu lệnh SQL.")
                status.update(label="Thất bại", state="error")
                st.stop()
            
            st.write("📝 Generated SQL:")
            st.code(sql_query, language="sql")
            
            # Bước B: SQL -> Data
            st.write("⚡ Đang truy vấn Database...")
            result = execute_sql(sql_query)
            status.update(label="Hoàn tất!", state="complete", expanded=False)

        # Bước C: Xử lý kết quả trả về
        response_text = ""
        chart_obj = None
        
        if isinstance(result, str): # Trường hợp lỗi (execute_sql trả về string lỗi)
            response_text = f"⚠️ Có lỗi xảy ra: {result}"
            st.markdown(response_text)
            
        elif isinstance(result, pd.DataFrame):
            if result.empty:
                response_text = "Truy vấn thành công nhưng không tìm thấy dữ liệu nào."
                st.markdown(response_text)
            else:
                # Hiển thị bảng dữ liệu
                st.dataframe(result, use_container_width=True)
                
                # Logic Visualization (Giai đoạn 5)
                chart_obj = auto_visualize(result)
                if chart_obj:
                    st.plotly_chart(chart_obj, use_container_width=True)
                
                # Logic Agent giải thích (Giả lập logic Phase 4)
                # Ở đây mình làm đơn giản: Đếm số dòng. 
                # Nếu bạn đã có hàm `explain_data(df)` ở Phase 4, hãy gọi nó ở đây.
                response_text = f"Tôi tìm thấy **{len(result)}** kết quả phù hợp với câu hỏi của bạn."
                st.markdown(response_text)

        # 3. Lưu lại lịch sử để hiển thị lần sau
        msg_data = {"role": "assistant", "content": response_text}
        if isinstance(result, pd.DataFrame) and not result.empty:
            msg_data["data"] = result
        if chart_obj:
            msg_data["chart"] = chart_obj
            
        st.session_state.messages.append(msg_data)