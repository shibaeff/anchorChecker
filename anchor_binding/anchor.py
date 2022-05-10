"""anchor module provides a proxy to Anchor Protocol API"""

import subprocess
import json
import requests


class AnchorAPI:
    """
    A proxy class to the Anchor Protocol

    :param bin_path: path to anchor_tool binary
    :type: str, optional
    """

    def __init__(self, bin_path="./app"):
        """Intialize with a binary tool"""
        self._bin_path = bin_path

    def get_balance(self) -> str:
        """
        Query protocol APY - annual percentage yield

        :return: json with APY
        :type: str
        """
        process = subprocess.Popen(self._bin_path.split(),
                                   stdout=subprocess.PIPE)
        output, error = process.communicate()
        return json.loads(output)

    def get_anc_price(self) -> float:
        """
        Query current ANC price

        :return a price
        :type:  float
        """
        key = "https://api.binance.com/api/v3/ticker/price?symbol=ANCUSDT"
        # requesting data from url
        data = requests.get(key)
        data = data.json()
        return float(data['price'])

    def get_ust_price(self) -> float:
        """
        Query current ANC price

        :return a price
        :type:  float
        """
        key = "https://api.binance.com/api/v3/ticker/price?symbol=USTUSDT"
        # requesting data from url
        data = requests.get(key)
        data = data.json()
        return float(data['price'])

    def get_ust_cap(self) -> float:
        """
        Query current UST market cap

        :return: a market cap
        """
        key = "https://api.binance.com/api/v3/ticker/24hr?symbol=USTUSDT"
        data = requests.get(key)
        data = data.json()
        return float(data["weightedAvgPrice"]) * float(data["volume"])

    def get_anc_cap(self) -> float:
        """
        Query current ANC market cap

        :return: a market cap
        """
        key = "https://api.binance.com/api/v3/ticker/24hr?symbol=ANCUSDT"
        data = requests.get(key)
        data = data.json()
        return float(data["weightedAvgPrice"]) * float(data["volume"])
