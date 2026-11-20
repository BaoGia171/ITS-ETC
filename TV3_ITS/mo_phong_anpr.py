"""Chương 6.3: mô phỏng tra cứu phương tiện bằng biển số ANPR/LPR giả lập.

Đầu vào là kết quả đọc biển số dạng chuỗi, KHÔNG phải ảnh/camera.
Chỉ dùng thư viện chuẩn Python. Không sử dụng xe_thuc_te để nhận diện.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

CHAP_NHAN = "CHAP_NHAN"
CHUYEN_XAC_MINH = "CHUYEN_XAC_MINH"

COT_KET_QUA = (
    "ma_luot", "bien_so_nhan_duoc", "bien_so_chuan_hoa",
    "trang_thai", "ma_xe_nhan_dien", "ly_do"
)


def chuan_hoa_bien_so(bien_so: str | None) -> str:
    """Chuẩn hóa kiểu viết: xóa khoảng trắng, dấu gạch ngang và dấu chấm, in hoa.

    Chỉ hỗ trợ chuẩn hóa chuỗi đã nhận được; không tự sửa lỗi OCR, không đoán ký tự.
    """
    if bien_so is None:
        return ""
    if not isinstance(bien_so, str):
        raise TypeError("Biển số phải là chuỗi hoặc None")
    return "".join(c for c in bien_so.upper() if not c.isspace() and c not in "-.")


def doc_csv(duong_dan: Path, cot_bat_buoc: set[str]) -> list[dict[str, str]]:
    with duong_dan.open("r", encoding="utf-8-sig", newline="") as tep:
        reader = csv.DictReader(tep)
        if reader.fieldnames is None:
            raise ValueError(f"File CSV không có dòng tiêu đề: {duong_dan}")
        thieu = cot_bat_buoc - set(reader.fieldnames)
        if thieu:
            raise ValueError(f"{duong_dan.name} thiếu cột: {', '.join(sorted(thieu))}")
        rows = list(reader)
    if not rows:
        raise ValueError(f"File CSV không có dữ liệu: {duong_dan}")
    if any(None in dong for dong in rows):
        raise ValueError(f"Dòng CSV có số trường không hợp lệ: {duong_dan}")
    return rows


def tao_bang_tra_cuu(danh_sach_xe: list[dict[str, str]]) -> dict[str, str]:
    """Tạo ánh xạ biển số chuẩn hóa -> mã xe; bác bỏ dữ liệu đăng ký trùng/thiếu."""
    bang = {}
    ma_xe_da_co = set()
    for i, xe in enumerate(danh_sach_xe, start=1):
        ma_xe = (xe.get("ma_xe") or "").strip()
        bien_so = chuan_hoa_bien_so(xe.get("bien_so"))
        if not ma_xe or not bien_so:
            raise ValueError(f"Dòng đăng ký {i} thiếu mã xe hoặc biển số")
        if ma_xe in ma_xe_da_co:
            raise ValueError(f"Mã xe bị trùng trong danh sách đăng ký: {ma_xe}")
        if bien_so in bang:
            raise ValueError(f"Biển số bị trùng sau chuẩn hóa: {xe.get('bien_so')}")
        bang[bien_so] = ma_xe
        ma_xe_da_co.add(ma_xe)
    return bang


def nhan_dien_anpr(ma_luot: str, bien_so_nhan_duoc: str | None,
                  bang_tra_cuu: dict[str, str]) -> dict[str, str]:
    """Ra quyết định CHỈ từ biển số nhận được và bảng đăng ký.

    Không nhận tham số xe_thuc_te hoặc rfid_nhan_duoc để tránh rò rỉ đáp án.
    """
    chuan_hoa = chuan_hoa_bien_so(bien_so_nhan_duoc)
    ket_qua = {
        "ma_luot": ma_luot,
        "bien_so_nhan_duoc": bien_so_nhan_duoc or "",
        "bien_so_chuan_hoa": chuan_hoa,
        "trang_thai": CHUYEN_XAC_MINH,
        "ma_xe_nhan_dien": "",
        "ly_do": "",
    }
    if not chuan_hoa:
        ket_qua["ly_do"] = "KHONG_DOC_DUOC_BIEN_SO"
    elif chuan_hoa not in bang_tra_cuu:
        ket_qua["ly_do"] = "BIEN_SO_CHUA_DANG_KY"
    else:
        ket_qua["trang_thai"] = CHAP_NHAN
        ket_qua["ma_xe_nhan_dien"] = bang_tra_cuu[chuan_hoa]
        ket_qua["ly_do"] = "TIM_THAY_BIEN_SO"
    return ket_qua


def chay_mo_phong(xe_dang_ky: Path, luot_xe: Path) -> list[dict[str, str]]:
    xe = doc_csv(xe_dang_ky, {"ma_xe", "bien_so"})
    luot = doc_csv(luot_xe, {"ma_luot", "bien_so_nhan_duoc"})
    bang = tao_bang_tra_cuu(xe)
    cac_ma_luot = set()
    ket_qua = []
    for dong in luot:
        ma_luot = (dong.get("ma_luot") or "").strip()
        if not ma_luot or ma_luot in cac_ma_luot:
            raise ValueError(f"Mã lượt thiếu hoặc bị trùng: {ma_luot!r}")
        cac_ma_luot.add(ma_luot)
        ket_qua.append(nhan_dien_anpr(ma_luot, dong.get("bien_so_nhan_duoc"), bang))
    return ket_qua


def ghi_ket_qua_csv(duong_dan: Path, ket_qua: list[dict[str, str]]) -> None:
    duong_dan.parent.mkdir(parents=True, exist_ok=True)
    with duong_dan.open("w", encoding="utf-8-sig", newline="") as tep:
        writer = csv.DictWriter(tep, fieldnames=COT_KET_QUA)
        writer.writeheader()
        writer.writerows(ket_qua)


def main() -> None:
    thu_muc = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--xe-dang-ky", type=Path,
                        default=thu_muc / "du_lieu" / "xe_dang_ky.csv")
    parser.add_argument("--luot-xe", type=Path,
                        default=thu_muc / "du_lieu" / "luot_xe.csv")
    parser.add_argument("--output", type=Path,
                        default=thu_muc / "ket_qua" / "ket_qua_anpr.csv")
    args = parser.parse_args()
    ket_qua = chay_mo_phong(args.xe_dang_ky, args.luot_xe)
    ghi_ket_qua_csv(args.output, ket_qua)
    print(f"Đã xử lý {len(ket_qua)} lượt xe; lưu kết quả tại: {args.output}")
    print(f"{'Lượt':<6}{'Biển số đọc':<16}{'Mã xe':<10}{'Trạng thái':<20}Lý do")
    for dong in ket_qua:
        print(f"{dong['ma_luot']:<6}{dong['bien_so_nhan_duoc']:<16}"
              f"{dong['ma_xe_nhan_dien'] or '-':<10}{dong['trang_thai']:<20}{dong['ly_do']}")


if __name__ == "__main__":
    main()
