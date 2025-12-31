# 🏗️ Autonomous SQL Data Agent

> **Enterprise AI Assistant for Engineering Data Analysis**  
> *Hệ thống AI phân tích dữ liệu kỹ thuật tự động, hỗ trợ SQL Server, Self-Healing Code và Dự báo tương lai.*

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red)
![Google Gemini](https://img.shields.io/badge/AI-Google%20Gemini-orange)
![SQL Server](https://img.shields.io/badge/DB-SQL%20Server-lightgrey)
![Scikit-learn](https://img.shields.io/badge/ML-Scikit--learn-yellow)

## 📖 Giới thiệu (Introduction)

Dự án này là một **AI Agent** chuyên dụng cho việc phân tích dữ liệu kỹ thuật. Hệ thống kết nối trực tiếp vào **Microsoft SQL Server** (Production) hoặc dữ liệu **CSV**, biến ngôn ngữ tự nhiên thành hành động truy vấn.

Đặc biệt, hệ thống sở hữu khả năng **Self-Healing** khi viết code sai và khả năng **Dự báo (Forecasting)** xu hướng tương lai dựa trên dữ liệu lịch sử.

## ✨ Tính năng nổi bật (Key Features)

### 🧠 Trí tuệ nhân tạo & Tự động hóa
*   **🤖 AI Self-Correction:** Cơ chế vòng lặp thông minh. Nếu AI viết SQL sai cú pháp, hệ thống tự động gửi thông báo lỗi ngược lại cho AI để tự sửa chữa (Retry Loop) mà không cần người dùng can thiệp.
*   **🔮 Predictive Analytics:** Tự động phát hiện nhu cầu "dự báo" của người dùng. Hệ thống sẽ lấy dữ liệu chuỗi thời gian từ SQL Server và áp dụng thuật toán **Linear Regression** để vẽ biểu đồ dự đoán xu hướng tương lai.
*   **💬 Text-to-SQL (T-SQL):** Chuyển đổi câu hỏi tự nhiên thành SQL chuẩn Microsoft (`TOP`, `GETDATE`, `DATEPART`...).

### 🔌 Kết nối & Dữ liệu
*   **Multi-Source:** Hỗ trợ kết nối **SQL Server** và Upload **CSV** (In-memory Database).
*   **Stateless Connection:** Cơ chế tự động ngắt kết nối (`Auto-Dispose`) ngay sau khi truy vấn để bảo mật và tiết kiệm tài nguyên server.
*   **Security:** Chặn tuyệt đối các lệnh ghi/xóa (`DROP`, `DELETE`, `UPDATE`).

### 📊 Trực quan hóa
*   **Smart Visualization:** Tự động vẽ biểu đồ Bar/Line bằng Plotly.
*   **Forecast Chart:** Biểu đồ đường phân biệt rõ vùng dữ liệu Quá khứ (nét liền) và Dự báo (nét đứt).
*   **Export:** Tải xuống kết quả phân tích dưới dạng CSV.

## 🛠️ Công nghệ sử dụng (Tech Stack)

*   **Core:** Python 3.11
*   **LLM Engine:** Google Gemini (Model: `gemini-flash-latest`)
*   **Machine Learning:** Scikit-learn (Linear Regression)
*   **Database Driver:** `pyodbc` (ODBC Driver 18 for SQL Server)
*   **Backend:** SQLAlchemy, Pandas
*   **Frontend:** Streamlit, Plotly

## 📂 Cấu trúc dự án (Project Structure)

```text
AUTONOMOUS-SQL-DATA-AGENT/
│
├── core/                   # Modules xử lý chính (Backend)
│   ├── database.py         # Quản lý kết nối (SQL Server + SQLite Memory)
│   ├── sql_generator.py    # AI: Sinh SQL & Hàm sửa lỗi (Fixer)
│   ├── sql_executor.py     # Engine: Thực thi SQL & Bảo mật
│   ├── smart_agent.py      # Brain: Điều phối vòng lặp & Logic Router
│   └── forecaster.py       # ML: Thuật toán dự báo Linear Regression
│
├── scripts/                # Công cụ hỗ trợ
│   ├── seed_data.py        # Tạo dữ liệu giả vào SQL Server
│   └── check_models.py     # Kiểm tra model Google
│   └── test query.py       # Kiểm tra kết nối với database sql lite
│
├── app.py                  # Giao diện Web (Streamlit)
├── .env                    # Cấu hình bảo mật
└── requirements.txt        # Danh sách thư viện