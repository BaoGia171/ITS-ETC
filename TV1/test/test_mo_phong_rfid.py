import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import unittest
from mo_phong_rfid import (
    chuan_hoa_rfid,
    tao_bang_tra_cuu,
    nhan_dien_rfid,
    chay_mo_phong
)


class TestMoPhongRFID(unittest.TestCase):

    # 1. Kiem tra chuan hoa ma RFID
    def test_chuan_hoa_rfid(self):
        self.assertEqual(chuan_hoa_rfid(" tag001 "), "TAG001")

    # 2. Kiem tra tra cuu the hop le
    def test_the_hop_le(self):
        bang = tao_bang_tra_cuu([
            {"ma_xe": "XE01", "ma_the": "TAG001"}
        ])

        kq = nhan_dien_rfid("L01", "test", "TAG001", bang)
        self.assertEqual(kq["ma_xe_nhan_dien"], "XE01")
        self.assertEqual(kq["trang_thai"], "CHAP_NHAN")

    # 3. Kiem tra RFID trong
    def test_rfid_trong(self):
        bang = tao_bang_tra_cuu([
            {"ma_xe": "XE01", "ma_the": "TAG001"}
        ])

        kq = nhan_dien_rfid("L02", "test", "", bang)
        self.assertEqual(kq["trang_thai"], "CHUYEN_XAC_MINH")
        self.assertEqual(kq["ly_do"], "KHONG_DOC_DUOC_RFID")

    # 4. Kiem tra the chua dang ky
    def test_the_chua_dang_ky(self):
        bang = tao_bang_tra_cuu([
            {"ma_xe": "XE01", "ma_the": "TAG001"}
        ])

        kq = nhan_dien_rfid("L03", "test", "TAG999", bang)
        self.assertEqual(kq["trang_thai"], "CHUYEN_XAC_MINH")
        self.assertEqual(kq["ly_do"], "THE_RFID_CHUA_DANG_KY")

    # 5. Kiem tra the bi trung sau chuan hoa
    def test_the_trung(self):
        with self.assertRaises(ValueError):
            tao_bang_tra_cuu([
                {"ma_xe": "XE01", "ma_the": "TAG001"},
                {"ma_xe": "XE02", "ma_the": " tag001 "}
            ])

    # 6. Kiem tra xu ly toan bo du lieu
    
    # 6. Kiem tra xu ly toan bo du lieu
    def test_toan_bo_du_lieu(self):
        thu_muc = Path(__file__).resolve().parents[1]

        kq = chay_mo_phong(
            thu_muc / "du_lieu" / "xe_dang_ky.csv",
            thu_muc / "du_lieu" / "luot_xe.csv"
        )

        self.assertEqual(len(kq), 12)


if __name__ == "__main__":
    unittest.main(verbosity=2)
