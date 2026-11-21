## 6.4 Mô phỏng phối hợp RFID và ANPR/LPR

### 6.4.1. Nguyên tắc phối hợp hai công nghệ

Trong phạm vi đề tài, phương án phối hợp được mô phỏng ở bước đối chiếu kết quả định danh từ hai phương án RFID và ANPR/LPR đã thực hiện tại mục 6.2 và 6.3. Chương trình không đọc thẻ bằng thiết bị thật, không xử lý ảnh biển số và không thực hiện giao dịch thanh toán. Mục tiêu là kiểm tra cách xử lý khi hai nguồn cùng xác định một phương tiện, trả về kết quả khác nhau hoặc không đủ thông tin nhận diện.

Hai kết quả được ghép theo cùng mã lượt xe (ma_luot), sau đó đối chiếu mã xe đã nhận diện (ma_xe_nhan_dien). Chương trình không so sánh trực tiếp mã thẻ RFID với chuỗi biển số vì đây là hai loại thông tin khác nhau. Việc tra cứu từ mã thẻ hoặc biển số sang mã xe đã được thực hiện ở từng phương án độc lập.

Quy tắc chấp nhận yêu cầu cả hai nguồn có trạng thái CHAP_NHAN, có mã xe không trống và cùng trả về một mã xe. Nếu thiếu kết quả, một nguồn không nhận diện được hoặc hai mã xe không khớp, lượt xe được chuyển sang CHUYEN_XAC_MINH. Theo quy tắc này, chương trình không tự chọn kết quả của nguồn còn lại khi một nguồn gặp lỗi.

Cột xe_thuc_te chỉ được sử dụng để đánh giá sau khi chương trình đưa ra quyết định. Hai nguồn khớp nhau chưa bảo đảm phương tiện được nhận diện đúng, vì cả hai có thể cùng trả về mã của một xe khác. Tình huống này được kiểm tra qua lượt L09 trong bộ dữ liệu giả lập.

### 6.4.2. Xây dựng chương trình mô phỏng phối hợp

Chương trình được viết bằng Python trong tệp mo_phong_phoi_hop.py, sử dụng các thư viện chuẩn csv, pathlib và argparse. Chương trình chạy trên terminal, không cần giao diện hoặc thư viện bên ngoài.

Dữ liệu đầu vào gồm ba tệp: luot_xe.csv từ mục 6.1 để xác định danh sách lượt cần xử lý; ket_qua_rfid.csv từ mục 6.2; và ket_qua_anpr.csv từ mục 6.3. Hai tệp kết quả có các cột riêng của từng phương án, nhưng đều cung cấp ba trường cần thiết cho bước phối hợp là ma_luot, trang_thai và ma_xe_nhan_dien. Mỗi tệp kết quả trong lần chạy này có đủ 12 bản ghi, tương ứng L01–L12.

![Hình 6.4.1](hinh_anh/hinh_6_4_1.png)

*Hình 6.4.1. Kết quả RFID được sử dụng làm đầu vào cho phương án phối hợp.*

![Hình 6.4.2](hinh_anh/hinh_6_4_2.png)

*Hình 6.4.2. Kết quả ANPR/LPR được sử dụng làm đầu vào cho phương án phối hợp.*

Quy trình xử lý gồm: (1) đọc danh sách lượt xe và hai tệp kết quả; (2) kiểm tra cấu trúc CSV, mã lượt và trạng thái nhận diện; (3) ghép hai kết quả theo từng ma_luot trong danh sách; (4) kiểm tra trạng thái và so sánh mã xe; (5) in kết quả lên terminal và xuất tệp ket_qua_phoi_hop.csv. Danh sách lượt được lấy từ tệp đầu vào, không cố định trong chương trình ở 12 lượt.

Các hàm chính gồm doc_csv() để đọc và kiểm tra cấu trúc dữ liệu; doc_ket_qua() để kiểm tra kết quả từng nguồn; doi_chieu_hai_nguon() để áp dụng quy tắc phối hợp; và chay_mo_phong() để tổ chức xử lý toàn bộ lượt xe. Hàm main() tiếp nhận đường dẫn, ghi tệp CSV và hiển thị kết quả.

Đầu ra có sáu trường: ma_luot, ma_xe_rfid, ma_xe_anpr, trang_thai, ma_xe_nhan_dien và ly_do. Trường trang_thai chỉ nhận CHAP_NHAN hoặc CHUYEN_XAC_MINH; trường ly_do giải thích nguyên nhân xử lý. Khi chuyển xác minh, ma_xe_nhan_dien được để trống. Tệp này được dùng tại mục 6.5 để tổng hợp và so sánh với hai phương án độc lập.

Chương trình được kiểm tra bằng tệp test_phoi_hop.py với bốn bài kiểm thử tự động: các trường hợp phối hợp hai nguồn; phát hiện CSV không hợp lệ; kiểm tra kết quả trên bộ dữ liệu chung; và phát hiện mã lượt ngoài danh sách. Ảnh kiểm thử ghi nhận cả bốn bài đều đạt (OK). Kết quả này xác nhận các trường hợp đã kiểm thử tuân theo quy tắc xử lý, không đồng nghĩa mọi lượt xe đều được định danh đúng.

![Hình 6.4.3](hinh_anh/hinh_6_4_3.png)

