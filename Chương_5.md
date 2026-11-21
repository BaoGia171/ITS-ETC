# CHƯƠNG 5. PHÂN TÍCH TÌNH HUỐNG VÀ ĐỀ XUẤT

## 5.1. Tình huống RFID không nhận diện được thẻ

### Nguyên nhân kỹ thuật và yếu tố môi trường

Lỗi phần cứng và hỏng hóc vật lý: Thẻ RFID (e-tag) bị bong tróc, đứt mạch anten ngầm bên trong, hỏng chip silicon do va đập hoặc lão hóa vật liệu dưới tác động của nhiệt độ cao trên kính lái. Đầu đọc (RFID Reader) tại trạm gặp sự cố công suất phát, chập cháy nguồn hoặc lỗi cáp tín hiệu RG8/RG213 nối với anten.

Hiện tượng suy hao và che chắn vô tuyến: Phim cách nhiệt chứa thành phần kim loại (metalized film) dán trên kính kính trước làm suy hao sóng siêu cao tần (UHF: 860–960 MHz). Xe chở hàng kim loại lớn, xe container hoặc phương tiện chắn sát phía trước gây hiệu ứng bóng râm vô tuyến (RF Shadowing).

Nhiễu giao thoa tín hiệu: Nhiễu sóng RF từ các trạm viễn thông lân cận, thiết bị phát sóng nội bộ trạm hoặc hiện tượng phản xạ đa đường (Multipath Fading) do bề mặt kim loại của các xe xung quanh làm méo dạng tín hiệu phản hồi (Backscattered signal) từ thẻ về anten.

### Hệ quả vận hành

Tại trạm đơn làn có barie: Xe dừng đột ngột trước barie gây ùn tắc cục bộ tại làn ETC, buộc nhân viên vận hành phải can thiệp thủ công (quét tay, nhập biển số), giảm năng lực thông qua từ 800–1.000 xe/giờ xuống dưới 200 xe/giờ.

Tại hành lang tự do đa làn (MLFF/ERP 2.0): Phương tiện di chuyển ở tốc độ cao (up to 120 km/h) đi qua điểm thu phí mà không thể ghi nhận giao dịch RFID. Nếu không có hệ thống dự phòng, điều này dẫn đến thất thoát doanh thu (Leakage) hoặc phát sinh gánh nặng rà soát nợ thu phí lớn.

### Hướng xử lý sự cố khẩn cấp

Tự động chuyển luồng xử lý thị giác: Khi anten RFID không ghi nhận tín hiệu thẻ trong khoảng thời gian cửa sổ (twindow<100 ms), hệ thống quản lý làn (LCS) ngay lập tức kích hoạt luồng xử lý ảnh từ camera ANPR/LPR chuyên dụng để nhận diện biển số xe làm định danh thay thế.

Xác thực qua tài khoản liên kết: Biển số xe sau khi được camera ANPR nhận dạng sẽ được tra cứu tức thì trong cơ sở dữ liệu quốc gia/hệ thống tài khoản giao thông để tự động trừ tiền vào tài khoản liên kết (VD: VETC, ePass hoặc tài khoản ngân hàng/ví điện tử) mà không yêu cầu phương tiện dừng lại.

Hỗ trợ thiết bị cầm tay tại làn đơn: Tại các trạm thu phí barrier đơn làn, nhân viên trực làn sử dụng đầu đọc RFID di động (Handheld RFID Reader) áp sát kính lái hoặc kiểm tra biển số qua App vận hành để mở barie cưỡng bức, giải phóng làn nhanh chóng.

## 5.2. Tình huống ANPR/LPR nhận diện sai biển số

### Nguyên nhân thuật toán và điều kiện quang học

Hiện tượng che lấp và biến dạng vật lý: Biển số bị bám bùn đất, sơn mờ, bị cố tình dán làm thay đổi ký tự (ví dụ: sửa F thành E, 3 thành 8), biển số bị móp méo, cong vênh hoặc che khuất bởi móc kéo, giá chở đồ phía sau.

