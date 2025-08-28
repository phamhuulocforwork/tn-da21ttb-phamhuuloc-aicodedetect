# Chức năng phân tích nhiều file

Bây giờ tôi cần phân tích nhiều file cùng 1 lúc. Hãy tự lập kế hoạch chi tiết và thực hiện cụ thể yêu cầu như sau:

- Thêm api endpoint để xử lý phân tích nhiều file 1 lúc, có 2 tuỳ chọn cần xử lý (chỉ bằng so sánh baseline)
  - Upload file zip hoặc rar (có thể là chứa nhiều file, hoặc nhiều folder mỗi folder chứa nhiều file)
  - Link Google Drive folder/file share công khai
- Thêm 1 page để xử lý phân tích nhiều file với 3 step:
  - Step 1: Tuỳ chọn upload file nén (zip, rar), hoặc link Google Drive
  - Step 2: Table hiện thị danh sách, mỗi dòng là thông tin của một file
  - Step 3: Hiện thị danh sách file sau phân tích gồm thông tin tên file, số dòng, kích thước và Radial Chart kết quả só sánh baseline ví dụ: 46% Độ tương đồng với AI, 28% Độ tương đồng với người, nút xem chi tiết phân tích -> điều hướng tới `http://localhost:3000/analysis?code=` với code được encode
