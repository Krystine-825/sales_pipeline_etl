# 🛒 Sales ETL Pipeline & Dashboard (Beginner Data Engineer Project)

Dự án Data Engineering cơ bản xây dựng một luồng dữ liệu (Data Pipeline) hoàn chỉnh từ khâu trích xuất qua API, làm sạch dữ liệu, lưu trữ vào cơ sở dữ liệu quan hệ trên đám mây, và trực quan hóa thành Dashboard. Toàn bộ quy trình được tự động hóa (CI/CD) bằng GitHub Actions.

## 🛠️ Công nghệ sử dụng
* **Ngôn ngữ:** Python (Pandas, Requests, SQLAlchemy, python-dotenv)
* **Cơ sở dữ liệu:** PostgreSQL (Supabase Cloud)
* **Tự động hóa (Orchestration):** GitHub Actions
* **Trực quan hóa (BI):** Streamlit, Matplotlib, Seaborn

## 🚀 Luồng dữ liệu (Architecture)
1. **Extract (Trích xuất):** Kéo dữ liệu đơn hàng (`carts`) và sản phẩm (`products`) từ DummyJSON API.
2. **Transform (Biến đổi):** Sử dụng Pandas để làm phẳng (flatten) các mảng JSON lồng nhau, chuẩn hóa tên cột, tạo thêm cột dữ liệu ngày tháng giả định, và kết hợp (merge) bảng giá để tính tổng doanh thu.
3. **Load (Nạp):** Đẩy dữ liệu đã làm sạch vào cơ sở dữ liệu PostgreSQL trên Supabase. Kết nối được bảo mật nghiêm ngặt bằng biến môi trường (Environment Variables).
4. **Visualize (Trực quan hóa):** Truy vấn dữ liệu từ Supabase lên ứng dụng Streamlit để hiển thị báo cáo, vẽ biểu đồ và cho phép tải xuống file CSV/Excel.
5. **Automate (Tự động hóa):** GitHub Actions thực thi kịch bản ETL tự động vào nửa đêm hằng ngày.

## 📂 Cấu trúc thư mục
* `etl_pipeline.py`: Script xử lý ETL chính.
* `verify_data.py`: Script truy vấn kiểm tra dữ liệu thực tế.
* `dashboard.py`: Ứng dụng web Streamlit.
* `requirements.txt`: Danh sách các thư viện Python cần thiết.
* `.github/workflows/etl.yml`: File cấu hình lịch trình tự động của GitHub Actions.
* `.env`: (Local) Chứa chuỗi kết nối an toàn (Không đưa lên Git).

## 📝 Nhật ký Dự án & Xử lý Sự cố (Troubleshooting)

Trong quá trình xây dựng dự án, một số vấn đề thực tế đã phát sinh và được giải quyết:

**1. Chuyển đổi môi trường linh hoạt (Local to Cloud)**
* *Mục tiêu:* Thiết lập tự động hóa hoàn toàn luồng ETL mà không phụ thuộc vào máy tính cá nhân.
* *Giải pháp:* Chuyển đổi cơ sở dữ liệu từ Docker cục bộ lên Supabase (PostgreSQL Cloud). Xây dựng cơ chế đọc chuỗi kết nối qua `python-dotenv` khi chạy local và qua `GitHub Secrets` khi chạy trên CI/CD, đảm bảo tuyệt đối không rò rỉ mật khẩu lên mã nguồn mở.

**2. Vượt rào cản Anti-Scraping của API (Lỗi 403 Forbidden / JSONDecodeError)**
* *Vấn đề:* Khi cấu hình luồng chạy trên GitHub Actions, API ban đầu (FakeStoreAPI) liên tục trả về lỗi `403 Forbidden` hoặc `JSONDecodeError: Expecting value`.
* *Nguyên nhân:* Hệ thống bảo mật (Cloudflare) của nguồn cấp dữ liệu phát hiện lưu lượng truy cập xuất phát từ dải IP trung tâm dữ liệu đám mây (máy chủ Azure của GitHub Actions). Hệ thống tự động đánh giá đây là bot cào dữ liệu nên đã chặn toàn bộ kết nối.
* *Giải pháp:* 
  * Bước 1: Thử giả lập HTTP Header (`User-Agent`) của trình duyệt Chrome và Postman để ngụy trang, nhưng vẫn bị tường lửa chặn do khóa theo IP.
  * Bước 2: Linh hoạt thay đổi kiến trúc nguồn (Source). Thay thế FakeStoreAPI bằng DummyJSON API — một nguồn dữ liệu có cấu trúc tương đồng nhưng mở cấu hình mạng thân thiện với CI/CD hơn.
  * Bước 3: Điều chỉnh lại mã nguồn Transform (`pd.json_normalize`) để xử lý cấu trúc JSON lồng nhau theo chuẩn mới của DummyJSON. Pipeline sau đó đã chạy ổn định trên đám mây.

## 🏃 Hướng dẫn chạy dự án cục bộ (Local)
1. Clone dự án về máy.
2. Cài đặt thư viện: `pip install -r requirements.txt`
3. Tạo file `.env` và thiết lập biến `DATABASE_URL`.
4. Chạy ETL: `python etl_pipeline.py`
5. Xem Dashboard: `streamlit run dashboard.py`