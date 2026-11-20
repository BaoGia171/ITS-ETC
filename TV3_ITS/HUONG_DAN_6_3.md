# HƯỚNG DẪN CHẠY MÔ PHỎNG ANPR/LPR – MỤC 6.3

## 1. Phạm vi

Chương trình chỉ tra cứu chuỗi biển số giả lập, **không xử lý ảnh hoặc video**. Dữ liệu ở `du_lieu/` được sao chép theo đúng nội dung nhánh GitHub `TV2/TV2` của phần 6.1 tại thời điểm xây dựng bộ bàn giao. Không cần `pip install` thư viện nào.

## 2. Cấu trúc thư mục

```text
TV3/
├── mo_phong_anpr.py
├── du_lieu/
│   ├── xe_dang_ky.csv
│   └── luot_xe.csv
├── ket_qua/
│   └── ket_qua_anpr.csv
├── tests/
│   └── test_mo_phong_anpr.py
├── Chương_6_6.3.md
└── HUONG_DAN_6_3.md
```

## 3. Cách chạy (Windows PowerShell hoặc VS Code Terminal)

Di chuyển vào thư mục của bộ chương trình, sau đó chạy:

```powershell
python mo_phong_anpr.py
```

Kết quả được in ra terminal và lưu vào `ket_qua/ket_qua_anpr.csv` (UTF-8 BOM để thuận tiện mở bằng Excel).

Chạy kiểm thử tự động:

```powershell
python -m unittest discover -s tests -v
```

Nếu tách phần 6.3 sang nhánh GitHub riêng, bạn có thể chỉ định dữ liệu gốc của 6.1 mà không cần sửa code:

```powershell
python mo_phong_anpr.py --xe-dang-ky "../TV2/du_lieu/xe_dang_ky.csv" --luot-xe "../TV2/du_lieu/luot_xe.csv" --output "ket_qua/ket_qua_anpr.csv"
```

**Lưu ý:** đường dẫn `../TV2/...` chỉ là ví dụ, cần sửa theo vị trí thư mục thực tế trên máy. Khi chạy mặc định, chương trình dùng bản sao dữ liệu 6.1 có trong gói.

## 4. Quy tắc ra quyết định

- Chuẩn hóa biển số bằng cách chuyển chữ hoa, loại bỏ dấu `-`, dấu `.` và khoảng trắng (không tự sửa lỗi OCR).
- Nếu không đọc được biển số: `CHUYEN_XAC_MINH`, `KHONG_DOC_DUOC_BIEN_SO`.
- Nếu đọc được nhưng biển số chưa đăng ký: `CHUYEN_XAC_MINH`, `BIEN_SO_CHUA_DANG_KY`.
- Nếu tra cứu thấy biển số: `CHAP_NHAN`, trả về mã xe tương ứng và `TIM_THAY_BIEN_SO`.
- Chỉ dùng `ma_luot`, `bien_so_nhan_duoc`, cùng `ma_xe`/`bien_so` trong bảng đăng ký để ra quyết định. Không dùng `xe_thuc_te`, `kich_ban`, hoặc `rfid_nhan_duoc`.

## 5. Định dạng đầu ra để dùng lại ở mục 6.4 và 6.5

`ket_qua_anpr.csv` gồm: `ma_luot,bien_so_nhan_duoc,bien_so_chuan_hoa,trang_thai,ma_xe_nhan_dien,ly_do`.

- 6.4 có thể ghép kết quả ANPR và RFID theo `ma_luot` để so sánh `ma_xe_nhan_dien`.
- 6.5 có thể ghép theo `ma_luot` với `luot_xe.csv`, sau đó mới dùng `xe_thuc_te` để phân loại đúng/sai và tính thống kê.
- Quy ước trạng thái/lý do phải được nhóm thống nhất với mô-đun RFID và phối hợp khi tích hợp.

## 6. Kết quả từ 12 lượt thử nghiệm

- 5 lượt định danh đúng tự động: L01, L02, L03, L06, L10.
- 3 lượt chấp nhận sai: L07, L08, L09.
- 4 lượt chuyển xác minh: L04, L05, L11, L12.

Tỷ lệ tương ứng trên 12 lượt: 41,67%; 25,00%; 33,33%. Các số liệu này là kết quả **bộ kịch bản cố định**, không đại diện hiệu năng thực tế.

## 7. Nguồn đầu vào

- `https://github.com/BaoGia171/ITS-ETC/blob/TV2/TV2/tao_du_lieu.py`
- `https://github.com/BaoGia171/ITS-ETC/tree/TV2/TV2/du_lieu`
- `https://github.com/BaoGia171/ITS-ETC/blob/TV2/TV2/Chuong_6_6.1.md`

## 8. Gói bàn giao TV3

`Chương_4.md` và `Chương_6_6.3.md` giữ nội dung báo cáo. Mã thực thi nằm ở `mo_phong_anpr.py`; dữ liệu và kết quả nằm trong `du_lieu/` và `ket_qua/`. Các hình 6.3 được đặt trong `hinh_anh/` và liên kết từ Markdown.
