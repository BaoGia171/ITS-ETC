# **Chương 3. Các công nghệ nhận diện phương tiện trong ETC**

## **3.1. Công nghệ RFID: nguyên lý, thành phần, quy trình hoạt động**

### **3.1.1 Khái niệm và Nguyên lý hoạt động**

RFID (Radio Frequency Identification) là công nghệ nhận diện bằng sóng vô tuyến. Trong hệ thống ETC, đầu đọc nhận mã định danh từ thẻ gắn trên xe để tra cứu phương tiện đã đăng ký.

Với thẻ RFID thụ động, ăng-ten phát sóng để cấp năng lượng cho thẻ. Thẻ phản hồi mã EPC/ID về đầu đọc bằng cơ chế tán xạ ngược. Mã này được chuyển đến bộ điều khiển làn để xử lý.

### **3.1.2 Thành phần cơ bản của hệ thống RFID trong ETC**

Các thành phần phục vụ nhận diện RFID trong ETC có thể trình bày theo ba nhóm gồm thẻ trên phương tiện, thiết bị tại trạm/làn và hệ thống phần mềm, máy chủ.

**a. Thẻ định danh RFID trên phương tiện**

Thẻ RFID thụ động được dán trên kính lái hoặc đèn xe theo hướng dẫn của nhà cung cấp. Thẻ gồm vi mạch và ăng-ten, sử dụng năng lượng từ sóng của đầu đọc để phản hồi mã định danh.

Mã thẻ được liên kết với thông tin xe và tài khoản giao thông trong hệ thống. Thiết kế chống bóc dán giúp hạn chế việc chuyển thẻ sang xe khác.

**b. Thiết bị hiện trường tại trạm/làn**

Đầu đọc và ăng-ten RFID phát sóng, nhận tín hiệu phản hồi và đọc mã thẻ. Thiết bị được bố trí phù hợp với vùng nhận diện của làn, có thể lắp trên giá đỡ hoặc khung gantry tùy thiết kế trạm.

Cảm biến phát hiện phương tiện xác định thời điểm xe đi vào vùng nhận diện để khởi tạo lượt xử lý. Bộ điều khiển làn tiếp nhận dữ liệu đọc thẻ, gộp các lần đọc trùng trong cùng lượt và chuyển dữ liệu để tra cứu phương tiện.

Camera ANPR/LPR cung cấp ảnh và biển số để hỗ trợ đối chiếu khi triển khai phương án phối hợp.

**c. Hệ thống phần mềm và máy chủ**

Phần mềm quản lý liên kết mã thẻ với thông tin phương tiện, tài khoản và lịch sử lượt xe. Dữ liệu này phục vụ tra cứu, kiểm tra kết quả nhận diện và xử lý các trường hợp phát sinh.

Máy chủ tiếp nhận dữ liệu từ trạm/làn, lưu kết quả và hỗ trợ xử lý giao dịch. Trong phạm vi nhận diện, đầu ra cần xác định được phương tiện tương ứng với mã thẻ hoặc ghi nhận trường hợp cần xác minh.

### **3.1.3. Pipeline xử lý nhận diện phương tiện bằng RFID.**

Quy trình nhận diện bằng RFID bắt đầu khi xe đi vào làn và kết thúc khi hệ thống trả kết quả tra cứu phương tiện. Các bước xử lý được trình bày dưới đây.

Sơ đồ luồng xử lý nhận diện RFID qua 5 bước

<table>
<tr>
<td><p><strong>BẮT ĐẦU</strong></p><p>Phương tiện đi vào vùng nhận diện của làn ETC</p></td>
</tr>
</table>

**↓**

<table>
<tr>
<td><p><strong>BƯỚC 1 — PHÁT HIỆN XE VÀ KHỞI TẠO LƯỢT</strong></p><p>Cảm biến phát hiện xe → tạo mã lượt nhận diện</p></td>
</tr>
</table>

**↓**

<table>
<tr>
<td><p><strong>BƯỚC 2 — ĐỌC MÃ THẺ RFID</strong></p><p>Ăng-ten phát sóng → thẻ phản hồi → đầu đọc nhận mã EPC/ID</p></td>
</tr>
</table>

**↓**

