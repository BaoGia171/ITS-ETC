# Chương 3. Các công nghệ nhận diện phương tiện trong ETC

## **3.1. Công nghệ RFID: nguyên lý, thành phần, quy trình hoạt động**

### **3.1.1 Khái niệm và Nguyên lý hoạt động**

Nhận diện qua tần số vô tuyến (Radio Frequency Identification - RFID) là công nghệ truyền thông không dây cho phép định danh tự động đối tượng dựa trên sóng vô tuyến. Trong các hệ thống thu phí tự động không dừng (ETC), RFID sử dụng dải tần số siêu cao (Ultra High Frequency - UHF, 860 MHz – 960 MHz) với nguyên lý bức xạ điện từ và tán xạ ngược (Electromagnetic Backscatter Coupling)

Khi phương tiện di chuyển vào vùng phủ sóng vô tuyến của ăng-ten hiện trường (Reader Antenna), thẻ RFID thụ động (Passive Tag) dán trên phương tiện sẽ thu nhận năng lượng sóng điện từ để kích hoạt vi mạch nội tại, sau đó phản hồi lại tín hiệu mang chuỗi mã định danh duy nhất (EPC/ID) về đầu đọc.

### **3.1.2 Thành phần cơ bản của hệ thống RFID trong ETC**

- Thẻ định danh RFID (RFID Tag / Transponder) : Thẻ thụ động không cần nguồn pin riêng, gồm chip vi mạch lưu trữ mã ID định danh xe và mạch ăng-ten màng mỏng. Thẻ được thiết kế theo cơ chế chống bóc dán (tự phá hủy mạch khi cố tình tháo gỡ) để phòng chống gian lận.

- Thiết bị đầu đọc và Ăng-ten hiện trường (RFID Reader & Antenna) : Phát sóng vô tuyến liên tục và thu nhận dữ liệu phản hồi từ thẻ xe ở khoảng cách từ 3 m – 10 m.

- Bộ điều khiển trạm/làn (Lane Controller) : Tiếp nhận dữ liệu từ đầu đọc RFID, kiểm tra tính hợp lệ của giao dịch và truyền thông điệp về trung tâm xử lý dữ liệu.

### **3.1.3. Pipeline xử lý nhận diện phương tiện bằng RFID.**

Pipeline xử lý nhận diện phương tiện bằng công nghệ RFID trong hệ thống Thu phí Tự động Không dừng (ETC) là một chuỗi các bước kỹ thuật tuần tự, khép kín từ khâu kích hoạt cảm biến hiện trường, trao đổi dữ liệu vô tuyến cho đến xác thực thanh toán và truyền dữ liệu về trung tâm

Sơ đồ tổng quan luồng xử lý qua 6 giai đoạn

<table>
<tr>
<td><p><strong>BẮT ĐẦU: PHƯƠNG TIỆN TIẾN VÀO LÀN</strong></p><p>Phương tiện đi vào vùng nhận diện của trạm ETC</p></td>
</tr>
</table>

**↓**

<table>
<tr>
<td><p><strong>GIAI ĐOẠN 1 — PHÁT HIỆN PHƯƠNG TIỆN &amp; KHỞI TẠO PHIÊN</strong></p><p>Cảm biến vòng từ / Laser phát hiện xe → Kích hoạt bộ điều khiển làn</p></td>
</tr>
</table>

**↓**

<table>
<tr>
<td><p><strong>GIAI ĐOẠN 2 — TRUYỀN THÔNG VÔ TUYẾN &amp; ĐỌC THẺ RFID</strong></p><p>Ăng-ten phát sóng UHF 860–960 MHz → Kích hoạt thẻ thụ động → Nhận mã EPC/ID</p></td>
</tr>
</table>

**↓**

<table>
<tr>
<td><p><strong>GIAI ĐOẠN 3 — GIẢI MÃ &amp; TIỀN XỬ LÝ DỮ LIỆU TẠI LÀN</strong></p><p>Giải mã tín hiệu → Kiểm tra lỗi CRC → Khử trùng lặp Anti-collision</p></td>
</tr>
</table>

**↓**

<table>
<tr>
<td><p><strong>GIAI ĐOẠN 4 — XÁC THỰC &amp; KHẤU TRỪ TÀI KHOẢN</strong></p><p>Tra cứu CSDL tài khoản giao thông → Kiểm tra số dư → Khấu trừ phí tự động</p></td>
</tr>
</table>

