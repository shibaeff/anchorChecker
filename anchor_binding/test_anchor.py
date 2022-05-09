import unittest
import anchor_binding.anchor as anchor


def test_get_balance():
    obj = anchor.AnchorAPI()
    assert (type(obj.get_balance()["APY"]) == float)
    assert (obj.get_balance()["APY"] > 15.0)


def test_get_price():
    obj = anchor.AnchorAPI()
    assert (type(obj.get_balance()["APY"]) == float)
    assert (obj.get_balance()["APY"] > 15.0)


if __name__ == "__main__":
    unittest.main()