Điều kiện ánh sáng và thời tiết bất lợi: Đèn pha xe đối diện gây chói mắt camera (Headlight Glare), ánh sáng mặt trời chiếu trực diện tạo bóng râm gắt, mưa lớn, sương mù dày đặc hoặc điều kiện đêm tối làm giảm độ tương phản và chất lượng ảnh chụp (SNR<15 dB).

Thách thức biển số nước ngoài/biển số đặc thù: Chuỗi ký tự biển số ngoại giao, biển số xe quân sự, biển số nước ngoài (xe quá cảnh Lao/Cambodia) có phông chữ, bố cục màu sắc và kích thước nằm ngoài mẫu dữ liệu huấn luyện (Training Set) của mô hình Deep Learning/OCR.

### Hệ quả vận hành

Trừ tiền nhầm vào tài khoản của chủ phương tiện khác: Hệ thống nhận diện sai biển số xe A thành biển số xe B, dẫn đến việc khấu trừ giao dịch từ tài khoản giao thông của xe B (không hề qua trạm), gây bức xúc và khiếu nại từ khách hàng.

Phát sinh lượng lớn hồ sơ ngoại lệ cần xử lý thủ công: Gia tăng khối lượng công việc cho Trung tâm Xử lý Giao dịch (Back-Office), tăng chi phí vận hành và làm chậm tiến trình quyết toán giao dịch inter-operator.

### Hướng xử lý sự cố khẩn cấp

Cơ chế kiểm soát ngưỡng tin cậy (Confidence Threshold): Thiết lập ngưỡng tin cậy thuật toán (ví dụ: Confidence≥95%). Nếu điểm nhận dạng chữ/số nằm dưới ngưỡng này, hệ thống không tự động trừ tiền mà đẩy hình ảnh vào hàng đợi phân loại ngoại lệ (Exception Queue).

Xác minh đa góc nhìn và nhận dạng đặc trưng xe: Tích hợp dữ liệu từ camera toàn cảnh (Front/Rear Camera) để phân tích bổ sung các đặc trưng sinh học của xe (Make, Model, Color, Body Type - MMCR). So sánh màu sơn, kiểu dáng xe với dữ liệu đăng kiểm của biển số vừa nhận dạng để phát hiện sự bất hợp lý.

Quy trình xác minh bởi con người (Human-in-the-Loop): Thiết lập đội ngũ nhân sự kiểm duyệt hình ảnh 24/7 tại Back-Office. Các giao dịch nghi ngờ được hiển thị cùng hình ảnh độ phân giải cao để điện thoại viên/kiểm duyệt viên bấm xác nhận hoặc sửa lỗi ký tự chỉ trong vòng 3–5 giây.

## 5.3. Tình huống thông tin nhận diện giữa các công nghệ không khớp

### Bản chất của hiện tượng Mismatch

Hiện tượng Mismatch xảy ra khi thông tin thu thập từ hai công nghệ độc lập tại cùng một điểm kiểm soát không đồng nhất với nhau. Ví dụ: Đầu đọc RFID đọc ra Mã thẻ E-12345 (gắn liền với biển số 30A-111.11), nhưng camera ANPR chụp và phân tích biển số xe thực tế lại là 30A-999.99.

### Nguyên nhân cốt lõi

Hành vi gian lận thương mại: Chủ xe cố tình tráo đổi thẻ RFID giữa các xe (dùng thẻ của xe con nhỏ dán lên xe tải nặng để giảm phí), dán biển số giả để trốn phí, hoặc sử dụng thẻ RFID bị báo mất/khóa tài khoản.