**↓**

<table>
<tr>
<td><p><strong>GIAI ĐOẠN 5 — XÁC THỰC KÉP (ANPR) &amp; ĐIỀU KHIỂN HẠ TẦNG</strong></p><p>So khớp với Camera ANPR → Phát lệnh mở Barie / Ghi nhận MLFF</p></td>
</tr>
</table>

**↓**

<table>
<tr>
<td><p><strong>GIAI ĐOẠN 6 — ĐÓNG GÓI THÔNG ĐIỆP &amp; TRUYỀN VỀ TRUNG TÂM (TOC)</strong></p><p>Mã hóa BER chuẩn AP-DATEX / SNMP, gán OID → Truyền về Trung tâm TOC</p></td>
</tr>
</table>

### **3.1.4. Minh họa quy trình hoạt động và xử lý lỗi.**

**PIPELINE PHỐI HỢP RFID – ANPR/LPR TRONG HỆ THỐNG ETC**

Luồng nhận diện song song • Đối chiếu định danh • Xử lý ngoại lệ

<table>
<tr>
<td colspan="3"><p><strong>BẮT ĐẦU — PHƯƠNG TIỆN ĐI VÀO LÀN</strong></p><p>Cảm biến phát hiện xe → khởi tạo phiên nhận diện / mã lượt</p></td>
</tr>
<tr>
<td><p><strong>↓</strong></p></td>
<td></td>
<td><p><strong>↓</strong></p></td>
</tr>
<tr>
<td><p><strong>NHÁNH 1 · RFID (UHF)</strong></p><p>Đọc EPC/ID từ thẻ → tra cứu mã xe</p></td>
<td></td>
<td><p><strong>NHÁNH 2 · ANPR/LPR (Camera)</strong></p><p>Chụp ảnh → OCR biển số → tra cứu mã xe</p></td>
</tr>
<tr>
<td><p><strong>↓</strong></p></td>
<td></td>
<td><p><strong>↓</strong></p></td>
</tr>
<tr>
<td><p><strong>KẾT QUẢ RFID</strong></p><p>Tìm thấy mã xe / Không đọc được / Không đăng ký</p></td>
<td></td>
<td><p><strong>KẾT QUẢ ANPR</strong></p><p>Tìm thấy mã xe / Không đọc được / Không đăng ký</p></td>
</tr>
<tr>
<td><p><strong>↓</strong></p></td>
<td></td>
<td><p><strong>↓</strong></p></td>
</tr>
<tr>
<td colspan="3"><p><strong>ĐỒNG BỘ THEO CÙNG LƯỢT XE VÀ ĐỐI CHIẾU</strong></p><p>So sánh mã xe mà hai nguồn tra cứu được — không so sánh trực tiếp EPC với biển số</p></td>
</tr>
<tr>
<td><p><strong>↓</strong></p></td>
<td></td>
<td><p><strong>↓</strong></p></td>
</tr>
<tr>
<td><p><strong>TRƯỜNG HỢP A · HAI NGUỒN TRÙNG KHỚP</strong></p><p>RFID và ANPR cùng xác định một mã xe</p></td>
<td></td>
<td><p><strong>TRƯỜNG HỢP B · LỖI / KHÔNG KHỚP</strong></p><p>Thiếu dữ liệu, không tra cứu được hoặc hai mã xe khác nhau</p></td>
</tr>
<tr>
<td><p><strong>↓</strong></p></td>
<td></td>
<td><p><strong>↓</strong></p></td>
</tr>
<tr>
<td><p><strong>XÁC THỰC HỢP LỆ VỀ MẶT ĐỐI CHIẾU</strong></p><p>Chuyển tiếp kiểm tra tài khoản và điều kiện thu phí</p></td>
<td></td>
<td><p><strong>CHUYỂN XÁC MINH / LẬP HỒ SƠ NGOẠI LỆ</strong></p><p>Lưu chứng cứ RFID, ảnh/biển số và mã lượt; không tự động kết luận gian lận</p></td>
</tr>
<tr>
<td><p><strong>↓</strong></p></td>
<td></td>
<td><p><strong>↓</strong></p></td>
</tr>
<tr>
<td colspan="3"><p><strong>GHI NHẬN KẾT QUẢ &amp; GỬI VỀ HỆ THỐNG TRUNG TÂM (TOC)</strong></p><p>Trạng thái nhận diện / giao dịch hoặc hồ sơ ngoại lệ → lưu vết và truyền dữ liệu</p></td>
</tr>
</table>

