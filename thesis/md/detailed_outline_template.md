# Nhận diện cảm xúc từ văn bản tiếng Việt bằng mô hình NLP

## Mục tiêu của đề tài

Đề tài "Nhận diện cảm xúc từ văn bản tiếng Việt bằng mô hình NLP" hướng đến việc nghiên cứu, xây dựng và đánh giá một hệ thống có khả năng tự động nhận diện cảm xúc từ các đoạn văn bản tiếng Việt bằng cách ứng dụng các kỹ thuật xử lý ngôn ngữ tự nhiên (Natural Language Processing – NLP) kết hợp với các mô hình học máy hiện đại.

### Về mục tiêu nghiên cứu – học tập

Làm quen và thực hành triển khai các mô hình học máy (Machine Learning) và học sâu (Deep Learning), bao gồm cả các kiến trúc mạng nơ-ron như RNN, LSTM, BERT, hay Transformer trong bài toán phân tích cảm xúcâng cao kiến thức và kỹ năng chuyên môn trong lĩnh vực xử lý ngôn ngữ tự nhiên, đặc biệt là đối với tiếng Việt – một ngôn ngữ có đặc thù riêng về cú pháp và ngữ nghĩa. Tìm hiểu và áp dụng các kỹ thuật tiền xử lý văn bản, vector hóa, trích xuất đặc trưng và phân loại cảm xúc trên văn bản tự nhiênèn luyện kỹ năng xây dựng quy trình nghiên cứu khoa học: từ việc thu thập dữ liệu, xử lý dữ liệu, huấn luyện mô hình, đánh giá kết quả cho đến việc tối ưu và trình bày hệ thốngề mục tiêu ứng dụng, đề tài hướng đến việc xây dựng một mô hình hoặc hệ thống có khả năng phân loại cảm xúc trong văn bản tiếng Việt với độ chính xác cao, từ đó có thể được áp dụng vào các lĩnh vực thực tiễn như:

- Phân tích ý kiến người dùng trong các bài đánh giá sản phẩm, dịch vụ trên mạng xã hội, diễn đàn hoặc sàn thương mại điện tử Hỗ trợ giám sát dư luận xã hội, phát hiện xu hướng hoặc phản ứng tiêu cực tích cực từ cộng đồng đối với một sự kiện, cá nhân hoặc tổ chức Tăng cường khả năng tương tác của chatbot, trợ lý ảo bằng cách giúp hệ thống hiểu được cảm xúc của người dùng trong quá trình giao tiếp Làm nền tảng cho các nghiên cứu mở rộng về phân tích ngữ nghĩa, tóm tắt văn bản cảm xúc, hoặc tạo ra các hệ thống phản hồi thông minh, có cảm xúc trong tương lai Tóm lại, đề tài không chỉ phục vụ cho mục tiêu học thuật mà còn hướng đến việc tạo ra giá trị thực tiễn, góp phần thúc đẩy các nghiên cứu và ứng dụng công nghệ AI – NLP trong ngôn ngữ tiếng Việt.

### Nội dung thực hiện

Tìm hiểu khái niệm và các hướng tiếp cận trong phân tích cảm xúc (Sentiment Analysis): Đề tài sẽ tiến hành nghiên cứu các khái niệm nền tảng liên quan đến bài toán phân tích cảm xúc, bao gồm định nghĩa cảm xúc trong ngữ cảnh văn bản, các mức độ phân loại cảm xúc phổ biến (như tích cực, tiêu cực, trung lập hoặc các nhãn chi tiết hơn như vui, buồn, tức giận, sợ hãi,...), cùng với các cấp độ phân tích (mức độ câu, đoạn văn, tài liệu). Ngoài ra, đề tài sẽ khảo sát các hướng tiếp cận trong lĩnh vực này, bao gồm phương pháp dựa trên từ điển cảm xúc, cũng như các phương pháp hiện đại dựa trên mô hình học máy và học sâu. Việc nắm vững các hướng tiếp cận sẽ là cơ sở để xây dựng chiến lược phù hợp cho tiếng Việt – một ngôn ngữ có đặc điểm khác biệt so với tiếng Anh.

Khảo sát và lựa chọn tập dữ liệu tiếng Việt phù hợp: Dữ liệu là yếu tố then chốtrong việc huấn luyện và đánh giá mô hình phân tích cảm xúc. Do đó, đề tài sẽ thực hiện khảoát, thu thập và đánh giá các bộ dữ liệu tiếng Việt có sẵn phục vụ cho bài toán nhận diện cảmúc. Một số nguồn dữ liệu có thể được khai thác bao gồm các diễn đàn, trang đánh giá sảnhẩm, bình luận mạng xã hội như Facebook, Shopee, Tiki, hoặc dữ liệu từ các bài báo, blog.rong trường hợp dữ liệu không đủ hoặc chưa được gán nhãn đầy đủ, đề tài có thể thực hiệnước tiền xử lý và gán nhãn thủ công hoặc bán tự động. Dữ liệu sau khi thu thập sẽ được làmạch, chuẩn hóa và phân chia thành tập huấn luyện, tập kiểm thử và tập kiểm tra.

