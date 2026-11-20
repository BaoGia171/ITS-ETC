"""Kiểm thử phần 6.3 (chạy bằng unittest, không cần cài thư viện)."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mo_phong_anpr import (  # noqa: E402
    CHAP_NHAN, CHUYEN_XAC_MINH, chay_mo_phong,
    chuan_hoa_bien_so, nhan_dien_anpr, tao_bang_tra_cuu,
)


class TestAnpr(unittest.TestCase):
    def setUp(self):
        self.bang = {"51A10001": "XE01", "51A10002": "XE02"}

    def test_chuan_hoa(self):
        self.assertEqual(chuan_hoa_bien_so(" 51a - 100.01 "), "51A10001")
        self.assertEqual(chuan_hoa_bien_so(""), "")
        self.assertEqual(chuan_hoa_bien_so(None), "")

    def test_bien_so_hop_le(self):
        kq = nhan_dien_anpr("L01", "51A-10001", self.bang)
        self.assertEqual((kq["trang_thai"], kq["ma_xe_nhan_dien"]), (CHAP_NHAN, "XE01"))

    def test_thieu_bien_so(self):
        kq = nhan_dien_anpr("L04", "", self.bang)
        self.assertEqual(kq["trang_thai"], CHUYEN_XAC_MINH)
        self.assertEqual(kq["ly_do"], "KHONG_DOC_DUOC_BIEN_SO")

    def test_bien_so_chua_dang_ky(self):
        kq = nhan_dien_anpr("L11", "99Z-99999", self.bang)
        self.assertEqual(kq["trang_thai"], CHUYEN_XAC_MINH)
        self.assertEqual(kq["ly_do"], "BIEN_SO_CHUA_DANG_KY")

    def test_trung_bien_so_sau_chuan_hoa(self):
        with self.assertRaises(ValueError):
            tao_bang_tra_cuu([
                {"ma_xe": "XE01", "bien_so": "51A-10001"},
                {"ma_xe": "XE02", "bien_so": "51a10001"},
            ])

    def test_du_lieu_tu_6_1(self):
        kq = chay_mo_phong(ROOT / "du_lieu/xe_dang_ky.csv", ROOT / "du_lieu/luot_xe.csv")
        self.assertEqual(len(kq), 12)
        chap_nhan = [x for x in kq if x["trang_thai"] == CHAP_NHAN]
        self.assertEqual(len(chap_nhan), 8)
        self.assertEqual(len(kq) - len(chap_nhan), 4)
        self.assertEqual(kq[6]["ma_xe_nhan_dien"], "XE03")  # L07: nhận sai xe thực tế
        self.assertEqual(kq[8]["ma_xe_nhan_dien"], "XE02")  # L09: hai nguồn cùng sai


if __name__ == "__main__":
    unittest.main()
