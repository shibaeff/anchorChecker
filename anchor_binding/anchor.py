"""Anchor_binding makes calls to Anchor Protocol to retrieve APY etc."""
import subprocess
import json


class AnchorAPI:
    """To use package import this class..."""

    def __init__(self, bin_path="./app"):
        """Intialize with a binary tool..."""
        self._bin_path = bin_path

    def get_balance(self):
        """Query protocol APY..."""
        process = subprocess.Popen(self._bin_path.split(),
                                   stdout=subprocess.PIPE)
        output, error = process.communicate()
        return json.loads(output)
