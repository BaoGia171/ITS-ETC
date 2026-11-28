from __future__ import annotations
import argparse
import sys
from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd

TEN_FILE = {
    "luot_xe": "luot_xe.csv",
    "rfid": "ket_qua_rfid.csv",
    "anpr": "ket_qua_anpr.csv",
    "phoi_hop": "ket_qua_phoi_hop.csv",
}

TRANG_THAI_HOP_LE = {"CHAP_NHAN", "CHUYEN_XAC_MINH"}

# Bo kiem thu hoi quy co dinh cho bo du lieu mau L01-L12.
# Fixture nay tach rieng voi du lieu doc tu CSV, khong tao du lieu dau vao khi chay.
MA_LUOT_MAU = [f"L{i:02d}" for i in range(1, 13)]
XE_THUC_TE_MAU = {
    "L01": "XE01", "L02": "XE04", "L03": "XE01", "L04": "XE02",
    "L05": "XE03", "L06": "XE01", "L07": "XE02", "L08": "XE01",
    "L09": "XE01", "L10": "XE04", "L11": "XE05", "L12": "XE06",
}
KET_QUA_MAU = {
    "RFID": {
        "L01": ("CHAP_NHAN", "XE01"),
        "L02": ("CHAP_NHAN", "XE04"),
        "L03": ("CHUYEN_XAC_MINH", ""),
        "L04": ("CHAP_NHAN", "XE02"),
        "L05": ("CHUYEN_XAC_MINH", ""),
        "L06": ("CHAP_NHAN", "XE02"),
        "L07": ("CHAP_NHAN", "XE02"),
        "L08": ("CHAP_NHAN", "XE02"),
        "L09": ("CHAP_NHAN", "XE02"),
        "L10": ("CHUYEN_XAC_MINH", ""),
        "L11": ("CHAP_NHAN", "XE05"),
        "L12": ("CHUYEN_XAC_MINH", ""),
    },
    "ANPR/LPR": {
        "L01": ("CHAP_NHAN", "XE01"),
        "L02": ("CHAP_NHAN", "XE04"),
        "L03": ("CHAP_NHAN", "XE01"),
        "L04": ("CHUYEN_XAC_MINH", ""),
        "L05": ("CHUYEN_XAC_MINH", ""),
        "L06": ("CHAP_NHAN", "XE01"),
        "L07": ("CHAP_NHAN", "XE03"),
        "L08": ("CHAP_NHAN", "XE03"),
        "L09": ("CHAP_NHAN", "XE02"),
        "L10": ("CHAP_NHAN", "XE04"),
        "L11": ("CHUYEN_XAC_MINH", ""),
        "L12": ("CHUYEN_XAC_MINH", ""),
    },
    "Phối hợp": {
        "L01": ("CHAP_NHAN", "XE01"),
        "L02": ("CHAP_NHAN", "XE04"),
        "L03": ("CHUYEN_XAC_MINH", ""),
        "L04": ("CHUYEN_XAC_MINH", ""),
        "L05": ("CHUYEN_XAC_MINH", ""),
        "L06": ("CHUYEN_XAC_MINH", ""),
        "L07": ("CHUYEN_XAC_MINH", ""),
        "L08": ("CHUYEN_XAC_MINH", ""),
        "L09": ("CHAP_NHAN", "XE02"),
        "L10": ("CHUYEN_XAC_MINH", ""),
        "L11": ("CHUYEN_XAC_MINH", ""),
        "L12": ("CHUYEN_XAC_MINH", ""),
    },
}
SO_LUONG_MONG_DOI = {
    "RFID": (5, 3, 4),
    "ANPR/LPR": (5, 3, 4),
    "Phối hợp": (2, 1, 9),
}

COT_BAT_BUOC = {
    "luot_xe": {"ma_luot", "xe_thuc_te"},
    "rfid": {"ma_luot", "trang_thai", "ma_xe_nhan_dien"},
    "anpr": {"ma_luot", "trang_thai", "ma_xe_nhan_dien"},
    "phoi_hop": {"ma_luot", "trang_thai", "ma_xe_nhan_dien"},
}

PHUONG_AN = [
    ("RFID", "rfid"),
    ("ANPR/LPR", "anpr"),
    ("Phối hợp", "phoi_hop"),
]


class LoiDuLieu(ValueError):
    """Loi du lieu dau vao khong hop le."""


