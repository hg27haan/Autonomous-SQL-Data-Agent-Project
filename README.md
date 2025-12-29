# 🏗️ Autonomous SQL Data Agent

> **AI Assistant for Engineering Data Analysis**  
> *Biến câu hỏi tự nhiên thành truy vấn SQL và biểu đồ trực quan.*

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red)
![Google Gemini](https://img.shields.io/badge/AI-Google%20Gemini-orange)
![SQLAlchemy](https://img.shields.io/badge/ORM-SQLAlchemy-green)

## 📖 Giới thiệu (Introduction)

Dự án này là một **AI Agent** có khả năng tự động hóa quy trình phân tích dữ liệu cho ngành kỹ thuật. Thay vì phải viết các câu lệnh SQL phức tạp, người dùng (kỹ sư, quản lý) chỉ cần đặt câu hỏi bằng tiếng Việt/Anh. Hệ thống sẽ tự động:

1.  Hiểu cấu trúc Database (Schema).
2.  Viết câu lệnh SQL tương ứng.
3.  Thực thi truy vấn an toàn.
4.  Trực quan hóa kết quả bằng bảng và biểu đồ tương tác.

Dự án được xây dựng để luyện tập tư duy **System Design**, **Prompt Engineering** và **Full-stack AI Application**.

## ✨ Tính năng chính (Key Features)

*   **💬 Natural Language to SQL:** Chuyển đổi câu hỏi tự nhiên ("Máy nào hay hỏng nhất?") thành SQL chuẩn xác.
*   **🛡️ Secure Execution:** Cơ chế bảo vệ, chỉ cho phép truy vấn (`SELECT`), chặn các lệnh phá hoại (`DROP`, `DELETE`).
*   **📊 Auto-Visualization:** Tự động phát hiện dữ liệu để vẽ biểu đồ phù hợp (Bar chart, Line chart) sử dụng Plotly.
*   **🧠 Dynamic Schema Awareness:** AI tự động đọc cấu trúc bảng, không cần train lại model khi Database thay đổi.
*   **💻 Modern UI:** Giao diện Chatbot thân thiện xây dựng bằng Streamlit.

## 🛠️ Công nghệ sử dụng (Tech Stack)

*   **Core:** Python 3.11
*   **LLM Engine:** Google Gemini (Model: `gemini-flash-latest`)
*   **Backend:** SQLAlchemy, Pandas
*   **Frontend:** Streamlit, Plotly
*   **Database:** SQLite (Dễ dàng mở rộng sang PostgreSQL)

## 📂 Cấu trúc dự án (Project Structure)

Dự án được tổ chức theo mô hình Module hóa (Clean Architecture):

```text
AUTONOMOUS-SQL-DATA-AGENT/
│
├── core/                   # Xử lý Logic chính (Backend)
│   ├── database.py         # Quản lý kết nối & Schema
│   ├── sql.generator.py        # Module kết nối AI để sinh SQL
│   └── sql.executor.py         # Module thực thi SQL & Bảo mật
│
├── scripts/                # Các công cụ hỗ trợ (Utilities)
│   ├── seed_data.py        # Tạo dữ liệu giả lập (Machines, Logs...)
│   └── check_models.py     # Kiểm tra model Google khả dụng
│
├── app.py                  # Giao diện Web (Streamlit Entry point)
├── main.py                 # Giao diện Console (CLI Entry point)
├── factory.db              # SQLite Database
├── .env                    # Chứa API Key bảo mật
└── requirements.txt        # Danh sách thư viện