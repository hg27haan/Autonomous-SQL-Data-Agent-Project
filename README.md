# 🏗️ Autonomous SQL Data Agent

> **Enterprise AI Assistant for Engineering Data Analysis**  
> *Hệ thống AI phân tích dữ liệu kỹ thuật tự động, hỗ trợ SQL Server và CSV Upload.*

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red)
![Google Gemini](https://img.shields.io/badge/AI-Google%20Gemini-orange)
![SQL Server](https://img.shields.io/badge/DB-SQL%20Server-lightgrey)
![ODBC](https://img.shields.io/badge/Driver-ODBC%2017%2F18-green)

## 📖 Giới thiệu (Introduction)

Dự án này là một **AI Agent** chuyên dụng cho việc phân tích dữ liệu. Khác với các chatbot thông thường, hệ thống này kết nối trực tiếp vào Database doanh nghiệp (**Microsoft SQL Server**) hoặc dữ liệu cá nhân (**CSV**), biến ngôn ngữ tự nhiên thành hành động truy vấn dữ liệu thực tế.

Hệ thống được thiết kế theo tư duy **Stateless & Secure**, đảm bảo kết nối database chỉ được mở khi cần thiết và đóng ngay lập tức sau khi truy vấn xong.

## ✨ Tính năng nổi bật (Key Features)

*   **🔌 Multi-Source Data:** 
    *   Kết nối trực tiếp **Microsoft SQL Server** (Production).
    *   Hỗ trợ **Upload CSV** (In-memory Database) cho dữ liệu Ad-hoc.
*   **💬 Text-to-SQL (T-SQL):** AI tự động viết SQL chuẩn cú pháp Microsoft SQL Server (`TOP`, `GETDATE`,...).
*   **🛡️ Security & Stateless:** 
    *   Cơ chế **Auto-Dispose**: Tự động ngắt kết nối Database ngay sau khi lấy dữ liệu để tiết kiệm tài nguyên và bảo mật.
    *   Chặn tuyệt đối các lệnh ghi/xóa (`DROP`, `DELETE`, `UPDATE`).
*   **📊 Smart Visualization:** Tự động phát hiện loại dữ liệu để vẽ biểu đồ (Bar, Line) bằng Plotly.
*   **📥 Export Data:** Cho phép tải xuống kết quả truy vấn dưới dạng file CSV.
*   **🧠 Dynamic Schema:** AI tự động đọc cấu trúc bảng mới nhất mà không cần huấn luyện lại.

## 🛠️ Công nghệ sử dụng (Tech Stack)

*   **Core:** Python 3.11
*   **LLM Engine:** Google Gemini (Model: `gemini-flash-latest`)
*   **Database Driver:** `pyodbc` (Kết nối SQL Server qua ODBC Driver).
*   **Backend:** SQLAlchemy, Pandas.
*   **Frontend:** Streamlit, Plotly.

## 📂 Cấu trúc dự án (Project Structure)

```text
AUTONOMOUS-SQL-DATA-AGENT/
│
├── core/                   # Modules xử lý chính (Backend)
│   ├── database.py         # Quản lý kết nối (SQL Server + SQLite Memory)
│   ├── sql_generator.py    # AI: Đọc Schema & Sinh SQL (Stateless)
│   └── sql_executor.py     # Engine: Thực thi SQL & Bảo mật
│
├── scripts/                # Công cụ hỗ trợ (Utilities)
│   ├── seed_data.py        # Tạo dữ liệu giả vào SQL Server
│   └── check_models.py     # Kiểm tra model Google khả dụng
│
├── app.py                  # Giao diện Web (Streamlit)
├── main.py                 # Giao diện dòng lệnh (CLI)
├── .env                    # Cấu hình bảo mật (API Key, DB Creds)
└── requirements.txt        # Danh sách thư viện