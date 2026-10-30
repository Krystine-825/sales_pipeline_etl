# Dự án Data Engineer (Beginner): Sales Data Pipeline

Dự án này mô phỏng một luồng dữ liệu (Data Pipeline) thực tế, tự động lấy dữ liệu bán hàng từ API, xử lý và lưu trữ vào cơ sở dữ liệu PostgreSQL, sau đó trực quan hóa dữ liệu trên Dashboard.

## 1. Lý thuyết cốt lõi đã áp dụng

### Mô hình ETL (Extract - Transform - Load)
* **Extract (Trích xuất):** Kéo dữ liệu đơn hàng dạng JSON lồng nhau từ Fake Store API.
* **Transform (Biến đổi):** Sử dụng thư viện Pandas của Python để làm phẳng (flatten) dữ liệu JSON, đổi tên cột, định dạng lại kiểu dữ liệu (ngày tháng, số nguyên).
* **Load (Nạp):** Đẩy dữ liệu đã làm sạch vào cơ sở dữ liệu PostgreSQL.

### Containerization với Docker
* Thay vì cài đặt PostgreSQL trực tiếp lên máy tính dễ gây xung đột môi trường, dự án sử dụng **Docker** để bọc cơ sở dữ liệu trong một container độc lập. 
* Giúp môi trường phát triển (Dev) đồng nhất và dễ dàng dọn dẹp khi không sử dụng.

### Môi trường ảo (Virtual Environment) trong Python
* Sử dụng `venv` để tạo ra một không gian làm việc cục bộ cho dự án. Các thư viện (`pandas`, `sqlalchemy`, `streamlit`) được cài đặt riêng biệt, không ảnh hưởng đến các dự án Python khác trên máy tính.

### Tự động hóa (Automation & Orchestration)
* **Local:** Sử dụng Windows Task Scheduler kết hợp với Batch script (`.bat`) để lập lịch chạy pipeline tự động hằng ngày.
* **Thực tế doanh nghiệp:** Thường sử dụng Apache Airflow (nặng, tốn tài nguyên) hoặc các công cụ CI/CD như GitHub Actions (nhẹ, chạy trên mây) để quản lý luồng, theo dõi tiến trình và xử lý lỗi (retry/alert).

---

## 2. Các bước đã thực hiện

### Bước 1: Khởi tạo cơ sở dữ liệu với Docker
* Viết cấu hình `docker-compose.yml` để tải và chạy image `postgres:15`.
* Mở port `5432` và thiết lập Volume để dữ liệu không bị mất khi tắt container.

### Bước 2: Xây dựng Pipeline ETL (`etl_pipeline.py`)
* Sử dụng thư viện `requests` để gọi API `https://fakestoreapi.com/carts`.
* Dùng `pd.json_normalize()` kết hợp với tham số `record_path` và `meta` để bóc tách mảng `products` lồng bên trong mỗi `cart`.
* Sử dụng `sqlalchemy` (với driver `psycopg2`) để kết nối tới PostgreSQL và nạp dữ liệu bằng hàm `to_sql()`.

### Bước 3: Kiểm chứng dữ liệu (`verify_data.py`)
* Viết script Python truy vấn thẳng vào PostgreSQL thông qua Pandas bằng câu lệnh SQL cơ bản ( `SELECT`, `COUNT`, `SUM`, `GROUP BY`).
* Đảm bảo dữ liệu đã vào đúng form và không bị thiếu sót.

### Bước 4: Tự động hóa nội bộ (Local Automation)
* Viết file `run_etl.bat` tự động di chuyển thư mục, kích hoạt `venv` và chạy script Python.
* Lên lịch bằng Windows Task Scheduler để chạy ngầm vào 12:00 AM mỗi ngày.

### Bước 5: Trực quan hóa dữ liệu với Streamlit (`dashboard.py`)
* Xây dựng Web Dashboard để hiển thị báo cáo.
* **Data Integration:** Kéo thêm dữ liệu giá tiền từ API (`/products`) và `merge` với dữ liệu đơn hàng trong Database để tính toán **Doanh thu**.
* **Visualization:** Sử dụng `matplotlib` và `seaborn` để vẽ biểu đồ số lượng bán ra và doanh thu.
* **Export:** Thêm tính năng xuất dữ liệu ra định dạng `.csv` và `.xlsx` (sử dụng `openpyxl`).

---

## 3. Công nghệ sử dụng (Tech Stack)
* **Ngôn ngữ:** Python 3
* **Thư viện xử lý dữ liệu:** Pandas, Numpy
* **Database:** PostgreSQL, SQLAlchemy, Psycopg2
* **Infrastructure:** Docker, Docker Compose
* **Visualization:** Streamlit, Matplotlib, Seaborn
* **Automation (Local):** Windows Task Scheduler