# models.py
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

# Khởi tạo Base model
Base = declarative_base()

class Machine(Base):
    __tablename__ = 'machines'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)        # VD: Máy tiện CNC-01
    model = Column(String)                       # VD: Siemens X500
    location = Column(String)                    # VD: Zone A
    install_date = Column(Date)
    
    # Quan hệ ngược để truy vấn dễ dàng
    logs = relationship("MaintenanceLog", back_populates="machine")

class Technician(Base):
    __tablename__ = 'technicians'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)        # VD: Nguyen Van A
    specialty = Column(String)                   # VD: Điện, Cơ khí
    years_experience = Column(Integer)

    logs = relationship("MaintenanceLog", back_populates="technician")

class MaintenanceLog(Base):
    __tablename__ = 'maintenance_logs'
    
    id = Column(Integer, primary_key=True)
    machine_id = Column(Integer, ForeignKey('machines.id'))
    technician_id = Column(Integer, ForeignKey('technicians.id'))
    date = Column(Date)
    description = Column(String)                 # VD: Thay dầu, Sửa mạch
    cost = Column(Float)                         # Chi phí sửa chữa
    status = Column(String)                      # Success, Pending, Failed

    # Thiết lập quan hệ
    machine = relationship("Machine", back_populates="logs")
    technician = relationship("Technician", back_populates="logs")

# Hàm khởi tạo DB
def init_db(db_name='factory.db'):
    engine = create_engine(f'sqlite:///{db_name}')
    Base.metadata.create_all(engine)
    return engine