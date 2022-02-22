import subprocess
import json


class AnchorAPI:
    def __init__(self, bin_path="./app"):
        self._bin_path = bin_path

    def get_balance(self):
        process = subprocess.Popen(self._bin_path.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        return json.loads(output)