# ----------------------------------------------------------------------
# DOC VA KIEM TRA DU LIEU
# ----------------------------------------------------------------------
def tim_thu_muc_du_lieu(chi_dinh: Optional[Path]) -> Path:
    """
    Xac dinh thu muc chua 4 file CSV dau vao.
    - Neu nguoi dung truyen --data-dir thi dung dung thu muc do.
    - Neu khong, thu lan luot: ./data, ./du_lieu, thu muc chua chuong trinh;
      thu muc nao co du ca 4 file thi chon.
    """
    if chi_dinh is not None:
        return chi_dinh

    goc = Path(__file__).resolve().parent
    for ten in ("data", "du_lieu", "."):
        ung_vien = (goc / ten).resolve()
        if all((ung_vien / f).is_file() for f in TEN_FILE.values()):
            return ung_vien

    return goc / "data"


def kiem_tra_du_file(thu_muc: Path) -> None:
    """Bao ro file nao con thieu truoc khi doc."""
    thieu = [f for f in TEN_FILE.values() if not (thu_muc / f).is_file()]
    if thieu:
        raise FileNotFoundError(
            f"Thieu {len(thieu)} file trong thu muc: {thu_muc.resolve()}\n"
            f"Cac file con thieu: {thieu}\n"
            f"Hay copy du 4 file {list(TEN_FILE.values())} vao thu muc tren, "
            f"hoac chay voi --data-dir <thu_muc_chua_file>."
        )


def doc_csv(duong_dan: Path, ten_loai: str) -> pd.DataFrame:
    """Doc CSV dang chuoi, giu ma va gia tri rong; khong tu tao du lieu."""
    if not duong_dan.is_file():
        raise FileNotFoundError(
            f"Khong tim thay file bat buoc: {duong_dan.name}\n"
            f"Vi tri can dat: {duong_dan.resolve()}"
        )

    try:
        df = pd.read_csv(
            duong_dan,
            dtype=str,
            encoding="utf-8-sig",
            keep_default_na=False,
        )
    except Exception as exc:
        raise LoiDuLieu(f"Khong doc duoc {duong_dan}: {exc}") from exc

    df.columns = [str(c).strip() for c in df.columns]
    thieu_cot = COT_BAT_BUOC[ten_loai] - set(df.columns)
    if thieu_cot:
        raise LoiDuLieu(
            f"{duong_dan.name}: thieu cot bat buoc {sorted(thieu_cot)}"
        )

    for cot in df.columns:
        df[cot] = df[cot].map(lambda x: x.strip() if isinstance(x, str) else x)

    if df.empty:
        raise LoiDuLieu(f"{duong_dan.name}: file khong co ban ghi.")

    return df


def kiem_tra_ma_luot(df: pd.DataFrame, ten_file: str) -> None:
    """Chan ma_luot trong va trung truoc khi tao bang tra cuu."""
    ma = df["ma_luot"].astype(str).str.strip()
    trong = ma.eq("")
    if trong.any():
        dong = (df.index[trong] + 2).tolist()
        raise LoiDuLieu(f"{ten_file}: ma_luot trong tai dong CSV {dong}.")

    trung = ma[ma.duplicated(keep=False)].unique().tolist()
    if trung:
        raise LoiDuLieu(f"{ten_file}: ma_luot bi trung {trung}.")


def kiem_tra_bang_ket_qua(df: pd.DataFrame, ten_file: str) -> None:
    kiem_tra_ma_luot(df, ten_file)

    trang_thai = set(df["trang_thai"])
    sai = sorted(trang_thai - TRANG_THAI_HOP_LE)
    if sai:
        raise LoiDuLieu(
            f"{ten_file}: trang_thai khong hop le {sai}; "
            f"chi chap nhan {sorted(TRANG_THAI_HOP_LE)}."
        )

    chap_nhan_thieu_ma = df[
        (df["trang_thai"] == "CHAP_NHAN")
        & (df["ma_xe_nhan_dien"] == "")
    ]
    if not chap_nhan_thieu_ma.empty:
        ds = chap_nhan_thieu_ma["ma_luot"].tolist()
        raise LoiDuLieu(
            f"{ten_file}: CHAP_NHAN nhung ma_xe_nhan_dien trong tai {ds}."
        )