Lỗi đồng bộ thời gian thời gian thực (Time-Synchronization Error): Độc lập về mặt xung nhịp thời gian giữa thiết bị RFID Controller và ANPR Processor. Khi các xe bám đuôi quá sát (Tailgating), sự lệch thời gian (Δt>200 ms) khiến hệ thống ghép cặp (Matching Engine) nhầm lẫn dữ liệu RFID của xe phía trước với ảnh ANPR của xe phía sau.

### Quy trình xử lý ngoại lệ quy chuẩn

Khởi tạo Mã Hồ sơ Sự cố (Incident Case ID): Ngay khi phát hiện sai lệch thông tin, hệ thống core tự động khóa giao dịch tự động, tạo một Incident ID gắn với các metadata: Thời gian, ID làn, Mã RFID đọc được, Ảnh ANPR toàn cảnh, Ảnh ANPR cận cảnh biển số.

Gán mã OID và lưu vết tự động: Gán mã định danh đối tượng (Object ID - OID) cho toàn bộ gói dữ liệu đa phương tiện và lưu trữ bất biến (Immutable Log) trên hệ thống CSDL trung tâm phục vụ tra cứu pháp lý.

Cảnh báo vi phạm và xử phạt nguội:

Tại trạm đơn làn: Cảnh báo đỏ tại bảng LED làn và màn hình cabin để nhân viên/lực lượng chức năng dừng xe kiểm tra trực tiếp.

Tại trạm đa làn MLFF: Tự động chuyển thông tin về Cục CSGT / Đội quản lý dữ liệu giao thông để phát thông báo vi phạm, phạt nguội và đưa biển số/thẻ vào Danh sách đen (Blacklist) trên toàn hệ thống.

## 5.4. Bảng tổng hợp tình huống và giải pháp