<table>
<tr>
<td><p><strong>BƯỚC 3 — KIỂM TRA DỮ LIỆU ĐỌC</strong></p><p>Kiểm tra dữ liệu thu nhận → gộp các lần đọc cùng thẻ trong một lượt</p></td>
</tr>
</table>

**↓**

<table>
<tr>
<td><p><strong>BƯỚC 4 — TRA CỨU PHƯƠNG TIỆN</strong></p><p>Dùng mã thẻ để tra cứu trong danh sách phương tiện đăng ký</p></td>
</tr>
</table>

**↓**

<table>
<tr>
<td><p><strong>BƯỚC 5 — TRẢ KẾT QUẢ NHẬN DIỆN</strong></p><p>Trả mã xe nếu tìm thấy hoặc trạng thái cần xác minh → ghi nhận theo mã lượt</p></td>
</tr>
</table>

### **3.1.4. Minh họa quy trình hoạt động và xử lý lỗi.**

**MINH HỌA NHẬN DIỆN VÀ XỬ LÝ LỖI RFID**

<table>
<tr>
<td colspan="3"><p><strong>PHƯƠNG TIỆN TIẾN VÀO LÀN</strong></p><p>Cảm biến phát hiện xe → khởi tạo mã lượt</p></td>
</tr>
<tr>
<td colspan="3"><p>↓</p></td>
</tr>
<tr>
<td colspan="3"><p><strong>ĐỌC THẺ RFID</strong></p><p>Đầu đọc và ăng-ten thu nhận mã EPC/ID từ thẻ</p></td>
</tr>
<tr>
<td colspan="3"><p>↓</p></td>
</tr>
<tr>
<td colspan="3"><p><strong>KIỂM TRA KẾT QUẢ ĐỌC VÀ TRA CỨU</strong></p><p>Nếu đọc được mã thẻ, tra cứu trong danh sách phương tiện đăng ký</p></td>
</tr>
<tr>
<td colspan="3"><p>↓</p></td>
</tr>
<tr>
<td><p><strong>TRƯỜNG HỢP 1</strong></p><p>Đọc được mã thẻ và tìm thấy trong danh sách</p></td>
<td><p><strong>TRƯỜNG HỢP 2</strong></p><p>Không đọc được mã thẻ</p></td>
<td><p><strong>TRƯỜNG HỢP 3</strong></p><p>Đọc được mã thẻ nhưng không tìm thấy trong danh sách</p></td>
</tr>
<tr>
<td><p>↓</p></td>
<td><p>↓</p></td>
<td><p>↓</p></td>
</tr>
<tr>
<td><p><strong>TRẢ VỀ MÃ XE</strong></p><p>Chuyển sang bước kiểm tra tài khoản và điều kiện thu phí</p></td>
<td><p><strong>CHUYỂN XÁC MINH</strong></p><p>Kiểm tra thẻ, vị trí dán và thiết bị đọc</p></td>
<td><p><strong>CHUYỂN XÁC MINH</strong></p><p>Kiểm tra mã thẻ và thông tin đăng ký</p></td>
</tr>
<tr>
<td colspan="3"><p>↓</p></td>
</tr>
<tr>
<td colspan="3"><p><strong>GHI NHẬN KẾT QUẢ XỬ LÝ</strong></p><p>Lưu mã lượt, mã thẻ nếu có, mã xe tra cứu được và trạng thái xử lý</p></td>
</tr>
</table>

*Hình: Quy trình nhận diện bằng RFID và các nhánh xử lý lỗi.*

Kết quả tra cứu RFID chưa tự xác minh được thẻ có gắn đúng phương tiện hay không. Cơ chế phối hợp với ANPR/LPR được trình bày tại mục 3.3.

## **3.2. Công nghệ nhận diện biển số bằng hình ảnh (ANPR/LPR): nguyên lý, thành phần, quy trình hoạt động**

### **3.2.1 Khái niệm và Nguyên lý hoạt động :**

ANPR/LPR là công nghệ nhận diện biển số tự động từ ảnh hoặc video. Trong ETC, camera ghi nhận hình ảnh xe, phần mềm xác định vùng biển số và chuyển các ký tự trên ảnh thành chuỗi văn bản để tra cứu phương tiện.

