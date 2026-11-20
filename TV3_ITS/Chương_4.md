# **Chương 4\. Phân tích và so sánh các công nghệ nhận diện**

## **4.1. Xây dựng tiêu chí so sánh: định nghĩa từng tiêu chí, nhóm tiêu chí** 

Để có cơ sở khoa học và định lượng trong việc đánh giá, lựa chọn công nghệ nhận diện phương tiện phục vụ hệ thống Thu phí điện tử không dừng (ETC) và Quản lý nhu cầu giao thông (ERP), các tiêu chí so sánh được xây dựng và phân thành ba nhóm chính 

A. Nhóm tiêu chí Hiệu năng & Kỹ thuật (Technical & Operational Performance) 

* Độ chính xác nhận diện (Recognition Accuracy) : Tỷ lệ phần trăm phương tiện được định danh đúng thông tin (chuỗi mã ID thẻ/OBU hoặc chuỗi ký tự biển số xe) trên tổng số lượt phương tiện lưu thông qua vùng kiểm soát trong điều kiện tiêu chuẩn và ngoại cảnh bất lợi   
* Tốc độ xử lý & Độ trễ thời gian thực (Processing Speed & Latency) : Thời gian tính bằng millisecond kể từ thời điểm phương tiện tiến vào vùng quét đến khi hệ thống trích xuất xong dữ liệu định danh, xác thực tài khoản và phát lệnh điều khiển hạ tầng   
* Khả năng thích ứng môi trường (Environmental Reliability) : Khả năng duy trì độ chính xác và độ bền của thiết bị hiện trường dưới tác động của điều kiện thời tiết khắc nghiệt (mưa lớn, sương mù, nhiệt độ cao, ánh sáng chói hoặc đao phủ bóng tối đêm)   
* Tốc độ phương tiện tối đa hỗ trợ (Maximum Vehicle Speed) : Vận tốc giới hạn của phương tiện mà tại đó công nghệ nhận diện vẫn đảm bảo tỷ lệ đọc/chụp chính xác, đặc biệt quan trọng đối với mô hình Thu phí Tự do Đa làn (Multi-Lane Free-Flow \- MLFF) 

B. Nhóm tiêu chí Chi phí & Khả năng triển khai (Financial & Implementation Feasibility) 

* Chi phí đầu tư hạ tầng hiện trường (CAPEX \- Roadside Infrastructure) : Tổng chi phí mua sắm, lắp đặt khung gantry, đầu đọc, camera AI, cảm biến, tủ điều khiển biên và xây dựng hạ tầng kỹ thuật dân dụng   
* Chi phí thiết bị trên phương tiện (CAPEX \- In-Vehicle Hardware) : Chi phí phát hành, dán thẻ RFID thụ động hoặc trang bị bộ thiết bị thông minh (IU/OBU) trên từng phương tiện giao thông   
* Chi phí vận hành & bảo trì (OPEX \- Operation & Maintenance) : Chi phí duy trì đường truyền viễn thông, bảo dưỡng phần cứng, vận hành phần mềm máy chủ, tiêu thụ điện năng và xử lý lỗi hỏng hóc kỹ thuật phát sinh 

C. Nhóm tiêu chí An ninh, Pháp lý & Quản trị (Security, Legal & Governance) 

* Tính chống gian lận & Giá trị pháp lý bằng chứng (Anti-Fraud & Legal Evidence) : Khả năng tự phát hiện các hành vi gian lận (như tháo dán thẻ, sử dụng biển số giả, mạo danh tài khoản) và cung cấp đầy đủ hình ảnh/video bằng chứng đạt chuẩn pháp lý phục vụ xử phạt   
* Chuẩn hóa & Khả năng liên thông (Standardization & Interoperability) : Chi phí phát hành, dán thẻ RFID thụ động hoặc trang bị bộ thiết bị thông minh (IU/OBU) trên từng phương tiện giao thông   
* Bảo mật dữ liệu & Quyền riêng tư (Data Security & Privacy) : Chi phí duy trì đường truyền viễn thông, bảo dưỡng phần cứng, vận hành phần mềm máy chủ, tiêu thụ điện năng và xử lý lỗi hỏng hóc kỹ thuật phát sinh 

