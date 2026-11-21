# Mô phỏng phối hợp RFID và ANPR/LPR — mục 6.4

Giải nén file ZIP. Giữ nguyên thư mục `TV4` và thư mục ảnh bên trong để báo cáo Markdown hiển thị được hình.

## Các phần bàn giao

- `Chương_5.md`: nội dung chương 5 từ bản Word trên nhánh TV4.
- `Chương_6_6.4.md`: báo cáo 6.4 đã cập nhật theo code và kết quả chạy mới.
- `hinh_anh/`: bốn ảnh minh họa được liên kết trong báo cáo 6.4.
- `mo_phong_phoi_hop.py`: chương trình phối hợp hai nguồn.
- `test_phoi_hop.py`: kiểm thử tự động.
- Ba CSV đầu vào và `ket_qua_phoi_hop.csv`: dữ liệu chạy thử và kết quả.

## Cách chạy

Mở terminal tại thư mục chứa thư mục `TV4` sau khi giải nén:

```sh
python TV4/mo_phong_phoi_hop.py
python -m unittest discover -s TV4 -p "test_*.py" -v
```

Chỉ cần Python 3, không cần cài thư viện ngoài hoặc giao diện.

## Dữ liệu đầu vào

- `luot_xe.csv`: bản sao dữ liệu 6.1 trên nhánh TV2; dùng `ma_luot` để xác định các lượt cần xử lý.
- `ket_qua_rfid.csv`: kết quả từ TV1, commit `d141d97`.
- `ket_qua_anpr.csv`: kết quả từ TV3, commit `8066f19`.

Hai file kết quả giữ nguyên nội dung từ các nhánh tương ứng. Khi TV1 hoặc TV3 cập nhật kết quả, thay bản sao này rồi chạy lại. Có thể chọn file khác bằng `--luot-xe`, `--rfid`, `--anpr` và chọn nơi lưu bằng `--output`.

## Quy tắc phối hợp

Ghép kết quả theo cùng `ma_luot`. Chỉ chấp nhận khi cả hai nguồn có trạng thái `CHAP_NHAN` và cùng trả về một `ma_xe_nhan_dien`. Thiếu kết quả, nhận diện thất bại hoặc hai mã xe không khớp đều chuyển xác minh. Không đối chiếu trực tiếp mã thẻ với biển số; không sử dụng `xe_thuc_te` để quyết định chấp nhận.

Chương trình báo lỗi nếu CSV sai số cột, thiếu cột cần thiết, mã lượt trống/trùng, trạng thái không hợp lệ, chấp nhận mà thiếu mã xe hoặc có mã lượt ngoài danh sách đầu vào.

## Kết quả bàn giao cho TV5

File `ket_qua_phoi_hop.csv` có các cột `ma_luot`, `ma_xe_rfid`, `ma_xe_anpr`, `trang_thai`, `ma_xe_nhan_dien`, `ly_do`. Trạng thái gồm `CHAP_NHAN` và `CHUYEN_XAC_MINH`; mã xe kết quả để trống khi chuyển xác minh.

Với 12 lượt hiện tại: chấp nhận L01, L02, L09; chuyển xác minh 9 lượt còn lại. L09 là trường hợp hai nguồn cùng khớp sai: chương trình vẫn chấp nhận XE02 trong khi xe thực tế là XE01. Khi TV5 đối chiếu với `xe_thuc_te`, kết quả là 2 lượt đúng tự động, 1 lượt chấp nhận sai và 9 lượt chuyển xác minh. Tỷ lệ chấp nhận không đồng nghĩa với tỷ lệ định danh đúng.

Đây là mô phỏng quy tắc xử lý trên dữ liệu giả lập, không phải đo độ chính xác của thiết bị thực tế.