def kiem_tra_va_ghep(
    luot_xe: pd.DataFrame,
    cac_bang: Dict[str, pd.DataFrame],
) -> pd.DataFrame:
    """Kiem tra du/ thua va ghep bang bang ma_luot, khong ghep theo dong."""
    kiem_tra_ma_luot(luot_xe, TEN_FILE["luot_xe"])

    if luot_xe["xe_thuc_te"].eq("").any():
        ds = luot_xe.loc[luot_xe["xe_thuc_te"].eq(""), "ma_luot"].tolist()
        raise LoiDuLieu(f"luot_xe.csv: xe_thuc_te trong tai {ds}.")

    tap_ma_goc = set(luot_xe["ma_luot"])
    for ten, bang in cac_bang.items():
        ten_file = TEN_FILE[ten]
        kiem_tra_bang_ket_qua(bang, ten_file)
        tap_ma_kq = set(bang["ma_luot"])

        thieu = sorted(tap_ma_goc - tap_ma_kq)
        ngoai = sorted(tap_ma_kq - tap_ma_goc)
        if thieu or ngoai:
            chi_tiet = []
            if thieu:
                chi_tiet.append(f"thieu ma_luot {thieu}")
            if ngoai:
                chi_tiet.append(f"co ma_luot ngoai danh sach {ngoai}")
            raise LoiDuLieu(f"{ten_file}: " + "; ".join(chi_tiet) + ".")

    ket_qua = luot_xe[["ma_luot", "xe_thuc_te"]].copy()
    for ten, bang in cac_bang.items():
        cot = bang[["ma_luot", "trang_thai", "ma_xe_nhan_dien"]].rename(
            columns={
                "trang_thai": f"trang_thai_{ten}",
                "ma_xe_nhan_dien": f"ma_xe_{ten}",
            }
        )
        ket_qua = ket_qua.merge(
            cot,
            on="ma_luot",
            how="left",
            validate="one_to_one",
            sort=False,
        )

    return ket_qua


# ----------------------------------------------------------------------
# DANH GIA VA TINH CHI SO
# ----------------------------------------------------------------------
def danh_gia(trang_thai: str, ma_xe_nhan_dien: str, xe_thuc_te: str) -> str:
    """Xe thuc te chi duoc dung o buoc danh gia, khong tham gia nhan dien."""
    if trang_thai == "CHUYEN_XAC_MINH":
        return "CHUYEN_XAC_MINH"
    if ma_xe_nhan_dien == xe_thuc_te:
        return "DUNG_TU_DONG"
    return "CHAP_NHAN_SAI"


def tao_bang_chi_tiet(df: pd.DataFrame) -> pd.DataFrame:
    chi_tiet = df.copy()
    for _, hau_to in PHUONG_AN:
        chi_tiet[f"danh_gia_{hau_to}"] = chi_tiet.apply(
            lambda r, h=hau_to: danh_gia(
                r[f"trang_thai_{h}"],
                r[f"ma_xe_{h}"],
                r["xe_thuc_te"],
            ),
            axis=1,
        )
    return chi_tiet


def tao_bang_so_sanh(chi_tiet: pd.DataFrame) -> pd.DataFrame:
    tong = len(chi_tiet)
    dong = []
    for ten, hau_to in PHUONG_AN:
        cot = f"danh_gia_{hau_to}"
        dung = int((chi_tiet[cot] == "DUNG_TU_DONG").sum())
        sai = int((chi_tiet[cot] == "CHAP_NHAN_SAI").sum())
        xac_minh = int((chi_tiet[cot] == "CHUYEN_XAC_MINH").sum())
        chap_nhan = dung + sai
        dong.append({
            "phuong_an": ten,
            "tong_luot": tong,
            "dung_tu_dong": dung,
            "chap_nhan_sai": sai,
            "chuyen_xac_minh": xac_minh,
            "ty_le_dung_tu_dong_pct": round(dung / tong * 100, 2) if tong else 0,
            "ty_le_chap_nhan_sai_pct": round(sai / tong * 100, 2) if tong else 0,
            "ty_le_chuyen_xac_minh_pct": round(xac_minh / tong * 100, 2) if tong else 0,
            "do_chinh_xac_trong_nhom_tu_dong_pct": (
                round(dung / chap_nhan * 100, 2) if chap_nhan else 0
            ),
        })
    return pd.DataFrame(dong)


