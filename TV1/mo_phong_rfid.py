
"""
Chuong 6.2: Mo phong nhan dien phuong tien bang RFID.

Dau vao:
- Danh sach the RFID da dang ky.
- Ma RFID nhan duoc tai tram.

Chi su dung RFID de nhan dien.
KHONG su dung xe_thuc_te hoac bien_so_nhan_duoc
de quyet dinh ket qua.

Chi su dung thu vien chuan Python.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


# ==============================
# 1. KHAI BAO TRANG THAI
# ==============================

CHAP_NHAN = "CHAP_NHAN"
CHUYEN_XAC_MINH = "CHUYEN_XAC_MINH"

COT_KET_QUA = (
    "ma_luot",
    "kich_ban",
    "rfid_nhan_duoc",
    "ma_the_chuan_hoa",
    "trang_thai",
    "ma_xe_nhan_dien",
    "ly_do"
)


# ==============================
# 2. CHUAN HOA MA RFID
# ==============================

def chuan_hoa_rfid(ma_the: str | None) -> str:
    """
    Chuan hoa ma RFID:
    - Chuyen thanh chu in hoa.
    - Loai bo khoang trang.
    - Khong tu sua ma RFID bi sai.
    """

    if ma_the is None:
        return ""

    if not isinstance(ma_the, str):
        raise TypeError("Ma RFID phai la chuoi hoac None")

    return "".join(
        c for c in ma_the.upper()
        if not c.isspace()
    )


# ==============================
# 3. DOC DU LIEU CSV
# ==============================

def doc_csv(
    duong_dan: Path,
    cot_bat_buoc: set[str]
) -> list[dict[str, str]]:

    with duong_dan.open(
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as tep:

        reader = csv.DictReader(tep)

        # Kiem tra dong tieu de
        if reader.fieldnames is None:
            raise ValueError(
                f"File CSV khong co dong tieu de: {duong_dan}"
            )

        # Kiem tra cot bat buoc
        thieu = cot_bat_buoc - set(reader.fieldnames)

        if thieu:
            raise ValueError(
                f"{duong_dan.name} thieu cot: "
                f"{', '.join(sorted(thieu))}"
            )

        rows = list(reader)

    # Kiem tra file rong
    if not rows:
        raise ValueError(
            f"File CSV khong co du lieu: {duong_dan}"
        )

    # Kiem tra dong thua cot
    if any(None in dong for dong in rows):
        raise ValueError(
            f"Dong CSV co so truong khong hop le: {duong_dan}"
        )

    return rows


# ==============================
# 4. TAO BANG TRA CUU THE RFID
# ==============================

def tao_bang_tra_cuu(
    danh_sach_xe: list[dict[str, str]]
) -> dict[str, str]:
    """
    Tao bang tra cuu:
    Ma the RFID -> Ma xe.

    Kiem tra ma xe va ma the bi trung
    hoac bi thieu.
    """

    bang = {}

    ma_xe_da_co = set()

    for i, xe in enumerate(danh_sach_xe, start=1):

        ma_xe = (xe.get("ma_xe") or "").strip()

        ma_the = chuan_hoa_rfid(
            xe.get("ma_the")
        )

        # Kiem tra du lieu rong
        if not ma_xe or not ma_the:
            raise ValueError(
                f"Dong dang ky {i} thieu ma xe hoac ma the"
            )

        # Kiem tra ma xe trung
        if ma_xe in ma_xe_da_co:
            raise ValueError(
                f"Ma xe bi trung: {ma_xe}"
            )

        # Kiem tra ma the trung
        if ma_the in bang:
            raise ValueError(
                f"Ma the RFID bi trung sau chuan hoa: {ma_the}"
            )

        bang[ma_the] = ma_xe

        ma_xe_da_co.add(ma_xe)

    return bang


# ==============================
# 5. NHAN DIEN PHUONG TIEN RFID
# ==============================

def nhan_dien_rfid(
    ma_luot: str,
    kich_ban: str,
    rfid_nhan_duoc: str | None,
    bang_tra_cuu: dict[str, str]
) -> dict[str, str]:
    """
    Nhan dien phuong tien chi dua tren ma RFID.

    Khong su dung:
    - xe_thuc_te
    - bien_so_nhan_duoc

    De tranh su dung thong tin dap an
    trong qua trinh nhan dien.
    """

    # Chuan hoa ma RFID nhan duoc
    ma_the_chuan_hoa = chuan_hoa_rfid(
        rfid_nhan_duoc
    )

    # Khoi tao ket qua
    ket_qua = {
        "ma_luot": ma_luot,
        "kich_ban": kich_ban,
        "rfid_nhan_duoc": rfid_nhan_duoc or "",
        "ma_the_chuan_hoa": ma_the_chuan_hoa,
        "trang_thai": CHUYEN_XAC_MINH,
        "ma_xe_nhan_dien": "",
        "ly_do": ""
    }

    # Truong hop khong doc duoc the
    if not ma_the_chuan_hoa:

        ket_qua["ly_do"] = "KHONG_DOC_DUOC_RFID"

    # Truong hop the chua dang ky
    elif ma_the_chuan_hoa not in bang_tra_cuu:

        ket_qua["ly_do"] = "THE_RFID_CHUA_DANG_KY"

    # Truong hop tim thay the trong co so du lieu
    else:

        ket_qua["trang_thai"] = CHAP_NHAN

        ket_qua["ma_xe_nhan_dien"] = (
            bang_tra_cuu[ma_the_chuan_hoa]
        )

        ket_qua["ly_do"] = "TIM_THAY_THE_RFID"

    return ket_qua


# ==============================
# 6. CHAY MO PHONG RFID
# ==============================

def chay_mo_phong(
    xe_dang_ky: Path,
    luot_xe: Path
) -> list[dict[str, str]]:

    # Doc danh sach xe dang ky
    xe = doc_csv(
        xe_dang_ky,
        {"ma_xe", "ma_the"}
    )

    # Doc danh sach luot xe
    luot = doc_csv(
        luot_xe,
        {"ma_luot", "kich_ban", "rfid_nhan_duoc"}
    )

    # Tao bang tra cuu RFID
    bang = tao_bang_tra_cuu(xe)

    cac_ma_luot = set()

    ket_qua = []

    # Xu ly tung luot xe
    for dong in luot:

        ma_luot = (
            dong.get("ma_luot") or ""
        ).strip()

        kich_ban = (
            dong.get("kich_ban") or ""
        ).strip()

        # Kiem tra ma luot
        if not ma_luot or ma_luot in cac_ma_luot:

            raise ValueError(
                f"Ma luot thieu hoac bi trung: {ma_luot!r}"
            )

        cac_ma_luot.add(ma_luot)

        # Chi lay ma RFID de nhan dien
        ket_qua.append(
            nhan_dien_rfid(
                ma_luot,
                kich_ban,
                dong.get("rfid_nhan_duoc"),
                bang
            )
        )

    return ket_qua


# ==============================
# 7. GHI KET QUA RA FILE CSV
# ==============================

def ghi_ket_qua_csv(
    duong_dan: Path,
    ket_qua: list[dict[str, str]]
) -> None:

    # Tao thu muc neu chua ton tai
    duong_dan.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with duong_dan.open(
        "w",
        encoding="utf-8-sig",
        newline=""
    ) as tep:

        writer = csv.DictWriter(
            tep,
            fieldnames=COT_KET_QUA
        )

        writer.writeheader()

        writer.writerows(ket_qua)


# ==============================
# 8. THONG KE KET QUA
# ==============================

def thong_ke(ket_qua: list[dict[str, str]]) -> None:

    chap_nhan = sum(
        1 for dong in ket_qua
        if dong["trang_thai"] == CHAP_NHAN
    )

    chuyen_xac_minh = sum(
        1 for dong in ket_qua
        if dong["trang_thai"] == CHUYEN_XAC_MINH
    )

    tong = len(ket_qua)

    print("\n===== THONG KE KET QUA =====")

    print("Tong so luot xe:", tong)
    print("So luot chap nhan:", chap_nhan)
    print("So luot chuyen xac minh:", chuyen_xac_minh)

    if tong > 0:
        print(
            "Ty le chap nhan:",
            round(chap_nhan / tong * 100, 2),
            "%"
        )


# ==============================
# 9. CHUONG TRINH CHINH
# ==============================

def main() -> None:

    # Xac dinh thu muc chuong trinh
    thu_muc = Path(__file__).resolve().parent

    parser = argparse.ArgumentParser(
        description="Mo phong nhan dien phuong tien bang RFID"
    )

    # File dang ky phuong tien
    parser.add_argument(
        "--xe-dang-ky",
        type=Path,
        default=thu_muc / "du_lieu" / "xe_dang_ky.csv"
    )

    # File cac luot xe
    parser.add_argument(
        "--luot-xe",
        type=Path,
        default=thu_muc / "du_lieu" / "luot_xe.csv"
    )

    # File ket qua
    parser.add_argument(
        "--output",
        type=Path,
        default=thu_muc / "ket_qua" / "ket_qua_rfid.csv"
    )

    args = parser.parse_args()

    # Chay mo phong
    ket_qua = chay_mo_phong(
        args.xe_dang_ky,
        args.luot_xe
    )

    # Ghi ket qua CSV
    ghi_ket_qua_csv(
        args.output,
        ket_qua
    )

    # Hien thi ket qua
    print(
        f"Da xu ly {len(ket_qua)} luot xe."
    )

    print(
        f"Da luu ket qua tai: {args.output}"
    )

    print(
        f"\n{'Luot':<8}"
        f"{'Kich ban':<30}"
        f"{'Ma the':<18}"
        f"{'Ma xe':<12}"
        f"{'Trang thai':<20}"
        f"Ly do"
    )

    for dong in ket_qua:

        print(
            f"{dong['ma_luot']:<8}"
            f"{dong['kich_ban']:<30}"
            f"{dong['rfid_nhan_duoc'] or '-':<18}"
            f"{dong['ma_xe_nhan_dien'] or '-':<12}"
            f"{dong['trang_thai']:<20}"
            f"{dong['ly_do']}"
        )

    # Thong ke
    thong_ke(ket_qua)


# ==============================
# 10. KHOI CHAY CHUONG TRINH
# ==============================

if __name__ == "__main__":
    main()
