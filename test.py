# =====================================================================
# MỤC 6.5 - TỔNG HỢP VÀ ĐÁNH GIÁ KẾT QUẢ BA PHƯƠNG ÁN
#   PA1: chỉ RFID (6.2)   PA2: chỉ biển số / ANPR giả lập (6.3)
#   PA3: phối hợp hai nguồn theo ma_luot (6.4)
# Đầu vào : xe_dang_ky.csv, luot_xe.csv (bộ dữ liệu chung 6.1 của TV2)
# Đầu ra  : ket_qua_6_5_so_sanh.csv, ket_qua_6_5_chi_tiet.csv, bieu_do_6_5.png
# Nguyên tắc: xe_thuc_te CHỈ dùng để chấm điểm ở bước 6.5,
#             KHÔNG tham gia quyết định nhận diện của PA1, PA2, PA3.
# =====================================================================
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# ====== 1. CẤU HÌNH ======
try:
    THU_MUC = Path(__file__).resolve().parent
except NameError:                       # chạy trong notebook / trình chạy không có __file__
    THU_MUC = Path.cwd()

FILE_DANG_KY = THU_MUC / "xe_dang_ky.csv"
FILE_LUOT_XE = THU_MUC / "luot_xe.csv"
FILE_RA_BANG = THU_MUC / "ket_qua_6_5_so_sanh.csv"
FILE_RA_CHI_TIET = THU_MUC / "ket_qua_6_5_chi_tiet.csv"
FILE_RA_HINH = THU_MUC / "bieu_do_6_5.png"

# Kết quả của các thành viên khác (nếu có thì đối chiếu chéo, không có thì bỏ qua)
FILE_THANH_VIEN = {
    "RFID": THU_MUC / "ket_qua_rfid.csv",
    "ANPR": THU_MUC / "ket_qua_anpr.csv",
    "KET_HOP": THU_MUC / "ket_qua_6_4.csv",
}
TU_TAO_DU_LIEU_MAU = True      # True: nếu thiếu 2 file đầu vào thì tạo bộ dữ liệu 6.1 để chạy thử

CHAP_NHAN = "CHAP_NHAN"
CHUYEN_XM = "CHUYEN_XAC_MINH"
DUNG_TU_DONG = "DUNG_TU_DONG"
CHAP_NHAN_SAI = "CHAP_NHAN_SAI"

TEN_PA = {
    "RFID": "PA1 - RFID",
    "ANPR": "PA2 - Biển số (ANPR)",
    "KET_HOP": "PA3 - Kết hợp hai nguồn",
}

DU_LIEU_MAU_DANG_KY = """ma_xe,ma_the,bien_so
XE01,TAG001,51A-10001
XE02,TAG002,51A-10002
XE03,TAG003,51A-10003
XE04,TAG004,51A-10004
XE05,TAG005,51A-10005
XE06,TAG006,51A-10006
"""
DU_LIEU_MAU_LUOT = """ma_luot,kich_ban,xe_thuc_te,rfid_nhan_duoc,bien_so_nhan_duoc
L01,hai_nguon_dung,XE01,TAG001,51A-10001
L02,hai_nguon_dung,XE04,TAG004,51A-10004
L03,thieu_rfid,XE01,,51A-10001
L04,thieu_bien_so,XE02,TAG002,
L05,thieu_ca_hai,XE03,,
L06,rfid_sai_bien_so_dung,XE01,TAG002,51A-10001
L07,rfid_dung_bien_so_sai,XE02,TAG002,51A-10003
L08,hai_nguon_sai_khong_khop,XE01,TAG002,51A-10003
L09,hai_nguon_cung_khop_sai,XE01,TAG002,51A-10002
L10,the_chua_dang_ky,XE04,TAG999,51A-10004
L11,bien_so_chua_dang_ky,XE05,TAG005,99Z-99999
L12,ca_hai_chua_dang_ky,XE06,TAG999,99Z-99999
"""

# ====== 2. ĐỌC VÀ KIỂM TRA DỮ LIỆU ======
def chuan_hoa(s):
    """Viết hoa, bỏ khoảng trắng, dấu '-', '.', ... để so khớp ổn định."""
    return "".join(ch for ch in str(s).upper() if ch.isalnum())

