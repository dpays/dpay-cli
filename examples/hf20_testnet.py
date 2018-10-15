from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import sys
from datetime import datetime, timedelta
import time
import io
import logging

from dpaycli.blockchain import Blockchain
from dpaycli.block import Block
from dpaycli.account import Account
from dpaycli.amount import Amount
from dpaycligraphenebase.account import PasswordKey, PrivateKey, PublicKey
from dpaycli.dpay import DPay
from dpaycli.utils import parse_time, formatTimedelta
from dpaycliapi.exceptions import NumRetriesReached
from dpaycli.nodelist import NodeList
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":
    # stm = DPay(node="https://testnet.timcliff.com/")
    # stm = DPay(node="https://testnet.dpaydev.com")
    stm = DPay(node="https://api.dpays.io")
    stm.wallet.unlock(pwd="pwd123")

    account = Account("dpayclibot", dpay_instance=stm)
    print(account.get_voting_power())

    account.transfer("holger80", 0.001, "BBD", "test")