Kết quả nhận diện phụ thuộc vào chất lượng ảnh, góc chụp, ánh sáng và tình trạng biển số. Vì vậy, hệ thống cần kiểm tra kết quả trước khi dùng cho việc đối chiếu hoặc xử lý giao dịch.

### **3.2.2 Thành phần cơ bản của hệ thống ANPR/LPR**

Hệ thống ANPR/LPR trong ETC có thể được trình bày theo bốn phân hệ kỹ thuật dưới đây. Cách bố trí thiết bị và nơi thực hiện xử lý ảnh phụ thuộc vào thiết kế của từng hệ thống.

**1. Phân hệ thu thập hình ảnh và chiếu sáng hiện trường (Image Acquisition & Illumination)**

- **Camera AI chuyên dụng hiện trường**. Ghi nhận ảnh phương tiện và biển số khi xe đi qua vùng quan sát. Độ phân giải, thời gian phơi sáng và góc chụp cần phù hợp để hạn chế ảnh nhòe và giúp biển số hiện rõ.

- **Hệ thống đèn chiếu sáng hồng ngoại (IR Illuminator)**. Hỗ trợ thu ảnh khi ánh sáng môi trường yếu. Hiệu quả còn phụ thuộc vào cách bố trí đèn, phản xạ từ biển số và điều kiện thời tiết.

**2. Khung gantry và phân hệ cảm biến kích hoạt hiện trường (Roadside Structure & Triggering Subsystem)**

- **Khung gantry treo thiết bị**. Cố định camera và đèn tại vị trí, góc quan sát phù hợp. Tùy thiết kế trạm, thiết bị cũng có thể được lắp trên cột hoặc giá đỡ riêng.

- **Cảm biến kích hoạt chụp ảnh (Vehicle Detectors)**. Có thể sử dụng vòng từ, laser hoặc phát hiện xe trong video. Khi xe vào vùng kiểm soát, hệ thống xác định thời điểm ghi hình và gắn ảnh với lượt xe tương ứng.

**3. Phân hệ xử lý biên trí tuệ nhân tạo (Edge AI Processing Unit)**

- **Bộ tính toán Edge AI hiện trường**. Có thể tích hợp trong camera hoặc đặt tại tủ kỹ thuật ở làn. Thiết bị xử lý ảnh gần nơi thu nhận, hỗ trợ giảm lượng dữ liệu cần truyền về máy chủ.

- **Thực thi mô hình nhận diện tại chỗ**. Phần mềm tiền xử lý ảnh, xác định vùng biển số và nhận dạng ký tự bằng OCR. Các mô hình học sâu có thể được sử dụng tùy giải pháp. Thời gian và độ chính xác xử lý phụ thuộc vào thiết bị, mô hình và chất lượng ảnh.

**4. Phần mềm quản lý và máy chủ trung tâm (Central LPR Software & TOC System)**

- **Máy chủ quản lý và kết nối trung tâm điều hành**. Lưu ảnh toàn cảnh, ảnh biển số, chuỗi ký tự nhận diện, thời gian và vị trí làn. Phần mềm hỗ trợ tra cứu dữ liệu phương tiện do hệ thống quản lý, đối chiếu với RFID và kiểm tra lại các lượt nhận diện chưa rõ.

- **Chuẩn hóa giao tiếp và từ điển dữ liệu**. Các cơ chế dưới đây được lựa chọn theo yêu cầu tích hợp của từng hệ thống.

- **Giao thức SNMP**. Hỗ trợ trao đổi thông tin quản lý, theo dõi trạng thái và báo cáo sự cố thiết bị hiện trường.

- **Hồ sơ AP-DATEX**. Quy định cách trao đổi dữ liệu giữa các thành phần trong hạ tầng ITS.

- **Định danh đối tượng OID**. Dùng để định danh các khái niệm dữ liệu ITS, hỗ trợ quản lý và thống nhất cách hiểu dữ liệu.

### **3.2.3. Pipeline xử lý ảnh và nhận diện biển số.**

