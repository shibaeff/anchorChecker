import subprocess

class AnchorAPI:
    def __init__(self, bin_path):
        self._bin_path = bin_path

    def GetBalance(self):
        bashCommand = "bin_path"
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()