def doc_csv(duong_dan, cot_bat_buoc):
    if not duong_dan.exists():
        raise FileNotFoundError(f"Không thấy file: {duong_dan}")
    df = pd.read_csv(duong_dan, dtype=str, keep_default_na=False, encoding="utf-8-sig")
    df.columns = [c.strip() for c in df.columns]
    thieu = [c for c in cot_bat_buoc if c not in df.columns]
    if thieu:
        raise ValueError(f"{duong_dan.name} thiếu cột bắt buộc: {thieu}")
    for c in df.columns:
        df[c] = df[c].str.strip()
    return df

def lap_bang_tra(dang_ky, cot_khoa):
    """Lập bảng tra {mã thẻ | biển số đã chuẩn hóa} -> mã xe; báo lỗi nếu dữ liệu đăng ký mâu thuẫn."""
    bang = {}
    for khoa, xe in zip(dang_ky[cot_khoa], dang_ky["ma_xe"]):
        k = chuan_hoa(khoa)
        if not k:
            raise ValueError(f"xe_dang_ky.csv: cột {cot_khoa} rỗng ở xe {xe}")
        if k in bang and bang[k] != xe:
            raise ValueError(f"xe_dang_ky.csv: {cot_khoa} '{khoa}' gán cho hai xe {bang[k]} và {xe}")
        bang[k] = xe
    return bang

def kiem_tra_luot(luot):
    if (luot["ma_luot"] == "").any():
        raise ValueError("luot_xe.csv có ma_luot rỗng")
    trung = luot.loc[luot["ma_luot"].duplicated(), "ma_luot"].tolist()
    if trung:
        raise ValueError(f"luot_xe.csv có ma_luot trùng: {trung}")

if TU_TAO_DU_LIEU_MAU:
    if not FILE_DANG_KY.exists():
        FILE_DANG_KY.write_text(DU_LIEU_MAU_DANG_KY, encoding="utf-8")
    if not FILE_LUOT_XE.exists():
        FILE_LUOT_XE.write_text(DU_LIEU_MAU_LUOT, encoding="utf-8")

dang_ky = doc_csv(FILE_DANG_KY, ["ma_xe", "ma_the", "bien_so"])
luot = doc_csv(FILE_LUOT_XE, ["ma_luot", "xe_thuc_te", "rfid_nhan_duoc", "bien_so_nhan_duoc"])
kiem_tra_luot(luot)

tra_the = lap_bang_tra(dang_ky, "ma_the")      # 6.2: mã thẻ  -> mã xe
tra_bien = lap_bang_tra(dang_ky, "bien_so")    # 6.3: biển số -> mã xe

# ====== 3. BA PHƯƠNG ÁN (KHÔNG DÙNG xe_thuc_te) ======
def tra_cuu(gia_tri, bang_tra):
    """6.2 / 6.3: tìm thấy -> (CHAP_NHAN, mã xe); rỗng hoặc không tìm thấy -> chuyển xác minh."""
    khoa = chuan_hoa(gia_tri)
    if not khoa:
        return CHUYEN_XM, ""
    xe = bang_tra.get(khoa)
    return (CHAP_NHAN, xe) if xe is not None else (CHUYEN_XM, "")

def phoi_hop(kq_rfid, kq_anpr):
    """6.4: cả hai nguồn thành công và cùng một mã xe -> chấp nhận; còn lại -> chuyển xác minh.
    So mã xe với mã xe, không so mã thẻ với biển số. Hai nguồn cùng sai (L09) vẫn được chấp nhận."""
    (tt1, xe1), (tt2, xe2) = kq_rfid, kq_anpr
    if tt1 == CHAP_NHAN and tt2 == CHAP_NHAN and xe1 == xe2:
        return CHAP_NHAN, xe1
    return CHUYEN_XM, ""

def danh_gia_6_5(trang_thai, ma_xe, xe_thuc_te):
    """6.5: chỉ ở bước này mới đối chiếu với xe_thuc_te."""
    if trang_thai != CHAP_NHAN:
        return CHUYEN_XM
    return DUNG_TU_DONG if ma_xe == xe_thuc_te else CHAP_NHAN_SAI