<table>
<tr>
<td><p><strong>GIAI ĐOẠN 1  |  </strong>Thu thập hình ảnh và kích hoạt</p></td>
</tr>
<tr>
<td><p>↓</p></td>
</tr>
<tr>
<td><p><strong>GIAI ĐOẠN 2  |  </strong>Tiền xử lý hình ảnh tại biên (Edge AI)</p></td>
</tr>
<tr>
<td><p>↓</p></td>
</tr>
<tr>
<td><p><strong>GIAI ĐOẠN 3  |  </strong>Phát hiện và định vị vùng biển số (Localization)</p></td>
</tr>
<tr>
<td><p>↓</p></td>
</tr>
<tr>
<td><p><strong>GIAI ĐOẠN 4  |  </strong>Phân đoạn ký tự (Character Segmentation)</p></td>
</tr>
<tr>
<td><p>↓</p></td>
</tr>
<tr>
<td><p><strong>GIAI ĐOẠN 5  |  </strong>Nhận dạng OCR và đánh giá điểm tin cậy (Confidence Score)</p></td>
</tr>
</table>

*Hình: Quy trình xử lý và nhận diện biển số bằng ANPR/LPR*

### **3.2.4. Minh họa quy trình hoạt động và xử lý lỗi**

<table>
<tr>
<td colspan="4"><p><strong>Phương tiện đi vào vùng ghi hình</strong></p></td>
</tr>
<tr>
<td colspan="4"><p>↓</p></td>
</tr>
<tr>
<td colspan="4"><p><strong>Thu thập ảnh và tiền xử lý</strong></p></td>
</tr>
<tr>
<td colspan="4"><p>↓</p></td>
</tr>
<tr>
<td colspan="4"><p><strong>Xác định vùng biển số và nhận dạng ký tự</strong></p></td>
</tr>
<tr>
<td colspan="4"><p>↓</p></td>
</tr>
<tr>
<td colspan="4"><p><strong>ĐỌC ĐƯỢC BIỂN SỐ VÀ ĐỦ TIN CẬY ĐỂ TRA CỨU?</strong></p></td>
</tr>
<tr>
<td colspan="2"><p><strong>CÓ</strong></p></td>
<td colspan="2"><p><strong>CHƯA ĐẠT</strong></p></td>
</tr>
<tr>
<td colspan="2"><p>↓</p></td>
<td colspan="2"><p>↓</p></td>
</tr>
<tr>
<td colspan="2"><p><strong>Tra cứu biển số trong dữ liệu đăng ký</strong></p></td>
<td colspan="2"><p><strong>Kiểm tra ảnh và kết quả nhận dạng</strong></p></td>
</tr>
<tr>
<td><p>↓</p></td>
<td><p>↓</p></td>
<td><p>↓</p></td>
<td><p>↓</p></td>
</tr>
<tr>
<td><p><strong>TÌM THẤY XE</strong></p></td>
<td><p><strong>KHÔNG TÌM THẤY</strong></p></td>
<td><p><strong>ẢNH KÉM / ĐỘ TIN CẬY THẤP</strong></p></td>
<td><p><strong>KHÔNG ĐỌC ĐƯỢC BIỂN SỐ</strong></p></td>
</tr>
<tr>
<td><p>↓</p></td>
<td><p>↓</p></td>
<td><p>↓</p></td>
<td><p>↓</p></td>
</tr>
<tr>
<td><p>Trả mã xe từ kết quả tra cứu</p></td>
<td><p>Chuyển xác minh biển số và dữ liệu đăng ký</p></td>
<td><p>Kiểm tra hoặc lấy lại ảnh nếu có thể, chuyển xác minh khi cần</p></td>
<td><p>Lưu ảnh và mã lượt, chuyển xác minh</p></td>
</tr>
<tr>
<td><p>↓</p></td>
<td><p>↓</p></td>
<td><p>↓</p></td>
<td><p>↓</p></td>
</tr>
<tr>
<td colspan="4"><p><strong>GHI NHẬN KẾT QUẢ THEO MÃ LƯỢT</strong></p></td>
</tr>
</table>

Lưu ý. Ngưỡng tin cậy được lựa chọn theo hệ thống và điều kiện triển khai. Biển số đọc sai vẫn có thể trùng với một xe đã đăng ký, nên kết quả tra cứu cần được đối chiếu khi đánh giá nhận diện.