## **4.2. Ma trận so sánh ba phương án: RFID, ANPR/LPR, kết hợp**

Nhóm tiêu chí : gồm 3 tiêu chí là Hiệu năng & Kỹ thuật , Chi phí & Triển khai và An ninh & Quản trị 

Tiêu chí cụ thể : gồm 10 tiêu chí : Độ chính xác , Tốc độ xử lý , Thích ứng môi trường , Vận tốc hỗ trợ , CAPEX Hạ tầng hiện trường , CAPEX Thiết bị trên xe  , OPEX Vận hành & Bảo trì  , Tính chống gian lận  , Bằng chứng pháp lý  , Chuẩn hóa & Liên thông 

Phương án 1: RFID thuần túy 

Phương án 2: ANPR/LPR thuần túy (Camera AI) 

Phương án 3: Kết hợp (RFID \+ ANPR/LPR) 

| Nhóm tiêu chí  | Tiêu chí cụ thể  | Phương án 1: RFID thuần túy  | Phương án 2: ANPR/LPR thuần túy (Camera AI)  | Phương án 3: Kết hợp (RFID \+ ANPR/LPR)  |
| :---- | :---- | :---- | :---- | :---- |
| Hiệu năng & Kỹ thuật  | Độ chính xác  | Rất cao (\>99.5%) với thẻ hợp lệ.  | Khá \- Cao (90% – 97%), phụ thuộc chất lượng biển số & thời tiết.  | Cực cao (99.9%) nhờ cơ chế đối chiếu xác thực kép.  |
|  | Tốc độ xử lý  | Cực nhanh (\< 10 ms), dữ liệu dạng chuỗi ID nhẹ .  | Trung bình (50 \- 200 ms), yêu cầu xử lý thuật toán AI hình ảnh .  | Rất nhanh, phân tách luồng xử lý ưu tiên RFID.  |
|  | Thích ứng môi trường  | Không bị ảnh hưởng bởi ánh sáng, thời tiết, bụi bẩn  | Nhạy cảm với mưa bão, sương mù, chói đèn pha, biển số mờ/bẩn  | Rất cao, RFID bù đắp sai số cho Camera khi thời tiết xấu |
|  | Vận tốc hỗ trợ  | Rất cao (\> 160 km/h) .  | Cao (120 \- 150 km/h), đòi hỏi Camera màn trập tốc độ cao .  | Rất cao (\> 160 km/h), đáp ứng hoàn hảo MLFF .  |
| Chi phí & Triển khai  | CAPEX Hạ tầng hiện trường  | Trung bình (Đầu đọc RFID, Ăng-ten, Cảm biến) .  | Trung bình \- Cao (Camera AI chuyên dụng, bộ xử lý biên AI) .  | Cao (Tích hợp cả hai dòng thiết bị hiện trường) .  |
|  | CAPEX Thiết bị trên xe  | Thấp (Thẻ thụ động RFID giá rẻ, dán 1 lần) .  | Không tốn chi phí (Không yêu cầu thiết bị/thẻ dán trên xe) .  | Thấp (Chỉ yêu cầu thẻ RFID dán trên xe) .  |
|  | OPEX Vận hành & Bảo trì  | Thấp, thiết bị RFID có độ bền cao, ít hỏng hóc .  | Trung bình (Bảo trì ống kính, đèn IR, nâng cấp thuật toán AI) .  | Trung bình \- Cao (Bảo trì song song hai hệ thống cảm biến) .  |
| An ninh & Quản trị  | Tính chống gian lận  | Thấp (Không phát hiện được biển số giả hoặc tháo dán thẻ trái phép) .  | Cao (Lưu trữ ảnh thực tế phương tiện và biển số) .  | Tuyệt đối (So khớp mã ID thẻ và biển số thực tế thời gian thực) .  |
|  | Bằng chứng pháp lý  | Không có (Chỉ lưu vết dữ liệu mã định danh số) .  | Đầy đủ (Có ảnh toàn cảnh, ảnh cận cảnh biển số xe) .  | Đầy đủ & Vững chắc (Có cả dữ liệu RFID và ảnh bằng chứng LPR) .  |
|  | Chuẩn hóa & Liên thông  | Chuẩn hóa cao (ISO/IEC 18000-63) .  | Chuẩn hóa cao (TCVN 14464-1/2:2025) .  | Chuẩn hóa toàn diện theo khung TCVN ITS quốc gia .  |