dong = []
for _, r in luot.iterrows():
    rfid = tra_cuu(r["rfid_nhan_duoc"], tra_the)
    anpr = tra_cuu(r["bien_so_nhan_duoc"], tra_bien)
    ket_qua = {"RFID": rfid, "ANPR": anpr, "KET_HOP": phoi_hop(rfid, anpr)}

    hang = {"ma_luot": r["ma_luot"]}
    if "kich_ban" in luot.columns:
        hang["kich_ban"] = r["kich_ban"]
    hang["xe_thuc_te"] = r["xe_thuc_te"]
    hang["rfid_nhan_duoc"] = r["rfid_nhan_duoc"]
    hang["bien_so_nhan_duoc"] = r["bien_so_nhan_duoc"]
    for ma_pa, (tt, xe) in ket_qua.items():
        hang[f"{ma_pa}_trang_thai"] = tt
        hang[f"{ma_pa}_ma_xe_ket_qua"] = xe
        hang[f"{ma_pa}_danh_gia"] = danh_gia_6_5(tt, xe, r["xe_thuc_te"])
    dong.append(hang)

chi_tiet = pd.DataFrame(dong)

# ====== 4. TỔNG HỢP TỶ LỆ ======
tong_hop = []
n = len(chi_tiet)
for ma_pa, ten in TEN_PA.items():
    dg = chi_tiet[f"{ma_pa}_danh_gia"]
    dung = int((dg == DUNG_TU_DONG).sum())
    sai = int((dg == CHAP_NHAN_SAI).sum())
    xm = int((dg == CHUYEN_XM).sum())
    tong_hop.append({
        "Phương án": ten,
        "Tổng lượt": n,
        "Đúng tự động": dung,
        "Chấp nhận sai": sai,
        "Chuyển xác minh": xm,
        "Tỷ lệ đúng tự động (%)": round(dung / n * 100, 2),
        "Tỷ lệ chấp nhận sai (%)": round(sai / n * 100, 2),
        "Tỷ lệ chuyển xác minh (%)": round(xm / n * 100, 2),
        "Tỷ lệ tự động chấp nhận (%)": round((dung + sai) / n * 100, 2),
        "Độ chính xác trong nhóm tự động (%)": round(dung / (dung + sai) * 100, 2) if (dung + sai) else 0.0,
    })
bang = pd.DataFrame(tong_hop)

# ====== 5. KIỂM THỬ THEO TỪNG LƯỢT (chỉ chạy khi đúng bộ dữ liệu 6.1: L01-L12) ======
# Thứ tự: (RFID, ANPR, KẾT HỢP); chuỗi rỗng = chuyển xác minh
KY_VONG_XE = {
    "L01": ("XE01", "XE01", "XE01"), "L02": ("XE04", "XE04", "XE04"),
    "L03": ("",     "XE01", ""),     "L04": ("XE02", "",     ""),
    "L05": ("",     "",     ""),     "L06": ("XE02", "XE01", ""),
    "L07": ("XE02", "XE03", ""),     "L08": ("XE02", "XE03", ""),
    "L09": ("XE02", "XE02", "XE02"), "L10": ("",     "XE04", ""),
    "L11": ("XE05", "",     ""),     "L12": ("",     "",     ""),
}
KY_VONG_SO_LUONG = {   # (đúng tự động, chấp nhận sai, chuyển xác minh)
    "RFID": (5, 3, 4), "ANPR": (5, 3, 4), "KET_HOP": (2, 1, 9),
}