## **3.3. Phối hợp RFID và ANPR/LPR trong nhận diện phương tiện**

### **3.3.1 Sự cần thiết của cơ chế phối hợp song song**

Trong hệ thống ETC, phối hợp song song RFID và ANPR/LPR giúp đối chiếu thông tin từ mã thẻ và hình ảnh biển số của cùng lượt xe. Hai nguồn bổ sung căn cứ kiểm tra phương tiện và hỗ trợ xử lý khi kết quả nhận diện thiếu hoặc không khớp.

**1. Giới hạn của các công nghệ nhận diện đơn lẻ**

- **Công nghệ RFID**

- *Ưu điểm*. Đọc mã thẻ mà không cần ảnh biển số và ít phụ thuộc vào điều kiện chiếu sáng.

- *Hạn chế*. Kết quả đọc thẻ chưa xác nhận được thẻ đang gắn trên đúng phương tiện đăng ký. Việc chuyển thẻ sang xe khác cần thêm thông tin để kiểm tra.

- **Công nghệ ANPR/LPR**

- *Ưu điểm*. Cung cấp biển số và hình ảnh phương tiện để tra cứu, đối chiếu và kiểm tra lại lượt xe.

- *Hạn chế*. Chất lượng nhận diện phụ thuộc vào ánh sáng, thời tiết, góc chụp và tình trạng biển số. Việc xử lý ảnh cũng cần thiết bị tính toán phù hợp.

**2. Lợi ích kỹ thuật và vận hành của cơ chế phối hợp song song**

- **Bổ sung thông tin và hỗ trợ vận hành**. Khi một nguồn gặp lỗi, nguồn còn lại cung cấp thêm căn cứ xác minh. Việc tiếp tục xử lý giao dịch phụ thuộc vào quy trình vận hành và mức độ tin cậy của dữ liệu.

- **Hỗ trợ phát hiện sai lệch và chống thất thu**. Đối chiếu kết quả tra cứu từ mã thẻ và biển số giúp phát hiện thông tin không khớp. Hệ thống lưu dữ liệu để kiểm tra nguyên nhân và xác minh trường hợp nghi ngờ gian lận.

- **Hỗ trợ thu phí tự do nhiều làn (MLFF)**. Phối hợp hai nguồn giúp kiểm tra kết quả nhận diện khi xe đi qua vùng thu phí. Mã thẻ, ảnh và biển số cần được ghép đúng theo cùng lượt xe.

- **Hỗ trợ chuẩn hóa và trao đổi dữ liệu**. Dữ liệu nhận diện cần có cách biểu diễn thống nhất để lưu trữ và trao đổi giữa thiết bị tại làn với máy chủ. Các tiêu chuẩn, giao thức áp dụng phụ thuộc vào thiết kế và yêu cầu của từng hệ thống.

Hai nguồn vẫn có thể cùng nhận diện sai hoặc cùng thiếu dữ liệu. Vì vậy, phối hợp công nghệ giúp bổ sung căn cứ đối chiếu nhưng vẫn cần quy trình xử lý ngoại lệ.

### **3.3.2. Pipeline xử lý nhận diện phối hợp.**

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

### **3.3.3. Cơ chế đối chiếu và xác thực kết quả.**

Việc đối chiếu hai nguồn được thực hiện qua ba bước.

Bước 1. Ghép dữ liệu cùng lượt xe. Dùng mã lượt, thời gian và vị trí làn để ghép kết quả đọc RFID với ảnh hoặc biển số của cùng phương tiện.

Bước 2. Tra cứu định danh. Mã thẻ và biển số được tra cứu trong dữ liệu đăng ký để xác định phương tiện mà mỗi nguồn nhận diện được.

Bước 3. Đối chiếu kết quả. Nếu hai nguồn cùng chỉ tới một phương tiện, kết quả được chuyển sang bước kiểm tra tài khoản và điều kiện thu phí. Khi thiếu thông tin hoặc hai kết quả khác nhau, hệ thống chuyển sang xử lý ngoại lệ.

Hai nguồn trùng khớp vẫn có thể cùng chỉ tới một phương tiện sai. Trường hợp này cần được xét khi đánh giá giới hạn của cơ chế phối hợp.