## 3.2. Công nghệ nhận diện biển số bằng hình ảnh (ANPR/LPR): nguyên lý, thành phần, quy trình hoạt động

### **3.2.1 Khái niệm và Nguyên lý hoạt động** **:**

Nhận diện biển số xe tự động (Automatic Number Plate Recognition - ANPR / License Plate Recognition - LPR) là công nghệ xử lý ảnh và Trí tuệ Nhân tạo (AI) giúp trích xuất chuỗi ký tự biển số từ hình ảnh chụp hoặc luồng video thời gian thực.

ANPR/LPR ứng dụng các mô hình học sâu (Deep Learning) và Mạng thần kinh nhân tạo (CNN) để phân tích cấu trúc hình ảnh: tự động định vị khung biển số, phân đoạn ký tự và nhận dạng quang học (OCR) với độ chính xác cao trong mọi điều kiện ánh sáng, góc chụp hay thời tiết.

### **3.2.2 Thành phần cơ bản của hệ thống ANPR/LPR**

- Camera AI chuyên dụng hiện trường : Tích hợp cảm biến độ phân giải cao, tốc độ màn hình trập (Shutter Speed) cực nhanh, cùng hệ thống đèn chiếu sáng hồng ngoại (IR Illuminators) giúp chống chói từ đèn pha xe và bắt nét tốt vào đêm.

- Bộ xử lý biên AI (Edge AI Processing Unit) : Thiết bị tính toán đặt trực tiếp tại tủ kỹ thuật bên đường, thực thi mô hình AI để nhận diện biển số tại chỗ, giảm thiểu độ trễ đường truyền.

- Máy chủ / Phần mềm quản lý LPR trung tâm : Lưu trữ ảnh toàn cảnh, ảnh cận cảnh biển số, thời gian xe qua trạm và thực hiện đối chiếu biển số với Cơ sở dữ liệu đăng ký phương tiện quốc gia

### **3.2.3. Pipeline xử lý ảnh và nhận diện biển số.**

### **3.2.4. Minh họa quy trình hoạt động và xử lý lỗi**

## **3.3. Phối hợp RFID và ANPR/LPR trong nhận diện phương tiện**

### **3.3.1 Sự cần thiết của cơ chế phối hợp song song**

- Nhược điểm của RFID riêng lẻ : RFID có tốc độ đọc cực nhanh nhưng không thể tự xác minh xem thẻ RFID có đang dán đúng trên chính phương tiện đăng ký ban đầu hay không (nguy cơ dùng biển số giả hoặc tháo dán thẻ trái phép)

- Nhược điểm của ANPR/LPR riêng lẻ : ANPR/LPR không yêu cầu thiết bị trên xe nhưng lại chịu ảnh hưởng bởi yếu tố môi trường (biển số bị mờ, dán che, bẩn, chói sáng hoặc thời tiết sương mù/mưa lớn)

- Giải pháp : Kết hợp **RFID + ANPR/LPR** tạo nên cơ chế **xác thực kép (Dual Verification)**, đảm bảo tính chính xác và an ninh tuyệt đối cho giao dịch ETC

### **3.3.2. Pipeline xử lý nhận diện phối hợp.**

### **3.3.3. Cơ chế đối chiếu và xác thực kết quả.**

- Xác thực đối chiếu, kiểm tra sự trùng khớp giữa mã RFID và biển số.

### 3.3.4. Xử lý ngoại lệ và phát hiện thông tin không khớp.

- Xử lý ngoại lệ & Chống gian lận :

Giao dịch hợp lệ :

Thẻ hỏng / Chưa dán thẻ :

Phát hiện thông tin không khớp và chuyển xác minh  :

## **3.4. Các hướng công nghệ khác trong thu phí và nhận diện phương tiện:**

**Công nghệ Giao tiếp Tầm ngắn Chuyên dụng (DSRC)**

- Vận hành trên dải tần 2.4 GHz hoặc 5.8/5.9 GHz giữa Bộ Thiết bị trên xe (In-vehicle Unit - IU) và các cổng gantry hiện trường.