# ----------------------------------------------------------------------
# KIEM THU
# ----------------------------------------------------------------------
def kiem_thu_bo_du_lieu_mau(
    chi_tiet: pd.DataFrame,
    bang_so_sanh: pd.DataFrame,
) -> None:
    """
    Kiem thu hoi quy doc lap voi fixture L01-L12.
    Neu dau vao khong phai bo mau da thong nhat, chuong trinh dung
    va yeu cau kiem tra lai thay vi am tham chap nhan mot bo du lieu khac.
    """
    tap_ma = chi_tiet["ma_luot"].tolist()
    if set(tap_ma) != set(MA_LUOT_MAU) or len(tap_ma) != len(MA_LUOT_MAU):
        raise AssertionError(
            "Kiem thu bo mau that bai: tap ma_luot khong khop fixture L01-L12. "
            f"Nhan duoc: {tap_ma}"
        )

    xe_thuc_te = dict(zip(chi_tiet["ma_luot"], chi_tiet["xe_thuc_te"]))
    if xe_thuc_te != XE_THUC_TE_MAU:
        raise AssertionError(
            "Kiem thu bo mau that bai: xe_thuc_te khong khop bo du lieu mau."
        )

    for ten, hau_to in PHUONG_AN:
        cot_trang_thai = f"trang_thai_{hau_to}"
        cot_ma_xe = f"ma_xe_{hau_to}"
        thuc_te = {
            r["ma_luot"]: (r[cot_trang_thai], r[cot_ma_xe])
            for _, r in chi_tiet.iterrows()
        }
        if thuc_te != KET_QUA_MAU[ten]:
            raise AssertionError(
                f"Kiem thu bo mau that bai: ket qua tung luot cua {ten} "
                "khong khop fixture."
            )

    for _, r in bang_so_sanh.iterrows():
        mong_doi = SO_LUONG_MONG_DOI[r["phuong_an"]]
        thuc_te = (
            int(r["dung_tu_dong"]),
            int(r["chap_nhan_sai"]),
            int(r["chuyen_xac_minh"]),
        )
        if thuc_te != mong_doi:
            raise AssertionError(
                f"Kiem thu {r['phuong_an']} that bai: "
                f"mong doi {mong_doi}, nhan duoc {thuc_te}."
            )

    l09 = chi_tiet.loc[chi_tiet["ma_luot"] == "L09"].iloc[0]
    for _, hau_to in PHUONG_AN:
        if l09[f"danh_gia_{hau_to}"] != "CHAP_NHAN_SAI":
            raise AssertionError(f"L09 cua {hau_to} phai la CHAP_NHAN_SAI.")


# ----------------------------------------------------------------------
# BIEU DO
# ----------------------------------------------------------------------
def ve_bieu_do(bang_so_sanh: pd.DataFrame, duong_dan: Path) -> None:
    try:
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise RuntimeError(
            "Chua cai matplotlib. Hay chay: pip install matplotlib"
        ) from exc

    cot = [
        ("dung_tu_dong", "Đúng tự động"),
        ("chap_nhan_sai", "Chấp nhận sai"),
        ("chuyen_xac_minh", "Chuyển xác minh"),
    ]
    fig, ax = plt.subplots(figsize=(10, 6))
    du_lieu = list(range(len(bang_so_sanh)))
    day = 0.23
    for i, (ten_cot, nhan) in enumerate(cot):
        gia_tri = bang_so_sanh[ten_cot].tolist()
        vi_tri = [x + (i - 1) * day for x in du_lieu]
        bars = ax.bar(vi_tri, gia_tri, width=day, label=nhan)
        ax.bar_label(bars, padding=3, fontsize=9)

    ax.set_title("So sánh kết quả nhận diện ETC theo 12 lượt xe")
    ax.set_ylabel("Số lượt")
    ax.set_xticks(du_lieu)
    ax.set_xticklabels(bang_so_sanh["phuong_an"].tolist())
    ax.set_ylim(0, max(10, int(bang_so_sanh[
        ["dung_tu_dong", "chap_nhan_sai", "chuyen_xac_minh"]
    ].to_numpy().max()) + 2))
    ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.35)
    fig.tight_layout()
    duong_dan.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(duong_dan, dpi=180, bbox_inches="tight")
    plt.close(fig)


# ----------------------------------------------------------------------
# IN KET QUA RA MAN HINH
# ----------------------------------------------------------------------
def pct(x: float) -> str:
    """41.67 -> '41,67%'."""
    return f"{x:.2f}".replace(".", ",") + "%"