*Hình 6.4.3. Kết quả kiểm thử tự động: bốn bài kiểm thử đều đạt (OK).*

### 6.4.3. Xử lý các trường hợp nhận diện không thành công hoặc không khớp

Trường hợp hai nguồn không khớp: khi cả hai đều chấp nhận nhưng trả về mã xe khác nhau, chương trình chuyển xác minh với lý do HAI_NGUON_KHONG_KHOP. Trong bộ dữ liệu này, L06, L07 và L08 thuộc nhóm trên. Chương trình không ưu tiên một nguồn để quyết định thay cho bước xác minh.

Trường hợp có bản ghi nhưng không nhận diện được: L03 và L10 được chuyển xác minh do nguồn RFID không trả về mã xe được chấp nhận; L04 và L11 gặp tình huống tương tự ở nguồn ANPR/LPR. L05 và L12 có bản ghi ở cả hai tệp nhưng cả hai nguồn đều không nhận diện được. Lý do tương ứng là RFID_KHONG_NHAN_DIEN_DUOC, ANPR_KHONG_NHAN_DIEN_DUOC hoặc CA_HAI_KHONG_NHAN_DIEN_DUOC.

Trường hợp thiếu bản ghi kết quả: nếu một mã lượt có trong luot_xe.csv nhưng không có bản ghi ở một hoặc cả hai tệp kết quả, chương trình vẫn ghi nhận lượt đó và chuyển xác minh. Các lý do được sử dụng là THIEU_KET_QUA_RFID, THIEU_KET_QUA_ANPR hoặc THIEU_CA_HAI_KET_QUA. Cần phân biệt thiếu bản ghi với trường hợp đã có bản ghi nhưng không đọc được thẻ hoặc biển số. Bộ dữ liệu chạy minh họa có đủ bản ghi; các tình huống thiếu bản ghi được kiểm tra trong bài kiểm thử tự động.

Đối với lỗi định dạng dữ liệu, chương trình báo lỗi và dừng thay vì coi đó là lỗi nhận diện. Các lỗi được kiểm tra gồm thiếu cột bắt buộc, dòng CSV sai số cột, mã lượt trống hoặc trùng, trạng thái không hợp lệ, trạng thái chấp nhận nhưng thiếu mã xe và mã lượt không thuộc danh sách đầu vào. Việc chuyển xác minh trong mô hình chỉ là ghi nhận trạng thái cần xử lý tiếp, không phải kết luận vi phạm hay đã thực hiện xác minh thủ công.

### 6.4.4. Kết quả mô phỏng và nhận xét

Chương trình đã xử lý đủ 12 lượt xe và xuất tệp ket_qua_phoi_hop.csv. Kết quả trên terminal ghi nhận 3 lượt CHAP_NHAN và 9 lượt CHUYEN_XAC_MINH. Ba lượt được chấp nhận là L01, L02 và L09, tương ứng mã xe XE01, XE04 và XE02.

![Hình 6.4.4](hinh_anh/hinh_6_4_4.png)

*Hình 6.4.4. Kết quả chạy mô phỏng phối hợp RFID và ANPR/LPR trên 12 lượt xe giả lập.*

Sau khi đối chiếu mã xe đầu ra với cột xe_thuc_te, kết quả được chia thành ba nhóm: định danh đúng tự động 2/12 lượt (16,67%); chấp nhận sai 1/12 lượt (8,33%); chuyển xác minh 9/12 lượt (75,00%). Tổng cộng là 12/12 lượt (100%). Các tỷ lệ đều được tính trên tổng số 12 lượt, không chỉ trên số lượt được chấp nhận.

L01 và L02 được định danh đúng vì mã xe từ hai nguồn vừa khớp nhau vừa trùng với xe thực tế. Riêng L09, cả RFID và ANPR/LPR đều trả về XE02 nên chương trình chấp nhận theo quy tắc đã đặt ra, trong khi xe_thuc_te là XE01. Vì vậy, L09 được tính là chấp nhận sai. Tỷ lệ hai nguồn khớp và được chấp nhận là 3/12 = 25,00%, khác với tỷ lệ định danh đúng tự động 2/12 = 16,67%.

So với kết quả của từng phương án độc lập trên cùng bộ dữ liệu, số lượt chấp nhận sai giảm từ 3 xuống 1, nhưng số lượt chuyển xác minh tăng từ 4 lên 9. Quy tắc yêu cầu đồng thuận giúp phát hiện một số sai lệch giữa hai nguồn, đồng thời làm giảm số lượt có thể xử lý tự động khi chỉ một nguồn nhận diện được. Đây là sự đánh đổi cần xem xét khi phân tích phương án phối hợp.

Kết quả liên hệ trực tiếp với các tình huống ở chương 5: không đọc được thẻ, nhận diện sai biển số và hai nguồn không khớp. Tuy nhiên, mô hình chưa thực hiện bước xác minh sau chuyển giao, chưa xử lý ảnh hoặc tín hiệu vô tuyến và chưa mô phỏng thời gian xử lý hay giao dịch thanh toán. Bộ 12 lượt là các tình huống được thiết kế chủ động; các tỷ lệ trên chỉ phản ánh quy tắc xử lý trên bộ dữ liệu này, không đại diện cho độ chính xác hoặc hiệu năng của hệ thống ETC thực tế.