- Cho phép trao đổi dữ liệu dung lượng lớn và giao dịch trực tiếp trên thẻ thông minh lưu trữ giá trị (CashCard). Tuy nhiên, chi phí thiết bị IU khá đắt và phụ thuộc vào khung gantry vật lý cồng kềnh\]. (Áp dụng tại Singapore ERP 1.0).

**Công nghệ Thu phí dựa trên Định vị Vệ tinh (GNSS Tolling / Satellite ERP)**

- Phương tiện bắt buộc lắp Thiết bị Trên xe thế hệ mới (On-Board Unit - OBU) tích hợp định vị vệ tinh GNSS và viễn thông di động.

- Tự động xác định tọa độ xe và tính phí khi xe đi qua các "cổng ảo" (Virtual Gantries) định nghĩa trên bản đồ số mà không cần xây dựng gantry vật lý.

- Kết hợp với vạch sơn mặt đường (mô hình "Blue Carpet" hoặc hình bầu dục xanh) và biển báo "ERP Charge Zone" làm dấu hiệu thị giác cảnh báo vùng tính phí.

- Mở rộng cung cấp các dịch vụ giá trị gia tăng như cảnh báo giao thông thời gian thực, cảnh báo khu vực trường học, tự động trả phí đỗ xe và phạt nguội vi phạm giao thông. (Tiêu biểu là mô hình ERP 2.0 tại Singapore).

**Hệ thống Giao thông Kết nối & Hợp tác (C-ITS) và V2X**

- Ứng dụng truyền thông V2X (Vehicle-to-Everything) tần số 5.9 GHz (dùng DSRC IEEE 802.11p / C-V2X PC5 với độ trễ dưới 10 ms) và Network V2X (4G/5G).

- Cho phép các phương tiện tương tác trực tiếp với hạ tầng (V2I) và phương tiện khác (V2V), hỗ trợ xác thực giao dịch thu phí đa làn tự do hoàn toàn và điều tiết dòng xe theo thời gian thực.

**Công nghệ Nhận diện BLE (Bluetooth Low Energy) & Smartphone App**

Sử dụng sóng Bluetooth tầm ngắn kết nối giữa Smartphone/OBU và cảm biến hiện trường, áp dụng cho thu phí đỗ xe đô thị và các điểm kiểm soát giao thông thông minh.

## 3.5. Thực tiễn áp dụng tại Việt Nam

**Hiện trạng công nghệ chủ đạo**

- Việt Nam đã hoàn thành chuẩn hóa và triển khai đồng bộ công nghệ RFID dải tần UHF (tiêu chuẩn ISO/IEC 18000-63) kết hợp Camera ANPR/LPR AI trên toàn bộ hệ thống đường cao tốc và quốc lộ.

- Người dân sử dụng thẻ định danh RFID (ePass hoặc VETC) dán trên kính lái/đèn xe liên kết với tài khoản giao thông.

**Lộ trình chuyển đổi sang Thu phí Tự do (Multi-Lane Free-Flow - MLFF)**

- Áp dụng mô hình quá độ thông minh trên các tuyến cao tốc Bắc - Nam phía Đông: Đầu vào đa làn tự do (không có barie) và điều tiết đầu ra đơn làn (vẫn duy trì barie).

- Mô hình này cho phép huấn luyện các thuật toán Trí tuệ Nhân tạo (Edge AI) nhận diện biển số và xác thực giao dịch ở tốc độ cao phía trên dòng xe đang di chuyển, đồng thời kiểm soát rủi ro tài khoản không đủ cân đối trước khi hành lang pháp lý cho phép bỏ hoàn toàn barie.

**Mở rộng ETC trong hạ tầng giao thông đô thị**

- Mở rộng ứng dụng thu phí ETC sang các điểm đỗ xe đô thị, bến xe, lòng đường và sân bay.

- Hà Nội đưa vào vận hành thí điểm Trung tâm Điều hành Giao thông Thông minh (TOC) tại Kim Mã tích hợp camera AI xử lý vi phạm và thu phí đỗ xe tự động.

- Hải Phòng triển khai hệ thống gần 200 camera AI từ tháng 2/2025 TP. Hồ Chí Minh đầu tư hạ tầng trung tâm dữ liệu siêu quy mô phục vụ điều hành đô thị thông minh.
