# Xây dựng cơ chế phát hiện AI-generated code trong bài tập lập trình của sinh viên

**Thông tin đề tài:**

- Thời gian thực hiện: khoảng 11 tuần (08/04/2025 - 16/06/2025)
- Quy mô dự án: Chỉ áp dụng cho bài tập trên lớp/về nhà của SV năm nhất học Kỹ thuật lập trình/cấu trúc dữ liệu
- Giới hạn về ngôn ngữ lập trình: C, Java, Python, và frontend
- Chỉ xét mẫu từ các công cụ AI phổ biến (như ChatGPT, Github Copilot, Deepseek, Remini)
- Sử dụng các phương pháp nhận diện dựa trên đặc trưng code (code fingerprint, cấu trúc syntax, độ phức tạp, độ lặp lại,...), thay vì dùng deep learning phức tạp.

## 📆 Kế hoạch chi tiết theo tuần

### 📆 Tuần 1 (03/07 – 06/07): Khởi động & Xác định phạm vi

- [ ] Nghiên cứu: rà soát yêu cầu bài tập, khảo sát giải pháp tương tự
- [ ] Phát triển: khởi tạo repo, thiết lập môi trường, chọn thư viện phân tích mã
- [ ] Test: chạy thử parser trên vài bài tập mẫu
- [ ] Viết báo cáo: hoàn thiện đề cương chi tiết, lập WBS
- [ ] Báo cáo tiến độ với GVHD (04/07)

### 📆 Tuần 2 (07/07 – 13/07): Thu thập & xây dựng tập dữ liệu

- [ ] Nghiên cứu: khảo sát công cụ AI (ChatGPT, Copilot, Deepseek, Remini)
- [ ] Phát triển: script thu thập/chuẩn hoá bài tập SV & mã AI, định nghĩa schema dữ liệu
- [ ] Test: kiểm tra tính toàn vẹn, loại bỏ trùng lặp
- [ ] Viết báo cáo: mô tả quy trình xây dựng dataset
- [ ] Báo cáo tiến độ với GVHD (11/07)

### 📆 Tuần 3 (14/07 – 20/07): Phát triển bộ trích xuất đặc trưng

- [ ] Nghiên cứu: code fingerprint, AST metrics, cyclomatic complexity
- [ ] Phát triển: cài đặt các extractor (fingerprint, phức tạp, lặp lại, tỷ lệ comment)
- [ ] Test: unit-test từng đặc trưng trên dataset nhỏ
- [ ] Viết báo cáo: mô tả module & kết quả test
- [ ] Báo cáo tiến độ với GVHD (18/07)

### 📆 Tuần 4 (21/07 – 27/07): Phân tích dữ liệu & mô hình baseline

- [ ] Nghiên cứu: thống kê đặc trưng, chọn tín hiệu mạnh
- [ ] Phát triển: mô hình rule-based / scoring, xác định ngưỡng ban đầu
- [ ] Test: cross-validation, ghi nhận precision/recall
- [ ] Viết báo cáo: báo cáo EDA & baseline
- [ ] Báo cáo tiến độ với GVHD (25/07)

### 📆 Tuần 5 (28/07 – 03/08): Hoàn thiện Prototype CLI

- [ ] Phát triển: tích hợp pipeline mô hình vào CLI, sinh report phân tích
- [ ] Test: thử nghiệm trên tập chưa thấy, tinh chỉnh tham số
- [ ] Viết báo cáo: hướng dẫn sử dụng, kiến trúc hệ thống
- [ ] Báo cáo tiến độ với GVHD (01/08)

### 📆 Tuần 6 (04/08 – 10/08): Giao diện Web & kiểm thử hệ thống

- [ ] Phát triển: Web API (FastAPI) frontend đơn giản, Dockerize
- [ ] Test: end-to-end, đánh giá UX, đo hiệu năng
- [ ] Viết báo cáo: chương triển khai & kết quả test hệ thống
- [ ] Báo cáo tiến độ với GVHD (08/08)

### 📆 Tuần 7 (11/08 – 17/08): Hoàn thiện, đánh giá & chuẩn bị bảo vệ

- [ ] Phát triển: tối ưu, đóng gói, script auto-evaluation
- [ ] Test: kiểm thử cuối, thu số liệu đánh giá
- [ ] Viết báo cáo: hoàn thiện khóa luận, slide & demo
- [ ] Báo cáo tiến độ: gửi bản nháp cuối, lấy phản hồi GVHD (14/08)
- [ ] Bảo vệ: 16-17/08 (dự kiến)

## 🚩 Mốc quan trọng

| Thời hạn | Mốc               | Ghi chú                      |
| -------- | ----------------- | ---------------------------- |
| 13/07    | Dataset đóng băng | Không chỉnh sửa sau mốc này  |
| 20/07    | Khóa bộ đặc trưng | Không thêm đặc trưng mới     |
| 27/07    | Baseline hoàn tất | Có kết quả đánh giá đầu tiên |
| 03/08    | Prototype CLI     | Sẵn sàng demo                |
| 10/08    | Web demo          | Hoạt động end-to-end         |
| 17/08    | Nộp khóa luận     | Mốc cứng                     |