Tìm hiểu và ứng dụng các kỹ thuật xử lý ngôn ngữ tự nhiên (NLP) đối với tiếngiệt: Văn bản tiếng Việt có nhiều thách thức trong NLP như ngôn ngữ không dấu, từ đaghĩa, cú pháp linh hoạt. Do đó, đề tài sẽ nghiên cứu các kỹ thuật tiền xử lý ngôn ngữ phùợp như tách từ, chuẩn hóa văn bản, loại bỏ từ dừng, xử lý từ viết tắt, biểu tượng cảm xúc,...goài ra, đề tài cũng sẽ xem xét các phương pháp biểu diễn văn bản (text representation) nhưord2Vec từ các mô hình đã được huấn luyện như PhoBERT – một mô hình BERT dànhiêng cho tiếng Việt.

Nghiên cứu và triển khai các thuật toán học máy (Machine Learning): Sau khioàn thành bước xử lý dữ liệu, đề tài sẽ thử nghiệm các mô hình học máy cổ điển như Naiveayes, SVM (Support Vector Machine), Decision Tree, KNN,... Các mô hình này sẽ đượcuấn luyện với dữ liệu đã xử lý để làm cơ sở đánh giá và so sánh hiệu năng ban đầu. Cácham số mô hình sẽ được tinh chỉnh (tuning) để cải thiện độ chính xác, đồng thời đánh giá độiệu quả qua các chỉ số như Accuracy, Precision, Recall, F1-score.

Nghiên cứu và áp dụng các mô hình học sâu (Deep Learning): Trong giai đoạn tiếpheo, đề tài sẽ nghiên cứu các kiến trúc học sâu hiện đại nhằm nâng cao độ chính xác và khảăng biểu diễn ngữ nghĩa sâu hơn. Các mô hình như CNN, RNN, LSTM, BiLSTM và đặciệt là các mô hình transformer như BERT, PhoBERT sẽ được xem xét triển khai. Đề tài cũngẽ đánh giá hiệu quả của các mô hình pre-trained được huấn luyện trên dữ liệu tiếng Việt đểận dụng sức mạnh học biểu diễn ngữ nghĩa từ mô hình lớn. Việc huấn luyện và tinh chỉnhác mô hình này đòi hỏi xử lý tốt các yếu tố kỹ thuật như điều chỉnh learning rate, batch size,poch, dropout,... và sử dụng GPU để tối ưu thời gian huấn luyện.

Đánh giá, so sánh mô hình và tổng hợp kết quả: Sau khi huấn luyện các mô hìnhọc máy và học sâu, đề tài sẽ tiến hành đánh giá và so sánh kết quả theo các tiêu chí địnhượng. Việc đánh giá không chỉ dựa trên độ chính xác, mà còn xét đến tính tổng quát, khảăng mở rộng và thời gian xử lý. Qua đó, lựa chọn mô hình tối ưu để làm mô hình cuối cùng.

Xây dựng hệ thống thử nghiệm và trình bày kết quả: Sau khi hoàn thiện quá trìnhghiên cứu và huấn luyện mô hình nhận diện cảm xúc, đề tài sẽ tiến hành xây dựng một ứngụng thử nghiệm có khả năng phân tích và phân loại cảm xúc của người dùng từ các phảnồi, bình luận trên các trang thương mại điện tử. Hệ thống đóng vai trò như một minh chứnghực tế cho hiệu quả của mô hình đã xây dựng, đồng thời thể hiện tiềm năng ứng dụng trongác bài toán công nghiệp.

### Phương pháp thực hiện

Để đạt được mục tiêu của đề tài, quá trình thực hiện sẽ được chia thành các bước cụhể, tuần tự theo quy trình xử lý dữ liệu và phát triển mô hình học máy/học sâu trong lĩnh vựcử lý ngôn ngữ tự nhiên. Cụ thể, các phương pháp được áp dụng bao gồm:

Khảo sát lý thuyết và tổng quan nghiên cứu: Tìm hiểu các khái niệm liên quan đếnhân tích cảm xúc (sentiment analysis), các cấp độ cảm xúc (câu, đoạn, tài liệu) và các loạiảm xúc phổ biến. Nghiên cứu các phương pháp dựa trên học máy và học sâu. Khảo sát cácông trình nghiên cứu trước đó liên quan đến phân tích cảm xúc trong tiếng Việt và các ngôngữ khác.

