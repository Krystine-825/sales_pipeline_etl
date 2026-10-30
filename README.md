# 🛒 Sales ETL Pipeline & Dashboard (Beginner Data Engineer Project)

Dự án Data Engineering cơ bản xây dựng một luồng dữ liệu (Data Pipeline) hoàn chỉnh từ khâu trích xuất qua API, làm sạch dữ liệu, lưu trữ vào cơ sở dữ liệu quan hệ, và trực quan hóa thành Dashboard.

## 🛠️ Công nghệ sử dụng
* **Ngôn ngữ:** Python (Pandas, Requests, SQLAlchemy)
* **Cơ sở dữ liệu:** PostgreSQL
* **Môi trường & Triển khai:** Docker, Windows Task Scheduler / GitHub Actions
* **Trực quan hóa (BI):** Streamlit, Matplotlib, Seaborn

## 🚀 Luồng dữ liệu (Architecture)
1. **Extract (Trích xuất):** Kéo dữ liệu đơn hàng và sản phẩm từ Fake Store API, lưu lại bản thô (raw JSON) để audit.
2. **Transform (Biến đổi):** Sử dụng Pandas để làm phẳng (flatten) các mảng JSON lồng nhau, chuẩn hóa kiểu dữ liệu (ngày tháng, số nguyên), và kết hợp bảng giá (merge) để tính doanh thu.
3. **Load (Nạp):** Đẩy dữ liệu đã làm sạch vào cơ sở dữ liệu PostgreSQL.
4. **Visualize (Trực quan hóa):** Truy vấn dữ liệu từ PostgreSQL lên Streamlit để vẽ biểu đồ và xuất báo cáo CSV/Excel.

## 📂 Cấu trúc thư mục
* `etl_pipeline.py`: Script chính thực hiện luồng Extract - Transform - Load.
* `verify_data.py`: Script truy vấn kiểm tra dữ liệu thực tế trong database.
* `dashboard.py`: Ứng dụng web Streamlit hiển thị biểu đồ và nút tải báo cáo.
* `docker-compose.yml`: Cấu hình khởi tạo database PostgreSQL cục bộ.
* `requirements.txt`: Danh sách các thư viện Python.