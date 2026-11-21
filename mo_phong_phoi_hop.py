import argparse
import csv
from pathlib import Path


THU_MUC = Path(__file__).resolve().parent


def doc_csv(duong_dan, cot_bat_buoc):
    with open(duong_dan, encoding="utf-8-sig", newline="") as tep:
        reader = csv.DictReader(tep)
        if not cot_bat_buoc.issubset(reader.fieldnames or []):
            raise ValueError(f"{duong_dan}: thieu cot {sorted(cot_bat_buoc)}")
        bang = {}
        for dong in reader:
            if None in dong or any(v is None for v in dong.values()):
                raise ValueError(f"{duong_dan}: dong CSV sai so cot")
            dong = {k: v.strip() for k, v in dong.items()}
            ma = dong["ma_luot"]
            if not ma or ma in bang:
                raise ValueError(f"{duong_dan}: ma_luot trong hoac trung: {ma}")
            bang[ma] = dong
        return bang


def doc_ket_qua(duong_dan):
    bang = doc_csv(duong_dan, {"ma_luot", "ma_xe_nhan_dien", "trang_thai"})
    for ma, dong in bang.items():
        if dong["trang_thai"] not in {"CHAP_NHAN", "CHUYEN_XAC_MINH"}:
            raise ValueError(f"{duong_dan}: trang thai khong hop le tai {ma}")
        if dong["trang_thai"] == "CHAP_NHAN" and not dong["ma_xe_nhan_dien"]:
            raise ValueError(f"{duong_dan}: chap nhan nhung thieu ma xe tai {ma}")
    return bang


def doi_chieu_hai_nguon(danh_sach_luot, bang_rfid, bang_anpr):
    ket_qua = []
    for ma in danh_sach_luot:
        rfid = bang_rfid.get(ma)
        anpr = bang_anpr.get(ma)
        xe_rfid = rfid["ma_xe_nhan_dien"] if rfid else ""
        xe_anpr = anpr["ma_xe_nhan_dien"] if anpr else ""
        rfid_ok = bool(rfid and rfid["trang_thai"] == "CHAP_NHAN" and xe_rfid)
        anpr_ok = bool(anpr and anpr["trang_thai"] == "CHAP_NHAN" and xe_anpr)
        chap_nhan = False
        if rfid is None and anpr is None:
            ly_do = "THIEU_CA_HAI_KET_QUA"
        elif rfid is None:
            ly_do = "THIEU_KET_QUA_RFID"
        elif anpr is None:
            ly_do = "THIEU_KET_QUA_ANPR"
        elif not rfid_ok and not anpr_ok:
            ly_do = "CA_HAI_KHONG_NHAN_DIEN_DUOC"
        elif not rfid_ok:
            ly_do = "RFID_KHONG_NHAN_DIEN_DUOC"
        elif not anpr_ok:
            ly_do = "ANPR_KHONG_NHAN_DIEN_DUOC"
        elif xe_rfid != xe_anpr:
            ly_do = "HAI_NGUON_KHONG_KHOP"
        else:
            chap_nhan = True
            ly_do = "HAI_NGUON_KHOP"
        ket_qua.append({
            "ma_luot": ma,
            "ma_xe_rfid": xe_rfid,
            "ma_xe_anpr": xe_anpr,
            "trang_thai": "CHAP_NHAN" if chap_nhan else "CHUYEN_XAC_MINH",
            "ma_xe_nhan_dien": xe_rfid if chap_nhan else "",
            "ly_do": ly_do,
        })
    return ket_qua


def chay_mo_phong(file_luot, file_rfid, file_anpr):
    danh_sach_luot = doc_csv(file_luot, {"ma_luot"})
    if not danh_sach_luot:
        raise ValueError("Danh sach luot xe rong")
    bang_rfid = doc_ket_qua(file_rfid)
    bang_anpr = doc_ket_qua(file_anpr)
    for ten, bang in [("RFID", bang_rfid), ("ANPR", bang_anpr)]:
        ma_ngoai = set(bang) - set(danh_sach_luot)
        if ma_ngoai:
            raise ValueError(f"{ten}: ma_luot ngoai danh sach: {sorted(ma_ngoai)}")
    return doi_chieu_hai_nguon(danh_sach_luot, bang_rfid, bang_anpr)


def main():
    parser = argparse.ArgumentParser(description="Mo phong phoi hop RFID va ANPR")
    parser.add_argument("--luot-xe", type=Path, default=THU_MUC / "luot_xe.csv")
    parser.add_argument("--rfid", type=Path, default=THU_MUC / "ket_qua_rfid.csv")
    parser.add_argument("--anpr", type=Path, default=THU_MUC / "ket_qua_anpr.csv")
    parser.add_argument("--output", type=Path, default=THU_MUC / "ket_qua_phoi_hop.csv")
    args = parser.parse_args()
    try:
        ket_qua = chay_mo_phong(args.luot_xe, args.rfid, args.anpr)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, "w", encoding="utf-8-sig", newline="") as tep:
            writer = csv.DictWriter(tep, fieldnames=list(ket_qua[0]))
            writer.writeheader()
            writer.writerows(ket_qua)
    except (OSError, ValueError) as loi:
        parser.exit(1, f"Loi: {loi}\n")
    for dong in ket_qua:
        print(dong["ma_luot"], dong["trang_thai"], dong["ma_xe_nhan_dien"] or "-", dong["ly_do"])
    so_chap_nhan = sum(d["trang_thai"] == "CHAP_NHAN" for d in ket_qua)
    print(f"Tong: {len(ket_qua)}; chap nhan: {so_chap_nhan}; chuyen xac minh: {len(ket_qua) - so_chap_nhan}")
    print(f"Da luu: {args.output}")


if __name__ == "__main__":
    main()
