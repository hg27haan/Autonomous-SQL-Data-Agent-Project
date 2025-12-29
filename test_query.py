# test_query.py
import pandas as pd
from sqlalchemy import create_engine

# Kết nối DB
engine = create_engine('sqlite:///factory.db')

# Thử một câu query phức tạp mà sau này AI sẽ phải tự viết
sql = """
SELECT 
    t.name as Technician, 
    COUNT(m.id) as Repair_Count, 
    SUM(m.cost) as Total_Cost
FROM maintenance_logs m
JOIN technicians t ON m.technician_id = t.id
GROUP BY t.name
ORDER BY Total_Cost DESC
LIMIT 5;
"""

print("📊 Top 5 Kỹ sư tiêu tốn chi phí sửa chữa nhiều nhất:")
df = pd.read_sql(sql, engine)
print(df)