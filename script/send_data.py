# seed_data.py
import random
from faker import Faker
from sqlalchemy.orm import sessionmaker
from core.database import init_db, Machine, Technician, MaintenanceLog
from datetime import date, timedelta

# Cấu hình
fake = Faker()
NUM_MACHINES = 50
NUM_TECHS = 10
NUM_LOGS = 1000

def seed():
    print("🔄 Đang khởi tạo database và dữ liệu giả...")
    engine = init_db()
    Session = sessionmaker(bind=engine)
    session = Session()

    # 1. Tạo Machines
    machine_types = ['CNC Lathe', 'Hydraulic Press', 'Robotic Arm', 'Conveyor Belt', '3D Printer']
    locations = ['Zone A', 'Zone B', 'Warehouse', 'Assembly Line']
    
    machines = []
    for _ in range(NUM_MACHINES):
        m = Machine(
            name=f"{random.choice(machine_types)} #{random.randint(100, 999)}",
            model=fake.bothify(text='Mod-####??'),
            location=random.choice(locations),
            install_date=fake.date_between(start_date='-5y', end_date='-1y')
        )
        machines.append(m)
    session.add_all(machines)
    session.commit() # Commit để lấy ID
    print(f"✅ Đã tạo {NUM_MACHINES} máy móc.")

    # 2. Tạo Technicians
    specialties = ['Electrical', 'Mechanical', 'Software', 'Hydraulics']
    techs = []
    for _ in range(NUM_TECHS):
        t = Technician(
            name=fake.name(),
            specialty=random.choice(specialties),
            years_experience=random.randint(1, 20)
        )
        techs.append(t)
    session.add_all(techs)
    session.commit()
    print(f"✅ Đã tạo {NUM_TECHS} kỹ sư.")

    # 3. Tạo Logs (Dữ liệu quan trọng nhất để AI phân tích)
    logs = []
    machine_ids = [m.id for m in machines]
    tech_ids = [t.id for t in techs]
    issues = ['Oil leak', 'Overheating', 'Sensor failure', 'Calibration error', 'Routine check']
    
    for _ in range(NUM_LOGS):
        log = MaintenanceLog(
            machine_id=random.choice(machine_ids),
            technician_id=random.choice(tech_ids),
            date=fake.date_between(start_date='-1y', end_date='today'),
            description=random.choice(issues),
            cost=round(random.uniform(50.0, 5000.0), 2),
            status=random.choice(['Success', 'Success', 'Success', 'Pending', 'Failed']) # Tỉ lệ Success cao hơn
        )
        logs.append(log)
    session.add_all(logs)
    session.commit()
    print(f"✅ Đã tạo {NUM_LOGS} nhật ký bảo trì.")
    
    session.close()
    print("🎉 Hoàn tất seeding!")

if __name__ == "__main__":
    seed()