### **3.3.4. Xử lý ngoại lệ và phát hiện thông tin không khớp.**

Các trường hợp sau cần được phân biệt khi xử lý kết quả nhận diện.

<table>
<tr>
<td><p><strong>Tình huống</strong></p></td>
<td><p><strong>Hướng xử lý</strong></p></td>
</tr>
<tr>
<td><p>Hai nguồn trùng khớp</p></td>
<td><p>Chuyển kết quả nhận diện sang bước kiểm tra tài khoản và điều kiện thu phí.</p></td>
</tr>
<tr>
<td><p>Thiếu kết quả RFID hoặc ANPR/LPR</p></td>
<td><p>Lưu thông tin từ nguồn còn lại, kiểm tra thẻ hoặc ảnh và chuyển xác minh theo quy trình vận hành.</p></td>
</tr>
<tr>
<td><p>Hai nguồn chỉ tới hai xe khác nhau</p></td>
<td><p>Kiểm tra việc ghép dữ liệu cùng lượt và thông tin đăng ký. Lưu mã thẻ, biển số, ảnh và thời gian để xác minh.</p></td>
</tr>
<tr>
<td><p>Cả hai nguồn đều thiếu hoặc không tra cứu được</p></td>
<td><p>Chuyển xác minh, kiểm tra thiết bị và dữ liệu đăng ký để bổ sung thông tin nhận diện.</p></td>
</tr>
</table>

## **3.4. Các hướng công nghệ khác trong thu phí và nhận diện phương tiện**

Bên cạnh RFID và ANPR/LPR, một số công nghệ khác hỗ trợ thu phí, xác định vị trí và trao đổi thông tin phương tiện. Phần này giới thiệu nguyên lý, ứng dụng và giới hạn của từng hướng để bổ sung bối cảnh cho đề tài.

### **3.4.1. Công nghệ giao tiếp tầm ngắn chuyên dụng (DSRC)**

Nguyên lý hoạt động và kiến trúc

DSRC sử dụng liên lạc vô tuyến giữa thiết bị trên xe và thiết bị bên đường để trao đổi dữ liệu khi xe đi qua điểm thu phí. Dải tần và phương thức giao dịch phụ thuộc vào hệ thống triển khai. Chẳng hạn, ETC tại Nhật Bản sử dụng DSRC 5,8 GHz.

Mô hình triển khai tiêu biểu

- Singapore ERP 1.0 sử dụng thiết bị trên xe (IU) và các điểm thu phí gắn với gantry. Đây là một ví dụ về thu phí dựa trên giao tiếp giữa xe và hạ tầng cố định.

- Nhật Bản ETC 2.0 sử dụng kết nối giữa thiết bị trên xe và ITS Spots. Ngoài thu phí, hệ thống cung cấp thông tin giao thông và hỗ trợ lái xe.

Hạn chế kỹ thuật

DSRC cần thiết bị trên xe và thiết bị thu phát tại những vị trí được bố trí trước. Việc mở rộng hoặc thay đổi điểm thu phí có thể kéo theo điều chỉnh hạ tầng và chi phí bảo trì.

### **3.4.2. Công nghệ thu phí dựa trên định vị vệ tinh (GNSS Tolling)**

Nguyên lý hoạt động và kiến trúc cổng ảo

GNSS kết hợp dữ liệu vị trí và thông tin tuyến đường hoặc vùng tính phí để xác định nghĩa vụ trả phí. Ranh giới thu phí có thể được thiết lập trên bản đồ số, giúp giảm sự phụ thuộc vào gantry tại từng điểm. Thiết bị OBU trên xe và kết nối truyền dữ liệu được sử dụng tùy thiết kế hệ thống.

Cơ chế vận hành và tính năng mở rộng

ERP 2.0 của Singapore là ví dụ sử dụng GNSS và OBU để xác định vị trí, xử lý phí và hiển thị thông tin cho người lái. Công nghệ này tạo khả năng triển khai thu phí theo quãng đường trong tương lai. Việc áp dụng cách tính phí cụ thể còn phụ thuộc vào chính sách vận hành.

Thách thức kỹ thuật