## **4.3. Đánh giá ưu điểm và hạn chế của từng phương án**

### **4.3.1. Phương án 1: Công nghệ RFID thuần túy** 

Ưu điểm: 

* Tốc độ và tính ổn định cực cao : Sóng vô tuyến UHF truyền nhận dữ liệu định danh mã EPC/ID gần như tức thời với dung lượng gói tin rất nhẹ   
* Chi phí thiết bị trên phương tiện rất thấp : Thẻ RFID thụ động có chi phí sản xuất rẻ, không dùng pin, tuổi thọ kéo dài theo đời xe   
* Khả năng hoạt động độc lập với môi trường : Không bị suy giảm hiệu năng do điều kiện thiếu sáng, thời tiết mưa bão hay bụi bẩn gầm xe/kính lái 

Hạn chế:

* Thiếu năng lực giám sát hình ảnh : RFID không thể chụp ảnh phương tiện, do đó không cung cấp được bằng chứng thị giác phục vụ công tác xử phạt nguội hoặc đăng kiểm   
* Rủi ro gian lận phương tiện : Hệ thống không thể tự xác minh xem thẻ RFID có đang dán đúng trên phương tiện đăng ký ban đầu hay không (nguy cơ tháo dán thẻ trái phép hoặc dùng xe khác mang thẻ) 

### **4.3.2. Phương án 2: Công nghệ ANPR/LPR thuần túy (AI Camera)** 

Ưu điểm: 

* Không đòi hỏi can thiệp vào phương tiện : Người dân không cần mua thiết bị hay dán thẻ lên xe, giúp loại bỏ rào cản tâm lý xã hội và chi phí phát hành thiết bị đầu cuối   
* Cung cấp bằng chứng pháp lý hoàn chỉnh : Ảnh chụp toàn cảnh và cận cảnh biển số xe có độ phân giải cao là căn cứ pháp lý vững chắc cho công tác xử phạt vi phạm hành chính và truy vết an ninh   
* Linh hoạt trong ứng dụng đô thị : Dễ dàng tích hợp vào hệ thống camera giám sát giao thông sẵn có tại các giao lộ, bãi đỗ xe và điểm kiểm soát đô thị 

Hạn chế: 

* Phụ thuộc vào chất lượng biển số và thời tiết : Độ chính xác bị suy giảm nghiêm trọng khi biển số xe bị bẩn, mờ, dán che cố tình, hoặc trong điều kiện sương mù dày đặc và mưa lớn   
* Yêu cầu năng lực tính toán và đường truyền lớn : Việc xử lý hình ảnh thời gian thực yêu cầu các bộ xử lý biên AI (Edge AI) đắt tiền và băng thông mạng lớn để truyền hình ảnh/video về trung tâm 

### **4.3.3. Phương án 3: Phương án kết hợp (RFID \+ ANPR/LPR)** 

Ưu điểm: 

Phát huy tối đa ưu thế tương hỗ : RFID đóng vai trò công nghệ xác thực giao dịch chính với tốc độ siêu nhanh; ANPR/LPR đóng vai trò giám sát, xác minh tính trùng khớp và cung cấp bằng chứng hình ảnh 