def in_bang(
    tieu_de: str,
    ten_cot: List[str],
    cac_dong: List[List[str]],
    can_le: Optional[List[str]] = None,
) -> None:
    """In bang co khung, tu dong can do rong cot. can_le: '<', '^' hoac '>'."""
    n = len(ten_cot)
    can_le = can_le or ["^"] * n
    rong = [
        max(len(str(x)) for x in [ten_cot[i]] + [d[i] for d in cac_dong])
        for i in range(n)
    ]

    def ke(trai: str, giua: str, phai: str) -> str:
        return trai + giua.join("─" * (w + 2) for w in rong) + phai

    def hang(o: List[str], can: List[str]) -> str:
        return "│" + "│".join(
            " " + format(str(o[i]), f"{can[i]}{rong[i]}") + " " for i in range(n)
        ) + "│"

    print(f"\n▌ {tieu_de}")
    print(ke("┌", "┬", "┐"))
    print(hang(ten_cot, ["^"] * n))
    print(ke("├", "┼", "┤"))
    for d in cac_dong:
        print(hang(d, can_le))
    print(ke("└", "┴", "┘"))


def o_chi_tiet(danh_gia_luot: str, ma_xe: str) -> str:
    if danh_gia_luot == "DUNG_TU_DONG":
        return f"✔ {ma_xe}"
    if danh_gia_luot == "CHAP_NHAN_SAI":
        return f"✘ {ma_xe}"
    return "? Xác minh"


def in_ket_qua(
    so_sanh: pd.DataFrame,
    chi_tiet: pd.DataFrame,
    cac_file: List[Path],
    thu_muc_du_lieu: Path,
) -> None:
    rong_khung = 72
    print("\n" + "═" * rong_khung)
    print("TỔNG HỢP KẾT QUẢ NHẬN DIỆN ETC (MỤC 6.5)".center(rong_khung))
    print("═" * rong_khung)
    print(f"Dữ liệu đầu vào : {thu_muc_du_lieu}")
    print(f"Số lượt xe      : {len(chi_tiet)}")
    print("Kiểm thử mẫu    : ✔ THÀNH CÔNG (khớp bộ mẫu L01-L12)")

    # --- Bang 1: so sanh 3 phuong an ---
    dong = []
    for _, r in so_sanh.iterrows():
        chap_nhan = int(r["dung_tu_dong"]) + int(r["chap_nhan_sai"])
        dong.append([
            r["phuong_an"],
            f'{int(r["dung_tu_dong"])}  ({pct(r["ty_le_dung_tu_dong_pct"])})',
            f'{int(r["chap_nhan_sai"])}  ({pct(r["ty_le_chap_nhan_sai_pct"])})',
            f'{int(r["chuyen_xac_minh"])}  ({pct(r["ty_le_chuyen_xac_minh_pct"])})',
            f'{int(r["dung_tu_dong"])}/{chap_nhan}  '
            f'({pct(r["do_chinh_xac_trong_nhom_tu_dong_pct"])})',
        ])
    in_bang(
        f"BẢNG 1 - SO SÁNH 3 PHƯƠNG ÁN (tỷ lệ tính trên {len(chi_tiet)} lượt)",
        ["Phương án", "Đúng tự động", "Chấp nhận sai",
         "Chuyển xác minh", "Chính xác trong nhóm tự động*"],
        dong,
        ["<", "^", "^", "^", "^"],
    )
    print("* Mẫu số riêng = số lượt CHAP_NHAN (đúng + sai), "
          "khác với tỷ lệ trên tổng số lượt.")

    # --- Nhan xet nhanh tinh tu du lieu ---
    it_sai_nhat = so_sanh.loc[so_sanh["chap_nhan_sai"].idxmin(), "phuong_an"]
    nhieu_xm_nhat = so_sanh.loc[so_sanh["chuyen_xac_minh"].idxmax(), "phuong_an"]
    print(f"→ Ít chấp nhận sai nhất : {it_sai_nhat}")
    print(f"→ Chuyển xác minh nhiều nhất : {nhieu_xm_nhat}")

    # --- Bang 2: chi tiet tung luot ---
    dong_ct = []
    for _, r in chi_tiet.iterrows():
        dong_ct.append([
            r["ma_luot"],
            r["xe_thuc_te"],
            o_chi_tiet(r["danh_gia_rfid"], r["ma_xe_rfid"]),
            o_chi_tiet(r["danh_gia_anpr"], r["ma_xe_anpr"]),
            o_chi_tiet(r["danh_gia_phoi_hop"], r["ma_xe_phoi_hop"]),
        ])
    in_bang(
        "BẢNG 2 - CHI TIẾT TỪNG LƯỢT",
        ["Lượt", "Xe thực tế", "RFID", "ANPR/LPR", "Phối hợp"],
        dong_ct,
        ["^", "^", "<", "<", "<"],
    )
    print("Chú thích: ✔ đúng tự động | ✘ chấp nhận sai | ? chuyển xác minh")
    print("(mã xe sau ký hiệu là xe mà phương án nhận diện được)")

    # --- File dau ra ---
    print("\n▌ CÁC FILE ĐÃ TẠO")
    for f in cac_file:
        print(f"  ✔ {f.name:<28} → {f.resolve()}")
    print("═" * rong_khung)


