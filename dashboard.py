import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import io
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

# 1. Kết nối cơ sở dữ liệu
load_dotenv() 
db_url = os.getenv("DATABASE_URL")
engine = create_engine(db_url)
st.title("📊 Báo cáo Doanh số & Doanh thu")

# 2. Truy vấn dữ liệu đơn hàng
query = """
SELECT product_id, COUNT(cart_id) AS total_orders, SUM(quantity) AS total_items_sold
FROM sales_orders
GROUP BY product_id
ORDER BY total_items_sold DESC
LIMIT 10;
"""
df_sales = pd.read_sql(query, engine)

# 3. Gọi API lấy giá sản phẩm và kết hợp dữ liệu
@st.cache_data 
def get_product_prices():
    headers = {'User-Agent': 'PostmanRuntime/7.36.3', 'Accept': '*/*'}
    res = requests.get("https://fakestoreapi.com/products", headers=headers, timeout=15).json()
    df_products = pd.json_normalize(res)[['id', 'price', 'title']]
    return df_products.rename(columns={'id': 'product_id'})

df_prices = get_product_prices()
df_sales['product_id'] = df_sales['product_id'].astype(int)
df_final = df_sales.merge(df_prices, on='product_id', how='left')

# Tính doanh thu = Tổng số lượng bán * Giá tiền
df_final['revenue'] = df_final['total_items_sold'] * df_final['price']

st.subheader("Bảng dữ liệu chi tiết")
st.dataframe(df_final[['product_id', 'title', 'total_items_sold', 'price', 'revenue']])

# 4. Tính năng trích xuất (Export)
col1, col2 = st.columns(2)
with col1:
    csv = df_final.to_csv(index=False).encode('utf-8')
    st.download_button(label="📥 Tải báo cáo (CSV)", data=csv, file_name="sales_report.csv", mime="text/csv")
with col2:
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df_final.to_excel(writer, index=False, sheet_name='Report')
    st.download_button(label="📥 Tải báo cáo (Excel)", data=buffer.getvalue(), file_name="sales_report.xlsx", mime="application/vnd.ms-excel")

# 5. Trực quan hóa dữ liệu
df_final['product_id_str'] = df_final['product_id'].astype(str)

st.subheader("Biểu đồ Số lượng bán ra")
fig1, ax1 = plt.subplots(figsize=(10, 4))
sns.barplot(data=df_final, x='product_id_str', y='total_items_sold', ax=ax1, palette='Blues_d')
ax1.set_xlabel("Mã sản phẩm")
st.pyplot(fig1)

st.subheader("Biểu đồ Doanh thu ($)")
fig2, ax2 = plt.subplots(figsize=(10, 4))
sns.barplot(data=df_final, x='product_id_str', y='revenue', ax=ax2, palette='Greens_d')
ax2.set_xlabel("Mã sản phẩm")
st.pyplot(fig2)