| Tình huống sự cố | Nguyên nhân | Giải pháp kỹ thuật tức thời (hiện trường) | Giải pháp quản lý và vận hành lâu dài |
| --- | --- | --- | --- |
| Không nhận diện được thẻ RFID | Thẻ bị hỏng, lắp sai vị trí, tín hiệu sóng vô tuyến yếu hoặc đầu đọc gặp sự cố. | Kiểm tra thẻ, vị trí dán và đầu đọc; thử đọc lại; sử dụng camera ANPR để hỗ trợ xác minh. | Kiểm tra chất lượng thẻ trước khi phát hành; chuẩn hóa vị trí dán thẻ; bảo trì đầu đọc định kỳ. |
| Nhận diện sai biển số xe (ANPR) | Biển số bị mờ, bẩn, cong vênh; ánh sáng không phù hợp; thuật toán OCR chưa chính xác. | Chụp lại hình ảnh, điều chỉnh camera, đối chiếu với hình ảnh từ camera khác. | Nâng cấp thuật toán nhận diện; bổ sung dữ liệu huấn luyện; kiểm định độ chính xác định kỳ. |
| RFID và ANPR cho kết quả không trùng khớp | Thẻ RFID gắn sai phương tiện, dữ liệu chưa đồng bộ hoặc nhận diện biển số sai. | Tạm giữ giao dịch để xác minh; đối chiếu mã thẻ, biển số và hình ảnh phương tiện. | Xây dựng cơ sở dữ liệu liên kết giữa mã thẻ, biển số và tài khoản giao thông. |
| Camera không nhận diện được khi trời mưa hoặc ban đêm | Mưa lớn, sương mù, ánh sáng yếu, ánh sáng ngược hoặc ống kính bị bám bẩn. | Vệ sinh camera, kiểm tra hệ thống chiếu sáng và kích hoạt camera dự phòng. | Trang bị camera hồng ngoại, cải thiện hệ thống chiếu sáng và nâng cấp thuật toán xử lý hình ảnh. |
| Nhận diện nhầm hai phương tiện đi gần nhau | Phương tiện di chuyển sát nhau, góc camera không phù hợp hoặc cảm biến phát hiện sai. | Kiểm tra hình ảnh toàn cảnh, đối chiếu dữ liệu cảm biến và thời gian ghi nhận. | Tối ưu vị trí camera, bổ sung cảm biến vòng từ và ứng dụng Sensor Fusion. |
| Phân loại sai loại phương tiện | Hình ảnh phương tiện bị che khuất, góc chụp hạn chế hoặc mô hình AI phân loại chưa chính xác. | Kiểm tra hình ảnh thực tế, đối chiếu dữ liệu đăng ký phương tiện và xác minh thủ công. | Huấn luyện AI với nhiều loại phương tiện; kết hợp camera và cảm biến kích thước. |
| Hệ thống xử lý giao dịch chậm | Máy chủ quá tải, đường truyền mạng không ổn định hoặc dữ liệu xử lý quá lớn. | Kiểm tra kết nối, kích hoạt máy chủ dự phòng và lưu dữ liệu tạm thời tại làn. | Nâng cấp hạ tầng mạng, tối ưu máy chủ và ứng dụng Edge AI để giảm độ trễ. |
| Mất kết nối giữa trạm thu phí và trung tâm điều hành | Lỗi mạng, thiết bị truyền dẫn hỏng hoặc sự cố hệ thống trung tâm. | Kích hoạt cơ chế lưu trữ ngoại tuyến, kiểm tra đường truyền và đồng bộ lại dữ liệu khi kết nối phục hồi. | Xây dựng hệ thống truyền dẫn dự phòng, giám sát kết nối và thiết lập quy trình khôi phục dữ liệu. |
| Phương tiện không có thẻ RFID hoặc thẻ không hợp lệ | Người dùng chưa đăng ký dịch vụ, thẻ chưa kích hoạt hoặc tài khoản gặp vấn đề. | Thực hiện xác minh thông tin, hướng dẫn người dùng và xử lý theo quy trình của đơn vị vận hành. | Tăng cường hướng dẫn đăng ký, quản lý vòng đời thẻ và xây dựng quy trình xử lý giao dịch ngoại lệ. |
| Thiết bị nhận diện hoạt động không ổn định | Thiết bị xuống cấp, nhiệt độ môi trường cao, bụi bẩn hoặc thiếu bảo trì. | Kiểm tra nguồn điện, vệ sinh thiết bị và thay thế linh kiện hư hỏng. | Triển khai bảo trì dự đoán (Predictive Maintenance), kiểm định định kỳ và cảnh báo sớm sự cố. |

## 5.5. Đề xuất giải pháp và định hướng phối hợp công nghệ

### 5.5.1. Giải pháp kỹ thuật

#### a. Hoàn thiện khung chuẩn hóa dữ liệu và giao thức truyền thông

Để nâng cao hiệu quả hoạt động của hệ thống ETC, cần xây dựng một khung chuẩn hóa dữ liệu thống nhất giữa các công nghệ nhận diện như RFID, ANPR/LPR và các thiết bị cảm biến. Việc sử dụng các định dạng dữ liệu khác nhau có thể gây khó khăn trong quá trình trao đổi, đồng bộ và đối chiếu thông tin giữa các hệ thống.

Do đó, cần thống nhất các thông tin cơ bản như mã thẻ RFID, biển số phương tiện, thời gian giao dịch và hình ảnh nhận diện. Đồng thời, chuẩn hóa giao thức truyền thông giữa các thiết bị và hệ thống trung tâm nhằm bảo đảm dữ liệu được truyền tải nhanh chóng, chính xác và an toàn. Giải pháp này không chỉ hạn chế sai lệch thông tin mà còn tạo điều kiện thuận lợi cho việc tích hợp các công nghệ mới trong tương lai.

#### b. Đẩy mạnh tích hợp Trí tuệ Nhân tạo Biên (Edge AI) và Cảm biến Hợp nhất (Sensor Fusion)

