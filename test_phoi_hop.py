import tempfile
import unittest
from pathlib import Path

from mo_phong_phoi_hop import THU_MUC, chay_mo_phong, doc_csv, doc_ket_qua, doi_chieu_hai_nguon


class TestPhoiHop(unittest.TestCase):
    def test_cac_truong_hop(self):
        a = {"ma_xe_nhan_dien": "XE01", "trang_thai": "CHAP_NHAN"}
        b = {"ma_xe_nhan_dien": "XE02", "trang_thai": "CHAP_NHAN"}
        loi = {"ma_xe_nhan_dien": "", "trang_thai": "CHUYEN_XAC_MINH"}
        for rfid, anpr, ly_do in [
            (a, a, "HAI_NGUON_KHOP"),
            (a, b, "HAI_NGUON_KHONG_KHOP"),
            (None, None, "THIEU_CA_HAI_KET_QUA"),
            (None, a, "THIEU_KET_QUA_RFID"),
            (a, None, "THIEU_KET_QUA_ANPR"),
            (loi, loi, "CA_HAI_KHONG_NHAN_DIEN_DUOC"),
            (loi, a, "RFID_KHONG_NHAN_DIEN_DUOC"),
            (a, loi, "ANPR_KHONG_NHAN_DIEN_DUOC"),
        ]:
            with self.subTest(ly_do=ly_do):
                kq = doi_chieu_hai_nguon(["L99"], {"L99": rfid} if rfid else {}, {"L99": anpr} if anpr else {})[0]
                self.assertEqual(kq["ly_do"], ly_do)
                self.assertEqual(kq["ma_xe_nhan_dien"], "XE01" if ly_do == "HAI_NGUON_KHOP" else "")
                self.assertEqual(kq["trang_thai"], "CHAP_NHAN" if ly_do == "HAI_NGUON_KHOP" else "CHUYEN_XAC_MINH")

    def test_du_lieu_chung(self):
        kq = chay_mo_phong(THU_MUC / "luot_xe.csv", THU_MUC / "ket_qua_rfid.csv", THU_MUC / "ket_qua_anpr.csv")
        self.assertEqual(len(kq), 12)
        chap_nhan = {d["ma_luot"]: d["ma_xe_nhan_dien"] for d in kq if d["trang_thai"] == "CHAP_NHAN"}
        self.assertEqual(chap_nhan, {"L01": "XE01", "L02": "XE04", "L09": "XE02"})
        truth = doc_csv(THU_MUC / "luot_xe.csv", {"ma_luot", "xe_thuc_te"})
        self.assertNotEqual(chap_nhan["L09"], truth["L09"]["xe_thuc_te"])

    def test_csv_khong_hop_le(self):
        for noi_dung in [
            "ma_luot,ma_xe_nhan_dien,trang_thai\nL01,XE01\n",
            "ma_luot,ma_xe_nhan_dien,trang_thai\nL01,XE01,CHAP_NHAN,du\n",
            "ma_luot,ma_xe_nhan_dien,trang_thai\nL01,XE01,CHAP_NHAN\nL01,XE01,CHAP_NHAN\n",
            "ma_luot,ma_xe_nhan_dien,trang_thai\n,XE01,CHAP_NHAN\n",
            "ma_luot,ma_xe_nhan_dien,trang_thai\nL01,,CHAP_NHAN\n",
            "ma_luot,ma_xe_nhan_dien,trang_thai\nL01,XE01,OK\n",
            "ma_luot,ma_xe\nL01,XE01\n",
        ]:
            with self.subTest(csv=noi_dung), tempfile.TemporaryDirectory() as tmp:
                tep = Path(tmp) / "loi.csv"
                tep.write_text(noi_dung, encoding="utf-8")
                with self.assertRaises(ValueError):
                    doc_ket_qua(tep)

    def test_ma_ngoai_danh_sach(self):
        with tempfile.TemporaryDirectory() as tmp:
            tep = Path(tmp) / "luot.csv"
            tep.write_text("ma_luot\nL99\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                chay_mo_phong(tep, THU_MUC / "ket_qua_rfid.csv", THU_MUC / "ket_qua_anpr.csv")


if __name__ == "__main__":
    unittest.main()
