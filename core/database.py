# core/database.py
import os
import urllib
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from dotenv import load_dotenv

# Load biến môi trường
load_dotenv()

Base = declarative_base()

class Machine(Base):
    __tablename__ = 'machines'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False) # SQL Server cần độ dài String cụ thể
    model = Column(String(255))
    location = Column(String(255))
    install_date = Column(Date)
    logs = relationship("MaintenanceLog", back_populates="machine")

class Technician(Base):
    __tablename__ = 'technicians'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    specialty = Column(String(255))
    years_experience = Column(Integer)
    logs = relationship("MaintenanceLog", back_populates="technician")

class MaintenanceLog(Base):
    __tablename__ = 'maintenance_logs'
    id = Column(Integer, primary_key=True)
    machine_id = Column(Integer, ForeignKey('machines.id'))
    technician_id = Column(Integer, ForeignKey('technicians.id'))
    date = Column(Date)
    description = Column(String(500))
    cost = Column(Float)
    status = Column(String(50))
    machine = relationship("Machine", back_populates="logs")
    technician = relationship("Technician", back_populates="logs")


def init_db(db_name=None):
    """
    Hàm kết nối Database linh hoạt (SQL Server hoặc SQLite)
    """
    # 1. Lấy thông tin từ .env
    server = os.getenv("DB_SERVER")
    database = os.getenv("DB_NAME")
    username = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    driver = os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server")

    connection_string = ""

    # 2. Kiểm tra: Nếu có đủ thông tin thì dùng SQL Server
    if server and database and username and password:
        # Mã hóa password để tránh lỗi ký tự đặc biệt (@, /...)
        params = urllib.parse.quote_plus(
            f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};UID={username};PWD={password}; TrustServerCertificate=yes"
        )
        connection_string = f"mssql+pyodbc:///?odbc_connect={params}"
        print(f"🔗 Đang kết nối tới SQL Server: {server}/{database}")
    
    else:
        # Fallback về SQLite nếu không cấu hình .env
        if not db_name: db_name = 'factory.db'
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path = os.path.join(base_dir, db_name)
        connection_string = f'sqlite:///{db_path}'
        print("🔗 Đang kết nối tới SQLite (Local)")

    # 3. Tạo Engine
    engine = create_engine(connection_string)
    
    # Tạo bảng nếu chưa có
    Base.metadata.create_all(engine)
    
    return engine