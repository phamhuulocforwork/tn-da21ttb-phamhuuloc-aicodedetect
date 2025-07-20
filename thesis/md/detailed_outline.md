# Tên đề tài: XÂY DỰNG CƠ CHẾ PHÁT HIỆN AI-GENERATED CODE TRONG BÀI TẬP LẬP TRÌNH CỦA SINH VIÊN

Quy mô dự án: Chỉ áp dụng cho bài tập trên lớp/về nhà của SV năm nhất học Kỹ thuật lập trình/cấu trúc dữ liệu

**Mục tiêu của đề tài**

Đề tài "Xây dựng cơ chế phát hiện AI-generated code trong bài tập lập trình của sinh viên" hướng đến việc nghiên cứu, xây dựng và đánh giá một hệ thống có khả năng phát hiện mã nguồn được tạo ra bởi các công cụ AI trong bài tập lập trình của sinh viên. Với sự phát triển mạnh mẽ của các mô hình ngôn ngữ lớn và công cụ hỗ trợ lập trình như ChatGPT, Github Copilot, Deepseek hay Remini,… Việc sinh viên sử dụng các công cụ này trong quá trình học tập đang trở nên phổ biến. Điều này tạo ra thách thức trong việc đánh giá năng lực thực sự của sinh viên, đặc biệt là trong các môn học cơ bản như Kỹ thuật lập trình hay Cấu trúc dữ liệu. Đề tài này phát triển một công cụ với quy trình cụ thể nhằm hỗ trợ việc phát hiện mã nguồn được tạo bởi AI thông qua việc phân tích các đặc trưng của mã nguồn mà không cần sử dụng các mô hình học sâu phức tạp.

Mục tiêu nghiên cứu của đề tài tập trung vào việc tìm hiểu sâu về các đặc trưng của mã nguồn do AI tạo ra, từ đó phát triển các phương pháp phân tích và phát hiện hiệu quả. Quá trình thực hiện đề tài giúp củng cố kiến thức về phân tích mã nguồn, hiểu rõ về cấu trúc và đặc điểm của mã do con người và AI tạo ra. Việc thu thập và xây dựng tập dữ liệu đối chiếu giúp phát triển kỹ năng xử lý dữ liệu thực tế, trong khi việc trích xuất các đặc trưng từ mã nguồn như AST (Abstract Syntax Tree), độ phức tạp, độ lặp lại và các đặc điểm về cách đặt tên biến/hàm giúp nâng cao hiểu biết về kỹ thuật phân tích mã nguồn.

Việc xây dựng mô hình phát hiện bằng phương pháp rule-based và học máy nhẹ cũng là cơ hội để áp dụng kiến thức về thuật toán vào giải quyết vấn đề thực tế, cũng như rèn luyện kỹ năng đánh giá hiệu quả của các phương pháp khác nhau. Quá trình này không chỉ giúp hoàn thiện kỹ năng lập trình và xử lý dữ liệu mà còn phát triển tư duy phân tích, tổng hợp và đánh giá trong nghiên cứu khoa học.

Về mặt ứng dụng, đề tài hướng đến việc xây dựng một công cụ thực tế có thể hỗ trợ giảng viên trong việc đánh giá bài tập của sinh viên, đảm bảo tính công bằng trong quá trình học tập. Công cụ này có thể được tích hợp vào hệ thống quản lý học tập, hỗ trợ việc phát hiện tự động mã nguồn nghi ngờ, từ đó giúp giảng viên tập trung vào việc đánh giá chính xác hơn các trường hợp đặc biệt.

**Nội dung thực hiện:**

Đề tài sẽ bắt đầu với việc nghiên cứu các khái niệm và công nghệ liên quan đến các công cụ AI hỗ trợ lập trình. Việc tìm hiểu cách thức hoạt động và đặc điểm mã nguồn từ các công cụ như ChatGPT, Github Copilot, Deepseek và Remini cung cấp nền tảng lý thuyết vững chắc để xác định các đặc trưng tiềm năng giúp phân biệt mã nguồn do AI tạo ra và mã nguồn do sinh viên viết.

Sau đó, đề tài sẽ tiến hành thu thập và xây dựng tập dữ liệu mẫu bao gồm hai nhóm: mã nguồn thực tế từ bài tập của sinh viên và mã nguồn được tạo bởi các công cụ AI với cùng yêu cầu bài tập. Quá trình này đòi hỏi sự phối hợp với giảng viên để có được bài tập và mã nguồn của sinh viên, đồng thời cần thực hiện việc sử dụng các công cụ AI để tạo ra mã nguồn tương ứng. Dữ liệu thu thập sẽ được phân loại và gán nhãn thủ công, tạo thành tập dữ liệu chuẩn để phục vụ cho quá trình phân tích và đánh giá sau này.

Tiếp theo, đề tài sẽ tập trung vào việc phân tích đặc trưng mã nguồn thông qua việc xây dựng các công cụ phân tích tự động. Các phương pháp phân tích và trích xuất đặc trưng sẽ được nghiên cứu và triển khai, bao gồm việc sử dụng AST để phân tích cấu trúc mã nguồn, tính toán đo lường độ phức tạp (cyclomatic complexity), phân tích độ lặp lại của mã (code redundancy) và cách đặt tên biến/hàm. Ngoài ra, đề tài còn xem xét các đặc trưng khác như tỷ lệ comment, biến đặt tên chung chung và các mẫu lập trình đặc trưng.

Dựa trên kết quả phân tích đặc trưng, đề tài sẽ tiến hành xây dựng các phương pháp phát hiện mã nguồn do AI tạo ra. Hai hướng tiếp cận chính sẽ được áp dụng: phương pháp dựa trên luật (rule-based) với việc xác định các ngưỡng thủ công cho các đặc trưng đã trích xuất, và phương pháp học máy nhẹ nếu có đủ dữ liệu. Việc kết hợp hai phương pháp này giúp tận dụng ưu điểm của mỗi phương pháp, đồng thời cho phép đánh giá hiệu quả của từng cách tiếp cận.

Cuối cùng, đề tài sẽ phát triển một ứng dụng thử nghiệm với giao diện người dùng thân thiện, cho phép người dùng nhập mã nguồn và nhận kết quả phân tích, cùng với các gợi ý và cảnh báo khi phát hiện mã nguồn có khả năng được tạo bởi AI. Ứng dụng này có thể được phát triển dưới dạng công cụ CLI hoặc web app đơn giản sử dụng các công nghệ như FastAPI và Next.js.