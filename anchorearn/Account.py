from terra_sdk.core import AccAddress, PublicKey
from terra_sdk.key.mnemonic import MnemonicKey
from terra_sdk.client.lcd import Wallet

from utils import JsonSerializable

from output import CHAINS

class Account():
    class Data():
        pass

    def __init__(self):
        pass

    def toData(self) -> Account.Data:
        pass
    
    def toJSON(self) -> str:
        pass

    def get_private_key(self):
        pass

    