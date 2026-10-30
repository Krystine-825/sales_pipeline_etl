import pandas as pd
from sqlalchemy import create_engine

# Kết nối tới PostgreSQL
engine = create_engine('postgresql+psycopg2://admin:adminpassword@localhost:5432/sales_data')

# Truy vấn 1: Lấy 5 bản ghi đầu tiên để kiểm tra cấu trúc
print("--- 5 BẢN GHI ĐẦU TIÊN ---")
df_head = pd.read_sql("SELECT * FROM sales_orders LIMIT 5", engine)
print(df_head)

# Truy vấn 2: Thống kê tổng số lượng bán ra theo từng sản phẩm
print("\n--- TOP 5 SẢN PHẨM BÁN CHẠY ---")
query = """
SELECT product_id, COUNT(cart_id) AS total_orders, SUM(quantity) AS total_items_sold
FROM sales_orders
GROUP BY product_id
ORDER BY total_items_sold DESC
LIMIT 5;
"""
df_stats = pd.read_sql(query, engine)
print(df_stats)