Chống thất thu và phát hiện gian lận triệt để : Khi mã ID RFID và biển số xe ANPR chụp được không khớp nhau (Mismatch), hệ thống lập tức báo động giao dịch bất thường để xử lý vi phạm 

Đảm bảo vận hành liên tục ngay cả khi một phân hệ gặp sự cố : Nếu camera bị che khuất tầm nhìn, RFID vẫn thực hiện giao dịch thanh toán; ngược lại, nếu thẻ RFID hỏng, ANPR/LPR vẫn ghi nhận lượt xe để tra cứu tài khoản trừ tiền trả sau 

Hạn chế: 

Chi phí đầu tư và vận hành cao : Đòi hỏi trang bị đồng thời cả hệ thống đầu đọc RFID và camera AI tại mỗi làn/cổng thu phí 

Yêu cầu độ phức tạp về tích hợp phần mềm : Phần mềm điều khiển trạm phải xử lý thuật toán đồng bộ thời gian (Time-synchronization) chính xác để ghép nối luồng dữ liệu RFID và luồng ảnh ANPR của cùng một phương tiện ở tốc độ cao 

## **4.4. Điều kiện lựa chọn công nghệ phù hợp theo bối cảnh triển khai**

Việc lựa chọn công nghệ nhận diện không thể áp dụng một công thức duy nhất cho mọi hạ tầng, mà phải căn cứ vào bối cảnh vận hành, vận tốc dòng xe và mục tiêu quản lý cụ thể 

Tuyến đường cao tốc liên tỉnh / Hành lang vận tải tốc độ cao (Mô hình MLFF) 

* Đặc điểm bối cảnh : Phương tiện di chuyển với vận tốc rất cao (80 \- 120 km/h), mật độ lưu thông lớn, yêu cầu xử lý giao dịch tức thì và đòi hỏi tính chống thất thu tuyệt đối   
* Công nghệ nên áp dụng : Phương án kết hợp RFID \+ ANPR/LPR   
* Lý giải cho việc trên : RFID đảm bảo tỷ lệ đọc thành công ở tốc độ cao mà không gây độ trễ, trong khi ANPR/LPR chụp ảnh làm căn cứ xử lý các trường hợp tài khoản không đủ tiền, xe dùng biển số giả hoặc cố tình gian lận 

Khu vực nội đô / Vùng thu phí chống ùn tắc (Congestion Pricing / ERP 2.0) 

* Đặc điểm bối cảnh : Mật độ giao thông cực kỳ phức tạp, nhiều phương tiện cắt ngang, không gian hạ tầng hạn chế không cho phép xây dựng các khung gantry vật lý cồng kềnh làm mất mỹ quan đô thị   
* Công nghệ nên áp dụng : Định vị Vệ tinh (GNSS) kết hợp OBU thế hệ mới và Camera ANPR AI hỗ trợ tại điểm nóng   
* Lý giải cho việc trên : Mô hình ERP 2.0 dựa trên GNSS cho phép khởi tạo các "cổng ảo" trên bản đồ số mà không tốn chi phí xây dựng hạ tầng vật lý . Các camera ANPR AI lắp tại các lối ra/vào điểm nóng đóng vai trò kiểm soát an ninh và hỗ trợ phạt nguội 

Giao thông tĩnh / Bãi đỗ xe, Bến xe, Sân bay, Cảng biển 

* Đặc điểm bối cảnh : Phương tiện di chuyển với vận tốc thấp hoặc dừng đỗ (0 \- 20 km/h), đối tượng tham gia bao gồm cả xe vãng lai chưa dán thẻ   
* Công nghệ nên áp dụng : ANPR/LPR thuần túy (Camera AI) hoặc RFID tầm ngắn/BLE   
* Lý giải cho việc trên : Tốc độ xe thấp giúp camera AI nhận diện biển số đạt độ chính xác tiệm cận 100% . Việc sử dụng ANPR/LPR giúp xe vãng lai không cần dán thẻ vẫn có thể vào ra và thanh toán tự động qua ứng dụng/ví điện tử liên kết
