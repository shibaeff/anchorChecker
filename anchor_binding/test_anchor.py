import unittest
from anchor import AnchorAPI


class TestAPI(unittest.TestCase):
    def test_get_balance(self):
        obj = AnchorAPI()
        assert (type(obj.get_balance()["APY"]) == float)
        assert (obj.get_balance()["APY"] > 15.0)

    def test_get_anc_price(self):
        obj = AnchorAPI().get_anc_price()
        assert (type(obj) == float)
        assert (obj > 0)

    def test_get_ust_price(self):
        obj = AnchorAPI().get_ust_price()
        assert (type(obj) == float)
        assert (obj > 0)

    def test_get_ust_market_cap(self):
        obj = AnchorAPI().get_ust_cap()
        assert (type(obj) == float)
        assert (obj > 0)

    def test_get_anc_market_cap(self):
        obj = AnchorAPI().get_anc_cap()
        assert (type(obj) == float)
        assert (obj > 0)


if __name__ == "__main__":
    unittest.main()