def kiem_thu():
    if set(chi_tiet["ma_luot"]) != set(KY_VONG_XE):
        print("Bỏ qua kiểm thử tự động: dữ liệu không phải bộ 6.1 (L01-L12).")
        return
    loi = []
    for _, r in chi_tiet.iterrows():
        for i, ma_pa in enumerate(["RFID", "ANPR", "KET_HOP"]):
            xe_kv = KY_VONG_XE[r["ma_luot"]][i]
            tt_kv = CHAP_NHAN if xe_kv else CHUYEN_XM
            if r[f"{ma_pa}_ma_xe_ket_qua"] != xe_kv or r[f"{ma_pa}_trang_thai"] != tt_kv:
                loi.append(f"{r['ma_luot']} {ma_pa}: kỳ vọng ({tt_kv}, '{xe_kv}'), "
                           f"thực tế ({r[f'{ma_pa}_trang_thai']}, '{r[f'{ma_pa}_ma_xe_ket_qua']}')")
    for ma_pa, kv in KY_VONG_SO_LUONG.items():
        dg = chi_tiet[f"{ma_pa}_danh_gia"]
        tt = (int((dg == DUNG_TU_DONG).sum()), int((dg == CHAP_NHAN_SAI).sum()), int((dg == CHUYEN_XM).sum()))
        if tt != kv:
            loi.append(f"{ma_pa}: số lượng (đúng, sai, xác minh) kỳ vọng {kv}, thực tế {tt}")
    print("=== KIỂM THỬ TỪNG LƯỢT: " + ("ĐẠT (36/36 kết quả khớp, 3/3 bộ đếm khớp)" if not loi else "CÓ LỖI") + " ===")
    for m in loi:
        print("  SAI:", m)

# ====== 6. ĐỐI CHIẾU CHÉO VỚI FILE CỦA TV1 / TV3 / TV4 (nếu có) ======
TT_THANH_CONG = {"CHAP_NHAN", "THANH_CONG", "SUCCESS", "OK", "KHOP"}
COT_MA_XE = ["ma_xe_ket_qua", "ma_xe_nhan_dien", "ma_xe"]

def doi_chieu_cheo():
    for ma_pa, duong_dan in FILE_THANH_VIEN.items():
        if not duong_dan.exists():
            continue
        try:
            df = doc_csv(duong_dan, ["ma_luot", "trang_thai"])
            cot_xe = next((c for c in COT_MA_XE if c in df.columns), None)
            if cot_xe is None:
                print(f"[Đối chiếu] {duong_dan.name}: không có cột mã xe trong {COT_MA_XE}")
                continue
            ngoai = {}
            for _, r in df.iterrows():
                ok = r["trang_thai"].upper() in TT_THANH_CONG
                ngoai[r["ma_luot"]] = r[cot_xe] if ok else ""
            lech = []
            for _, r in chi_tiet.iterrows():
                kq_nguoi_khac = ngoai.get(r["ma_luot"], "<thiếu lượt>")
                if kq_nguoi_khac != r[f"{ma_pa}_ma_xe_ket_qua"]:
                    lech.append(f"{r['ma_luot']}: file '{kq_nguoi_khac}' / code này '{r[f'{ma_pa}_ma_xe_ket_qua']}'")
            print(f"[Đối chiếu] {duong_dan.name}: " + ("KHỚP hoàn toàn" if not lech else f"LỆCH {len(lech)} lượt"))
            for m in lech:
                print("   ", m)
        except Exception as loi:
            print(f"[Đối chiếu] {duong_dan.name}: không đọc được ({loi})")

# ====== 7. XUẤT BẢNG VÀ IN KẾT QUẢ ======
bang.to_csv(FILE_RA_BANG, index=False, encoding="utf-8-sig")
chi_tiet.to_csv(FILE_RA_CHI_TIET, index=False, encoding="utf-8-sig")

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", None)
print("=== BẢNG SO SÁNH BA PHƯƠNG ÁN (6.5) ===")
print(bang.to_string(index=False))
print()
cot_dg = ["ma_luot", "xe_thuc_te"] + [f"{m}_danh_gia" for m in TEN_PA]
print("=== ĐÁNH GIÁ TỪNG LƯỢT ===")
print(chi_tiet[cot_dg].to_string(index=False))
print()
kiem_thu()
doi_chieu_cheo()

print()
print("=== NHẬN XÉT TỰ ĐỘNG ===")
for cot_so, mo_ta, ham in [
    ("Tỷ lệ chấp nhận sai (%)", "chấp nhận sai THẤP nhất", min),
    ("Tỷ lệ đúng tự động (%)", "đúng tự động CAO nhất", max),
    ("Tỷ lệ chuyển xác minh (%)", "chuyển xác minh THẤP nhất (ít tốn công người nhất)", min),
]:
    gia_tri = ham(bang[cot_so])
    ten_tot = bang.loc[bang[cot_so] == gia_tri, "Phương án"].tolist()
    print(f"- {mo_ta}: {' / '.join(ten_tot)} ({gia_tri}%)")