- Tín hiệu định vị có thể bị ảnh hưởng tại hầm hoặc khu vực nhiều nhà cao tầng. Hệ thống cần có biện pháp kiểm tra và xử lý sai số vị trí.

- Việc triển khai còn cần xem xét lắp đặt thiết bị, kết nối dữ liệu và bảo vệ thông tin hành trình.

### 3.4.3. Hệ thống giao thông kết nối và hợp tác (C-ITS) và hạ tầng V2X

Khái niệm và kiến trúc V2X

C-ITS hỗ trợ các thành phần giao thông trao đổi thông tin để phối hợp hoạt động. V2X bao gồm giao tiếp giữa xe với xe (V2V), xe với hạ tầng (V2I) và các đối tượng khác. Hai cách kết nối thường được đề cập gồm giao tiếp trực tiếp và giao tiếp qua mạng di động.

- Truyền thông trực tiếp (Direct V2X) cho phép trao đổi thông tin với các đối tượng ở gần thông qua những công nghệ như ITS-G5 hoặc C-V2X PC5.

- Truyền thông qua mạng (Network V2X) sử dụng mạng di động để trao đổi dữ liệu với hệ thống dịch vụ và quản lý giao thông.

Ứng dụng an toàn và thu phí liên thông

V2X hỗ trợ cảnh báo giao thông và trao đổi thông tin giữa phương tiện với hạ tầng. Trong thu phí, có thể xem xét sử dụng kết nối này để truyền dữ liệu phục vụ giao dịch. Khả năng áp dụng cần được đánh giá cùng cơ chế định danh, xác thực và khả năng tương thích giữa các hệ thống.

Bảo mật dữ liệu và quyền riêng tư

Dữ liệu trao đổi cần được xác thực và bảo vệ khỏi truy cập trái phép. Các giải pháp chứng thư số có thể hỗ trợ kiểm tra nguồn gửi, đồng thời cần có quy định về thu thập, lưu trữ và sử dụng thông tin hành trình.

### 3.4.4. Công nghệ Bluetooth Low Energy (BLE) và ứng dụng di động

Nguyên lý hoạt động

BLE là công nghệ kết nối vô tuyến công suất thấp giữa các thiết bị có hỗ trợ Bluetooth. Trong mô hình dùng ứng dụng di động, điện thoại có thể trao đổi dữ liệu với thiết bị tại điểm kiểm soát. Phạm vi hoạt động phụ thuộc vào thiết bị và môi trường truyền sóng.

Ứng dụng tiêu biểu

- Thu phí đỗ xe. BLE có thể hỗ trợ nhận biết thiết bị của người dùng tại bãi đỗ và kết hợp ứng dụng để xác nhận lượt sử dụng, thanh toán. Việc ghi nhận xe vào, ra cần được kiểm tra phù hợp với thiết kế bãi.

- Quản lý ra vào đô thị. BLE và ứng dụng có thể được xem xét cho điểm kiểm soát quy mô nhỏ. Cần bảo đảm liên kết đúng thiết bị, tài khoản và phương tiện khi xác nhận lượt xe.

Bốn hướng trên được giới thiệu ở mức tổng quan. Phần phân tích chính và mô phỏng của đề tài tập trung vào RFID, ANPR/LPR và phương án phối hợp.

## **3.5. Thực tiễn áp dụng tại Việt Nam**

Trong hệ thống ETC tại Việt Nam, phương tiện sử dụng thẻ RFID của các nhà cung cấp như VETC hoặc ePass, liên kết với tài khoản giao thông. Camera ghi nhận biển số và hình ảnh xe để hỗ trợ đối chiếu, kiểm tra các trường hợp phát sinh.

Với mô hình thu phí tự do nhiều làn (MLFF), việc ghép đúng kết quả đọc thẻ và biển số của cùng lượt xe cần được xem xét khi phương tiện đi qua vùng nhận diện. Đây là bối cảnh để thảo luận về khả năng phối hợp hai công nghệ.

ETC còn được mở rộng sang các điểm đỗ xe và sân bay. Trong phạm vi đề tài, những ứng dụng này được dùng để minh họa các bối cảnh triển khai khác nhau của nhận diện phương tiện.