Bên cạnh việc cải thiện hạ tầng kỹ thuật, cần đẩy mạnh ứng dụng trí tuệ nhân tạo biên (Edge AI) trong quá trình nhận diện phương tiện. Công nghệ này cho phép xử lý dữ liệu trực tiếp tại camera hoặc thiết bị đặt ở trạm thu phí, giúp giảm thời gian truyền dữ liệu về máy chủ trung tâm và nâng cao tốc độ phản hồi của hệ thống.

Ngoài ra, việc kết hợp cảm biến hợp nhất (Sensor Fusion) giúp tận dụng ưu điểm của nhiều công nghệ nhận diện khác nhau. Cụ thể, RFID được sử dụng để xác định mã định danh phương tiện, ANPR/LPR hỗ trợ nhận diện biển số, trong khi các cảm biến khác giúp xác định sự hiện diện và vị trí phương tiện. Dữ liệu từ các thiết bị sẽ được đối chiếu nhằm tăng độ chính xác và hạn chế trường hợp nhận diện sai. Đây là giải pháp phù hợp để khắc phục những hạn chế khi chỉ sử dụng một công nghệ nhận diện riêng lẻ.

### 5.5.2. Giải pháp quy trình vận hành

#### a. Thiết lập Cơ chế Xử lý Ngoại lệ và Chính sách Ân hạn (Grace Period)

Trong quá trình vận hành hệ thống ETC, có thể phát sinh một số tình huống như đầu đọc RFID không nhận được thẻ, camera nhận diện sai biển số, thông tin tài khoản không đồng bộ hoặc kết nối mạng bị gián đoạn. Vì vậy, cần xây dựng cơ chế xử lý ngoại lệ nhằm bảo đảm các giao dịch gặp sự cố vẫn được ghi nhận và kiểm tra đầy đủ.

Cụ thể, khi hệ thống RFID gặp lỗi, camera ANPR/LPR có thể hỗ trợ ghi nhận biển số và hình ảnh phương tiện để phục vụ xác minh. Đối với những trường hợp thông tin giữa thẻ và biển số không trùng khớp, giao dịch cần được chuyển sang trạng thái kiểm tra thay vì tự động xác nhận. Bên cạnh đó, cần áp dụng chính sách ân hạn (Grace Period) hợp lý, cho phép người dùng bổ sung thông tin hoặc hoàn tất thanh toán khi phát sinh lỗi kỹ thuật. Giải pháp này góp phần hạn chế tranh chấp, nâng cao tính minh bạch và bảo đảm quyền lợi của người tham gia giao thông.

#### b. Chuẩn hóa Quy trình Lắp đặt, Kiểm định và Bảo trì Dự phòng (Predictive Maintenance)

Chất lượng thiết bị và điều kiện lắp đặt có ảnh hưởng trực tiếp đến độ chính xác của các công nghệ nhận diện. Vì vậy, cần chuẩn hóa quy trình lắp đặt camera, đầu đọc RFID và các cảm biến để bảo đảm thiết bị hoạt động đúng vị trí, phạm vi và điều kiện kỹ thuật. Trước khi đưa vào sử dụng, hệ thống cần được kiểm định trong nhiều điều kiện khác nhau như ban ngày, ban đêm, trời mưa hoặc khi phương tiện di chuyển với tốc độ cao.

Bên cạnh đó, cần chú trọng công tác bảo trì dự phòng và từng bước ứng dụng bảo trì dự đoán (Predictive Maintenance). Thông qua việc theo dõi tình trạng hoạt động của thiết bị, hệ thống có thể phát hiện sớm các dấu hiệu bất thường như chất lượng hình ảnh camera suy giảm, đầu đọc RFID hoạt động không ổn định hoặc lỗi kết nối. Từ đó, đơn vị vận hành có thể chủ động kiểm tra và sửa chữa trước khi xảy ra sự cố nghiêm trọng. Điều này giúp giảm chi phí bảo trì, hạn chế gián đoạn và duy trì hiệu quả hoạt động lâu dài của hệ thống ETC.
