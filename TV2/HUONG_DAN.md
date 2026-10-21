## Sản phẩm

- tao_du_lieu.py: tạo dữ liệu, kiểm tra và lưu CSV.
- du_lieu/xe_dang_ky.csv: 6 xe, gồm ma_xe, ma_the, bien_so.
- du_lieu/luot_xe.csv: 12 lượt, gồm ma_luot, kich_ban, xe_thuc_te, rfid_nhan_duoc, bien_so_nhan_duoc.

Ô trống trong hai cột nhận được nghĩa là không đọc được.
TAG999 và 99Z-99999 là các giá trị chưa đăng ký được cố ý đưa vào để kiểm thử.
Sai dữ liệu đọc khác với lỗi cấu trúc dữ liệu: chương trình cho phép dữ liệu đọc thiếu/sai, nhưng chặn xe đăng ký thiếu/trùng, mã lượt trùng và xe thực tế không tồn tại.

## Các thành viên khác sử dụng

- Phần RFID dùng xe_dang_ky.csv để tra cứu rfid_nhan_duoc theo ma_the.
- Phần ANPR dùng xe_dang_ky.csv để tra cứu bien_so_nhan_duoc theo bien_so.
- Phần phối hợp đối chiếu hai kết quả tra cứu của cùng ma_luot.
- Phần tổng hợp dùng xe_thuc_te để đánh giá sau quyết định. Không truyền xe_thuc_te vào hàm nhận diện.
- Có thể đọc CSV bằng csv.DictReader với encoding="utf-8-sig".

Mọi dữ liệu đều giả lập. Bộ tình huống phục vụ kiểm tra quy tắc, không thể hiện tỷ lệ lỗi hay độ chính xác công nghệ thực tế. Có trường hợp cả hai nguồn cùng khớp sai; khớp nhau không bảo đảm đúng phương tiện.
