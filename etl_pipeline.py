import requests
import pandas as pd
from sqlalchemy import create_engine

# 1. Extract
print("Đang lấy dữ liệu từ API...")
raw_data = requests.get("https://fakestoreapi.com/carts").json()

# 2. Transform: Bóc tách mảng lồng nhau
df_carts = pd.json_normalize(
    raw_data,
    record_path=['products'],
    meta=['id', 'userId', 'date'],
    meta_prefix='cart_'
)

# Chuẩn hóa tên cột và kiểu dữ liệu
df_carts = df_carts.rename(columns={
    'productId': 'product_id',
    'cart_id': 'cart_id',
    'cart_userId': 'user_id',
    'cart_date': 'order_date'
})
df_carts['order_date'] = pd.to_datetime(df_carts['order_date']).dt.date

# 3. Load: Kết nối tới PostgreSQL trong Docker
print("Đang nạp dữ liệu vào PostgreSQL...")
engine = create_engine('postgresql+psycopg2://admin:adminpassword@localhost:5432/sales_data')

# Tạo bảng sales_orders và insert toàn bộ data
df_carts.to_sql('sales_orders', engine, if_exists='replace', index=False)
print("Hoàn tất ETL pipeline!")