# ----------------------------------------------------------------------
# CHUONG TRINH CHINH
# ----------------------------------------------------------------------
def main() -> int:
    # Dam bao in duoc tieng Viet va ky tu ve khung tren console Windows.
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

    parser = argparse.ArgumentParser(
        description="TV5 - Tong hop ket qua RFID, ANPR/LPR va phoi hop."
    )
    parser.add_argument(
        "--data-dir", type=Path, default=None,
        help="Thu muc chua 4 file CSV dau vao "
             "(mac dinh: tu dong tim trong ./data, ./du_lieu hoac thu muc chuong trinh).",
    )
    parser.add_argument(
        "--output-dir", type=Path, default=Path(__file__).resolve().parent,
        help="Thu muc ghi CSV va bieu do dau ra (mac dinh: thu muc chuong trinh).",
    )
    args = parser.parse_args()

    try:
        thu_muc_du_lieu = tim_thu_muc_du_lieu(args.data_dir)
        kiem_tra_du_file(thu_muc_du_lieu)

        # 1. Doc du lieu tu cac thanh vien. Khong tu tao du lieu thay the.
        luot_xe = doc_csv(thu_muc_du_lieu / TEN_FILE["luot_xe"], "luot_xe")
        rfid = doc_csv(thu_muc_du_lieu / TEN_FILE["rfid"], "rfid")
        anpr = doc_csv(thu_muc_du_lieu / TEN_FILE["anpr"], "anpr")
        phoi_hop = doc_csv(thu_muc_du_lieu / TEN_FILE["phoi_hop"], "phoi_hop")

        # 2. Kiem tra du lieu va ghep theo ma_luot.
        da_ghep = kiem_tra_va_ghep(
            luot_xe,
            {"rfid": rfid, "anpr": anpr, "phoi_hop": phoi_hop},
        )

        # 3. Danh gia sau nhan dien va tinh chi so.
        chi_tiet = tao_bang_chi_tiet(da_ghep)
        so_sanh = tao_bang_so_sanh(chi_tiet)

        # 4. Kiem thu bat buoc truoc khi tao bat ky san pham dau ra nao.
        kiem_thu_bo_du_lieu_mau(chi_tiet, so_sanh)

        # 5. Chi xuat bao cao sau khi tat ca kiem tra da dat.
        args.output_dir.mkdir(parents=True, exist_ok=True)
        file_so_sanh = args.output_dir / "ket_qua_6_5_so_sanh.csv"
        file_chi_tiet = args.output_dir / "ket_qua_6_5_chi_tiet.csv"
        file_bieu_do = args.output_dir / "bieu_do_6_5.png"

        so_sanh.to_csv(file_so_sanh, index=False, encoding="utf-8-sig")
        chi_tiet.to_csv(file_chi_tiet, index=False, encoding="utf-8-sig")
        ve_bieu_do(so_sanh, file_bieu_do)

        # 6. In ket qua ra man hinh.
        in_ket_qua(
            so_sanh,
            chi_tiet,
            [file_so_sanh, file_chi_tiet, file_bieu_do],
            thu_muc_du_lieu,
        )
        return 0

    except (FileNotFoundError, LoiDuLieu, AssertionError, RuntimeError) as loi:
        print(f"\nLOI - DUNG CHUONG TRINH: {loi}", file=sys.stderr)
        print("Khong xuat CSV hoac bieu do vi du lieu/kiem thu chua dat.", file=sys.stderr)
        return 1
    except Exception as loi:
        print(f"\nLOI KHONG DU KIEN: {loi}", file=sys.stderr)
        print("Khong xuat bao cao.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())