Thu thập và xử lý dữ liệu: Tìm kiếm và lựa chọn các bộ dữ liệu có sẵn chứa văn bảniếng Việt được gán nhãn cảm xúc, thực hiện các bước tiền xử lý ngôn ngữ tự nhiên, bao gồmàm sạch văn bản (loại bỏ ký tự đặc biệt, liên kết, html tag,...), tách từ bằng thư viện, chuẩnóa văn bản, mã hóa văn bản.

Xây dựng mô hình học máy và học sâu: Thử nghiệm các mô hình học máy cổ điểnể làm cơ sở so sánh, triển khai các mô hình học sâu phổ biến cho xử lý chuỗi văn bản, tinhhỉnh siêu tham số và tối ưu mô hình.uấn luyện và đánh giá mô hình: Chia dữ liệu thành các tập huấn luyện, kiểm thửà kiểm tra theo tỷ lệ hợp lý, sử dụng các thước đo đánh giá như Accuracy, Precision, Recall,1-score, Confusion Matrix để đo lường hiệu quả mô hình, so sánh kết quả giữa các môình học máy, học sâu và mô hình tiền huấn luyện để chọn ra phương án tối ưu.

Triển khai ứng dụng thử nghiệm: Phát triển một ứng dụng web đơn giản cho phépgười dùng nhập văn bản phản hồi hoặc bình luận sản phẩm từ các sàn thương mại điện tử,à nhận kết quả phân tích cảm xúc ngay lập tức. Ứng dụng sử dụng mô hình đã huấn luyệnhư một REST API phía backend (có thể dùng Flask, FastAPI), frontend đơn giản (có thểùng React). Có thể bổ sung tính năng phân tích hàng loạt phản hồi, biểu đồ thống kê cảmúc, lọc theo sản phẩm.

Tổng hợp kết quả và đề xuất hướng phát triển: Đưa ra nhận xét, phân tích nhữngu – nhược điểm của các mô hình đã thử nghiệm. So sánh hiệu quả mô hình với các kết quảrong các công trình nghiên cứu khác. Đề xuất hướng phát triển tiếp theo như mở rộng phạmi cảm xúc, áp dụng cho các lĩnh vực khác như y tế, giáo dục, chăm sóc khách hàng,...

### Bố cục đề tài

Chương 1: Giới thiệu đề tài: Lý do chọn đề tài, mục tiêu đề tài, đối tượng và phạmi nghiên cứu, phương pháp nghiên cứu, cấu trúc báo cáo.

Chương 2: Cơ sở lý thuyết: Tổng quan về xử lý ngôn ngữ tự nhiên (NLP), khái niệmà vai trò của phân tích cảm xúc (Sentiment Analysis), các kỹ thuật biểu diễn văn bản, tổnguan về học máy (Machine Learning) và học sâu (Deep Learning), các mô hình phổ biếnùng trong phân tích cảm xúc.

Chương 3: Phân tích và thiết kế hệ thống: Phân tích bài toán nhận diện cảm xúcrong văn bản tiếng Việt, yêu cầu hệ thống (chức năng và phi chức năng), thiết kế quy trìnhử lý dữ liệu, thiết kế kiến trúc hệ thống (mô hình tổng thể, các thành phần chính), mô hìnhuồng dữ liệu và xử lý, lựa chọn công nghệ.

Chương 4: Thực nghiệm và triển khai: Thu thập và xử lý dữ liệu văn bản tiếng Việt,iền xử lý, vector hóa văn bản, huấn luyện các mô hình học máy (ML) và học sâu (DL), đánhiá mô hình bằng các thước đo, so sánh kết quả giữa các mô hình, tinh chỉnh và lựa chọn môình tối ưu.

Chương 5: Xây dựng ứng dụng thử nghiệm: Mục tiêu và chức năng ứng dụng, thiếtế giao diện người dùng, kết nối mô hình với hệ thống phân tích phản hồi từ thương mại điệnử, mô phỏng quy trình, thử nghiệm kết quả ứng dụng thực tế.hương 6: Đánh giá và kết luận: Tổng kết kết quả đạt được, đánh giá hiệu quả môình và hệ thống, khó khăn, hạn chế trong quá trình thực hiện, hướng phát triển và mở rộngrong tương lai.

Tài liệu tham khảo, Phụ lục.

### Tài liệu tham khảo

Các tài liệu tham khảo sử dụng trong đề tài được lựa chọn từ nhiều nguồn uy tín, baoồm bài báo khoa học quốc tế, tài liệu nghiên cứu trong nước, sách chuyên ngành và cácguồn dữ liệu, công cụ thực tế. Những tài liệu này đóng vai trò quan trọng trong việc xâyựng cơ sở lý thuyết, lựa chọn mô hình và định hướng triển khai hệ thống. Một số tài liệuham khảo hiện tại:
