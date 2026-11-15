import csv

def doc_danh_sach_xe(file_path):
    """Đọc dữ liệu phương tiện đăng ký, tạo từ điển ánh xạ bien_so -> ma_xe"""
    tu_dien_bien_so = {}
    with open(file_path, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            bien_so = row['bien_so'].strip()
            ma_xe = row['ma_xe'].strip()
            tu_dien_bien_so[bien_so] = ma_xe
    return tu_dien_bien_so

def xu_ly_anpr(bien_so_nhan_duoc, tu_dien_bien_so):
    """Quy tắc xử lý nhận diện của phương án ANPR/LPR thuần túy"""
    bien_so_clean = bien_so_nhan_duoc.strip()
    
    # Trường hợp 1: Không đọc được biển số (dữ liệu rỗng)
    if not bien_so_clean:
        return "Chuyển xác minh", "", "Không đọc được biển số từ hình ảnh"
    
    # Trường hợp 2: Có chuỗi biển số, tiến hành tra cứu trong dữ liệu đăng ký
    if bien_so_clean in tu_dien_bien_so:
        ma_xe_tim_thay = tu_dien_bien_so[bien_so_clean]
        return "Chấp nhận tự động", ma_xe_tim_thay, "Tìm thấy biển số trong danh sách đăng ký"
    else:
        return "Chuyển xác minh", "", "Biển số chưa đăng ký trong hệ thống"

def danh_gia_ket_qua(trang_thai, ma_xe_du_doan, xe_thuc_te):
    """Phân nhóm kết quả dựa trên đối chiếu với xe thực tế"""
    if trang_thai == "Chuyển xác minh":
        return "Chuyển xác minh"
    if ma_xe_du_doan == xe_thuc_te:
        return "Định danh đúng tự động"
    return "Chấp nhận sai"

def chay_mo_phong_anpr(file_xe, file_luot):
    tu_dien_bien_so = doc_danh_sach_xe(file_xe)
    ket_qua_tong_hop = []
    thong_ke = {
        "Định danh đúng tự động": 0,
        "Chấp nhận sai": 0,
        "Chuyển xác minh": 0
    }

    with open(file_luot, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            ma_luot = row['ma_luot'].strip()
            kich_ban = row['kich_ban'].strip()
            xe_thuc_te = row['xe_thuc_te'].strip()
            bien_so_nhan = row['bien_so_nhan_duoc'].strip()

            trang_thai, ma_xe_chon, ly_do = xu_ly_anpr(bien_so_nhan, tu_dien_bien_so)
            nhom_kq = danh_gia_ket_qua(trang_thai, ma_xe_chon, xe_thuc_te)
            thong_ke[nhom_kq] += 1

            ket_qua_tong_hop.append({
                "ma_luot": ma_luot,
                "kich_ban": kich_ban,
                "xe_thuc_te": xe_thuc_te,
                "bien_so_nhan_duoc": bien_so_nhan if bien_so_nhan else "(Trống)",
                "ma_xe_chon": ma_xe_chon if ma_xe_chon else "-",
                "nhom_ket_qua": nhom_kq,
                "ly_do": ly_do
            })

    return ket_qua_tong_hop, thong_ke

if __name__ == "__main__":
    ds_ket_qua, bang_thong_ke = chay_mo_phong_anpr("danh_sach_xe.csv", "luot_xe.csv")
    
    print(f"{'Lượt':<6} | {'Kịch bản':<25} | {'Xe thực':<8} | {'Biển nhận':<11} | {'Xe chọn':<8} | {'Phân loại kết quả'}")
    print("-" * 92)
    for item in ds_ket_qua:
        print(f"{item['ma_luot']:<6} | {item['kich_ban']:<25} | {item['xe_thuc_te']:<8} | "
              f"{item['bien_so_nhan_duoc']:<11} | {item['ma_xe_chon']:<8} | {item['nhom_ket_qua']}")
        
    print("\n--- TỔNG HỢP TỶ LỆ ANPR/LPR (N = 12) ---")
    tong_luot = len(ds_ket_qua)
    for nhom, so_luong in bang_thong_ke.items():
        ty_le = (so_luong / tong_luot) * 100
        print(f"- {nhom}: {so_luong}/{tong_luot} lượt ({ty_le:.2f}%)")
