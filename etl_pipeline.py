import os
import requests
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Khởi tạo kết nối DB từ biến môi trường
load_dotenv()
db_url = os.getenv("DATABASE_URL")
engine = create_engine(db_url)

# 1. Extract: Lấy dữ liệu từ API kèm Header chống block
print("Đang lấy dữ liệu từ API...")
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}
response = requests.get("https://fakestoreapi.com/carts", headers=headers, timeout=15)

if response.status_code != 200:
    raise Exception(f"Lỗi gọi API. Mã trạng thái: {response.status_code}")
    
try:
    raw_data = response.json()
except ValueError:
    raise Exception("API không trả về dữ liệu JSON hợp lệ. Nội dung trả về: " + response.text)

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

# 3. Load: Đẩy lên Supabase PostgreSQL
print("Đang nạp dữ liệu vào PostgreSQL...")
df_carts.to_sql('sales_orders', engine, if_exists='replace', index=False)

print("Hoàn tất ETL pipeline!")