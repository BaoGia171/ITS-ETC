"""Phần 6.1 — Tạo và kiểm tra dữ liệu giả lập.
Chạy: python TV2/tao_du_lieu.py
Chỉ dùng thư viện có sẵn của Python. Không có dữ liệu cá nhân thật.
"""
import csv
from pathlib import Path


def tao_danh_sach_xe():
    """Danh sách đăng ký: mỗi xe có một mã thẻ và một biển số."""
    return [
        {"ma_xe": f"XE{i:02}", "ma_the": f"TAG{i:03}", "bien_so": f"51A-{10000+i}"}
        for i in range(1, 7)
    ]


def tao_luot_xe():
    """Mã thẻ/biển số bên dưới là kết quả đọc giả lập, không đọc từ thiết bị."""
    mau = [
        # Kịch bản, xe thực tế, thẻ nhận được, biển số nhận được
        ("hai_nguon_dung", "XE01", "TAG001", "51A-10001"),
        ("hai_nguon_dung", "XE04", "TAG004", "51A-10004"),
        ("thieu_rfid", "XE01", "", "51A-10001"),
        ("thieu_bien_so", "XE02", "TAG002", ""),
        ("thieu_ca_hai", "XE03", "", ""),
        ("rfid_sai_bien_so_dung", "XE01", "TAG002", "51A-10001"),
        ("rfid_dung_bien_so_sai", "XE02", "TAG002", "51A-10003"),
        ("hai_nguon_sai_khong_khop", "XE01", "TAG002", "51A-10003"),
        ("hai_nguon_cung_khop_sai", "XE01", "TAG002", "51A-10002"),
        ("the_chua_dang_ky", "XE04", "TAG999", "51A-10004"),
        ("bien_so_chua_dang_ky", "XE05", "TAG005", "99Z-99999"),
        ("ca_hai_chua_dang_ky", "XE06", "TAG999", "99Z-99999"),
    ]
    return [
        {
            "ma_luot": f"L{i:02}",
            "kich_ban": kich_ban,
            "xe_thuc_te": xe,
            "rfid_nhan_duoc": the,
            "bien_so_nhan_duoc": bien,
        }
        for i, (kich_ban, xe, the, bien) in enumerate(mau, 1)
    ]


def kiem_tra_du_lieu(danh_sach_xe, luot_xe):
    """Thông tin đăng ký phải đủ và duy nhất; dữ liệu đọc có thể thiếu hoặc sai."""
    if not danh_sach_xe or not luot_xe:
        raise ValueError("Danh sách xe và lượt xe không được rỗng.")

    for cot in ("ma_xe", "ma_the", "bien_so"):
        da_co = set()
        for xe in danh_sach_xe:
            gia_tri = xe.get(cot, "")
            if not isinstance(gia_tri, str) or not gia_tri.strip():
                raise ValueError(f"Xe đăng ký thiếu hoặc sai dữ liệu ở cột {cot}.")
            gia_tri = gia_tri.strip().upper()
            if gia_tri in da_co:
                raise ValueError(f"Danh sách xe bị trùng {cot}: {gia_tri}.")
            da_co.add(gia_tri)

    cac_ma_xe = {xe["ma_xe"] for xe in danh_sach_xe}
    cac_ma_luot = set()
    for luot in luot_xe:
        for cot in ("ma_luot", "kich_ban", "xe_thuc_te", "rfid_nhan_duoc", "bien_so_nhan_duoc"):
            if cot not in luot or not isinstance(luot[cot], str):
                raise ValueError(f"Lượt xe thiếu hoặc sai kiểu dữ liệu ở cột {cot}.")
        if not luot["ma_luot"].strip() or not luot["kich_ban"].strip():
            raise ValueError("Mã lượt và tên kịch bản không được trống.")
        if luot["ma_luot"] in cac_ma_luot:
            raise ValueError(f"Trùng mã lượt: {luot['ma_luot']}.")
        if luot["xe_thuc_te"] not in cac_ma_xe:
            raise ValueError(f"Xe thực tế chưa có trong danh sách: {luot['xe_thuc_te']}.")
        cac_ma_luot.add(luot["ma_luot"])
        # Không bác bỏ thẻ/biển số đọc sai, lạ hoặc trống:
        # đây là các tình huống cần đưa cho ba phương án xử lý.


def ghi_csv(duong_dan, cac_dong):
    with duong_dan.open("w", encoding="utf-8-sig", newline="") as tep:
        ghi = csv.DictWriter(tep, fieldnames=list(cac_dong[0]))
        ghi.writeheader()
        ghi.writerows(cac_dong)


def main():
    danh_sach_xe = tao_danh_sach_xe()
    luot_xe = tao_luot_xe()
    kiem_tra_du_lieu(danh_sach_xe, luot_xe)

    thu_muc = Path(__file__).resolve().parent / "du_lieu"
    thu_muc.mkdir(exist_ok=True)
    ghi_csv(thu_muc / "xe_dang_ky.csv", danh_sach_xe)
    ghi_csv(thu_muc / "luot_xe.csv", luot_xe)
    print(f"Kiểm tra đạt: {len(danh_sach_xe)} xe đăng ký, {len(luot_xe)} lượt thử nghiệm.")
    print("Đã lưu xe_dang_ky.csv và luot_xe.csv tại:", thu_muc)


if __name__ == "__main__":
    main()
