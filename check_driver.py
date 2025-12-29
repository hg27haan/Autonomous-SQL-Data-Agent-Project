# check_driver.py
import pyodbc
print("Các driver SQL đang có trên máy:")
for driver in pyodbc.drivers():
    print(f" - {driver}")