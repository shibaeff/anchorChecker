"""anchor module provides a proxy to Anchor Protocol API"""

import subprocess
import json


class AnchorAPI:
    """
    A proxy class to the Anchor Protocol

    :param bin_path: path to anchor_tool binary
    :type: str, optional
    """

    def __init__(self, bin_path="./app"):
        """Intialize with a binary tool"""
        self._bin_path = bin_path

    def get_balance(self):
        """Query protocol APY - annual percentage yield"""
        process = subprocess.Popen(self._bin_path.split(),
                                   stdout=subprocess.PIPE)
        output, error = process.communicate()
        return json.loads(output)