sai_ca_ba = chi_tiet.loc[
    (chi_tiet["RFID_danh_gia"] == CHAP_NHAN_SAI)
    & (chi_tiet["ANPR_danh_gia"] == CHAP_NHAN_SAI)
    & (chi_tiet["KET_HOP_danh_gia"] == CHAP_NHAN_SAI), "ma_luot"].tolist()
print(f"- Lượt cả ba phương án đều chấp nhận sai: {sai_ca_ba if sai_ca_ba else 'không có'}")
print("- Lưu ý: tỷ lệ chỉ áp dụng cho bộ dữ liệu giả lập, không phản ánh độ chính xác thực tế của thiết bị ETC.")

# ====== 8. VẼ BIỂU ĐỒ ======
cot_ty_le = ["Tỷ lệ đúng tự động (%)", "Tỷ lệ chấp nhận sai (%)", "Tỷ lệ chuyển xác minh (%)"]
nhan = ["Đúng tự động", "Chấp nhận sai", "Chuyển xác minh"]
mau = ["#2e7d32", "#c62828", "#f9a825"]
ten_truc_x = [t.replace(" - ", "\n") for t in bang["Phương án"]]

fig, ax = plt.subplots(1, 2, figsize=(14, 6))

# 8a. Cột nhóm: so sánh từng tỷ lệ giữa ba phương án
rong = 0.26
for k, (ten_cot, ten_nhan, mau_cot) in enumerate(zip(cot_ty_le, nhan, mau)):
    vi_tri = [i + (k - 1) * rong for i in range(len(bang))]
    thanh = ax[0].bar(vi_tri, bang[ten_cot], rong, color=mau_cot, label=ten_nhan)
    for cot_bar, gia_tri in zip(thanh, bang[ten_cot]):
        ax[0].text(cot_bar.get_x() + cot_bar.get_width() / 2, gia_tri + 1,
                   f"{gia_tri:.1f}", ha="center", fontsize=9)
ax[0].set_xticks(range(len(bang)))
ax[0].set_xticklabels(ten_truc_x, fontsize=9)
ax[0].set_ylabel("Tỷ lệ (%)")
ax[0].set_ylim(0, 100)
ax[0].set_title("So sánh các tỷ lệ giữa ba phương án")
ax[0].legend()

# 8b. Cột chồng: cơ cấu kết quả của từng phương án
duoi = [0] * len(bang)
for ten_cot, ten_nhan, mau_cot in zip(cot_ty_le, nhan, mau):
    ax[1].bar(ten_truc_x, bang[ten_cot], bottom=duoi, color=mau_cot, label=ten_nhan)
    for i, gia_tri in enumerate(bang[ten_cot]):
        if gia_tri > 4:
            ax[1].text(i, duoi[i] + gia_tri / 2, f"{gia_tri:.1f}%", ha="center",
                       va="center", color="white", fontsize=9)
    duoi = [d + g for d, g in zip(duoi, bang[ten_cot])]
ax[1].set_ylabel("Tỷ lệ (%)")
ax[1].set_ylim(0, 100)
ax[1].set_title("Cơ cấu kết quả theo phương án")
ax[1].tick_params(axis="x", labelsize=9)
ax[1].legend(loc="upper center", bbox_to_anchor=(0.5, -0.14), ncol=3, fontsize=8)

fig.suptitle(f"Mục 6.5 - So sánh ba phương án trên {n} lượt xe giả lập", fontsize=13)
fig.text(0.5, 0.005, "Tỷ lệ chỉ áp dụng cho bộ dữ liệu giả lập, không phản ánh độ chính xác thực tế của thiết bị ETC.",
         ha="center", fontsize=8, style="italic")
plt.tight_layout(rect=(0, 0.02, 1, 0.96))
plt.savefig(FILE_RA_HINH, dpi=150)
print(f"\nĐã xuất: {FILE_RA_BANG.name}, {FILE_RA_CHI_TIET.name}, {FILE_RA_HINH.name}")
plt.show()