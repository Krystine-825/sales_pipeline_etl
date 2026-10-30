import os
import requests
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()
db_url = os.getenv("DATABASE_URL")
engine = create_engine(db_url)

# 1. Extract: Lấy dữ liệu carts từ DummyJSON (mở hoàn toàn, không block IP)
print("Đang lấy dữ liệu từ API...")
response = requests.get("https://dummyjson.com/carts", timeout=15)

if response.status_code != 200:
    raise Exception(f"Lỗi gọi API. Mã trạng thái: {response.status_code}")
    
raw_data = response.json()

# 2. Transform: Bóc tách mảng 'products' nằm trong mỗi 'cart'
df_carts = pd.json_normalize(
    raw_data['carts'], # DummyJSON trả về danh sách nằm trong key 'carts'
    record_path=['products'],
    meta=['id', 'userId'],
    meta_prefix='cart_'
)

# Chuẩn hóa tên cột để khớp với dashboard cũ (lưu ý: DummyJSON không có cột date)
df_carts = df_carts.rename(columns={
    'id': 'product_id',
    'cart_id': 'cart_id',
    'cart_userId': 'user_id'
})

# Thêm cột order_date giả định (vì DummyJSON thiếu cột này)
df_carts['order_date'] = pd.Timestamp('today').normalize().date()

# Giữ lại đúng các cột cần thiết cho bảng sales_orders
final_columns = ['cart_id', 'user_id', 'order_date', 'product_id', 'quantity']
df_carts = df_carts[final_columns]

# 3. Load: Đẩy lên Supabase PostgreSQL
print("Đang nạp dữ liệu vào PostgreSQL...")
df_carts.to_sql('sales_orders', engine, if_exists='replace', index=False)

print("Hoàn tất ETL pipeline!")