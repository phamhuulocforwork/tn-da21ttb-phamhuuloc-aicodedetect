# Tên đề tài: XÂY DỰNG CƠ CHẾ PHÂN TÍCH VÀ ĐÁNH GIÁ MÃ NGUỒN ĐỂ HỖ TRỢ PHÂN BIỆT AI-GENERATED CODE TRONG BÀI TẬP LẬP TRÌNH CỦA SINH VIÊN

## **Mục tiêu của đề tài**

Đề tài hướng đến việc nghiên cứu, xây dựng và đánh giá một **hệ thống phân tích mã nguồn** có khả năng cung cấp **các chỉ số, thông số đặc trưng** nhằm hỗ trợ người dùng phân biệt giữa mã nguồn do sinh viên viết và mã nguồn được tạo bởi các công cụ AI (như ChatGPT, GitHub Copilot, Deepseek…).  
Hệ thống **không nhằm mục tiêu khẳng định tuyệt đối** một đoạn mã là AI-generated hay không, mà đóng vai trò **công cụ tham khảo** giúp giảng viên, cán bộ chấm thi hoặc quản trị viên có thêm căn cứ khi đánh giá bài làm.

Bối cảnh xuất phát từ thực tế việc sinh viên ngày càng dễ dàng sử dụng các công cụ AI để hoàn thành bài tập lập trình, đặc biệt trong các môn học cơ bản như _Kỹ thuật lập trình_ hay _Cấu trúc dữ liệu_. Điều này tạo ra thách thức trong việc đảm bảo tính công bằng và đánh giá đúng năng lực thực tế của sinh viên.  
Đề tài tập trung vào việc:

- Xác định và phân tích các **đặc trưng thống kê, cấu trúc và phong cách** của mã nguồn.
- Xây dựng cơ chế đánh giá dựa trên **quy tắc (rule-based)** và **mô hình học máy nhẹ** nếu có dữ liệu phù hợp.
- Trình bày kết quả dưới dạng **bảng thông số và báo cáo phân tích**, giúp người dùng tự đưa ra quyết định.

Về mặt ứng dụng, công cụ được kỳ vọng:

- Giúp giảng viên nhận diện nhanh những trường hợp cần xem xét kỹ hơn.
- Có thể tích hợp vào hệ thống quản lý học tập để hỗ trợ chấm điểm thủ công.
- Dễ mở rộng hoặc tùy chỉnh ngưỡng đánh giá cho phù hợp với từng môn học hoặc yêu cầu cụ thể.

---

## **Nội dung thực hiện**

1. **Nghiên cứu cơ sở lý thuyết**

   - Tìm hiểu hoạt động và đặc điểm mã nguồn của các công cụ AI hỗ trợ lập trình.
   - Nắm rõ các chỉ số và đặc trưng mã nguồn có khả năng phân biệt giữa code AI và code do con người viết.

2. **Thu thập và xây dựng tập dữ liệu đối chiếu**

   - Thu thập mã nguồn từ bài tập lập trình của sinh viên.
   - Sinh mã nguồn tương ứng bằng các công cụ AI với cùng đề bài.
   - Phân loại và gán nhãn thủ công để tạo tập dữ liệu tham chiếu.

3. **Phân tích và trích xuất đặc trưng mã nguồn**

   - Phân tích cấu trúc bằng AST (Abstract Syntax Tree).
   - Tính toán độ phức tạp cyclomatic, tỷ lệ comment, độ lặp lại, độ dài hàm, phong cách đặt tên biến/hàm.
   - Ghi nhận các mẫu lập trình hoặc định dạng đặc trưng.

4. **Xây dựng cơ chế đánh giá**

   - Thiết lập các quy tắc (rule-based) dựa trên ngưỡng đặc trưng.
   - Thử nghiệm mô hình học máy nhẹ nếu dữ liệu phù hợp.
   - Tạo thang điểm hoặc hệ số nghi ngờ để biểu diễn mức độ khả nghi.

5. **Phát triển ứng dụng minh họa**
   - Giao diện CLI hoặc web app (FastAPI, Next.js) cho phép người dùng nhập mã nguồn.
   - Hiển thị bảng thông số, biểu đồ và mức độ nghi ngờ.
   - Cung cấp tùy chọn tải báo cáo phân tích để lưu trữ hoặc gửi kèm khi chấm điểm.

---

> **Lưu ý:** Hệ thống chỉ đưa ra thông số và phân tích tham khảo, không thay thế kết luận của người chấm.
