# Xây dựng cơ chế phát hiện AI-generated code trong bài tập lập trình của sinh viên

**Thông tin đề tài:**

- Thời gian thực hiện: khoảng 11 tuần (08/04/2025 - 16/06/2025)
- Quy mô dự án: Chỉ áp dụng cho bài tập trên lớp/về nhà của SV năm nhất học Kỹ thuật lập trình/cấu trúc dữ liệu
- Giới hạn về ngôn ngữ lập trình: C, Java, Python, và frontend
- Chỉ xét mẫu từ các công cụ AI phổ biến (như ChatGPT, Github Copilot, Deepseek, Remini)
- Sử dụng các phương pháp nhận diện dựa trên đặc trưng code (code fingerprint, cấu trúc syntax, độ phức tạp, độ lặp lại,...), thay vì dùng deep learning phức tạp.

## 📆 Kế hoạch chi tiết theo tuần

### 📆 Tuần 1 (8/04 - 13/04): Phân tích đề tài

- [ ] Lựa chọn công nghệ
- [ ] Lập kế hoạch
- [ ] Viết đề cương chi tiết khóa luận

### 📆 Tuần 2 (14/04 - 20/04): Nghiên cứu cơ bản

- [ ] Khảo sát các công cụ AI phổ biến (ChatGPT, Copilot, Deepseek, Remini)
- [ ] Thu thập mẫu mã nguồn sinh từ AI
- [ ] Tìm hiểu các phương pháp phân tích đặc trưng code (code fingerprint, synta tree, cyclomatic complexity, clone detection)
- [ ] Trao đổi với GVHD

### 📆 Tuần 3 (21/04 - 27/04): Xây dựng tập dữ liệu mẫu

- [ ] Thu thập bài tập từ sinh viên
- [ ] Sinh mẫu code từ AI với cùng đề bài
- [ ] Phân loại thủ công mã AI vs mã con người
- [ ] Báo cáo tiến độ tuần 2 với GVHD

### 📆 Tuần 4 (28/04 - 04/05): Phân tích đặc trưng mã nguồn

- [ ] Viết tool Python để đo:
  - [ ] Độ phức tạp (radon)
  - [ ] Độ lặp lại (token-level)
  - [ ] Tỷ lệ comment, biến đặt tên chung chung
- [ ] Định nghĩa bộ đặc trưng đầu tiên
- [ ] Báo cáo tiến độ tuần 3 với GVHD

### 📆 Tuần 5 (05/05 - 11/05): Phân tích và thống kê dữ liệu

- [ ] Chạy phân tích trên tập dữ liệu
- [ ] Thống kê đặc trưng nào để phân biệt tốt giữa AI và người
- [ ] Lập bảng, biểu đồ so sánh, nhận xét
- [ ] Báo cáo tiến độ tuần 4 với GVHD

### 📆 Tuần 6 (12/05 - 18/05): Xây dựng prototype cơ bản

- [ ] Viết tool CLI/Web nhỏ nhận input mã nguồn
- [ ] Tính toán đặc trưng và xuất kết quả
- [ ] Gợi ý cảnh báo nếu nghi ngờ là mã AI-generated
- [ ] Báo cáo tiến độ tuần 5 với GVHD

### 📆 Tuần 7 (19/05 - 25/05): Kiểm thử - tinh chỉnh thuật toán

- [ ] Thử nghiệm với nhiều mẫu code
- [ ] Tối ưu ngưỡng cảnh báo
- [ ] Loại bỏ false positive nhiều nhất có thể
- [ ] Báo cáo tiến độ tuần 6 với GVHD

### 📆 Tuần 8 (26/05 - 01/06): Phát triển giao diện người dùng

- [ ] Web app nhỏ để nhập mã và hiển thị kết quả
- [ ] Giao diện đơn giản (Next.js/FastAPI)
- [ ] Hoàn thiện chức năng toàn hệ thống
- [ ] Báo cáo tiến độ tuần 7 GVHD

### 📆 Tuần 9 (02/06 - 08/06): Kiểm thử toàn hệ thống + viết khóa luận

- [ ] Test thử toàn diện
- [ ] Viết các phần chính của khóa luận: Cơ sở lý thuyết, Phương pháp tiếp cận, Phân tích dữ liệu
- [ ] Báo cáo tiến độ tuần 8 với GVHD

### 📆 Tuần 10 (09/06 - 11/06): Chỉnh sửa - Viết báo cáo hoàn chỉnh

- [ ] Viết phần đánh giá, kết luận, hướng phát triển
- [ ] Gửi GVHD xem bản nháp

### 📆 Tuần 11 (12/06 - 14/06): Sửa báo cáo theo phản hồi GVHD

- [ ] Hoàn thiện quyển khóa luận, chuẩn bị slide báo cáo
- [ ] Gửi khóa luận hoàn chỉnh

### 📆 Tuần 12 (15/06 - 16/06): Bảo vệ, nộp đồ khóa luận

- [ ] Chuẩn bị trình bày
- [ ] Nộp source code, tài liệu, slide
