from __future__ import print_function
from memory_profiler import profile
import sys
from datetime import datetime, timedelta
import time
import io
from dpaycli.dpay import DPay
from dpaycli.account import Account
from dpaycli.amount import Amount
from dpaycli.blockchain import Blockchain
from dpaycli.utils import parse_time
from dpaycli.instance import set_shared_dpay_instance
import logging
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@profile
def profiling(name_list):
    stm = DPay()
    set_shared_dpay_instance(stm)
    del stm
    print("start")
    for name in name_list:
        print("account: %s" % (name))
        acc = Account(name)
        max_index = acc.virtual_op_count()
        print(max_index)
        stopTime = datetime(2018, 4, 22, 0, 0, 0)
        hist_elem = None
        for h in acc.history_reverse(stop=stopTime):
            hist_elem = h
        print(hist_elem)
    print("blockchain")
    blockchain_object = Blockchain()
    current_num = blockchain_object.get_current_block_num()
    startBlockNumber = current_num - 20
    endBlockNumber = current_num
    block_elem = None
    for o in blockchain_object.stream(start=startBlockNumber, stop=endBlockNumber):
        print("block %d" % (o["block_num"]))
        block_elem = o
    print(block_elem)


if __name__ == "__main__":

    account_list = ["whitehorse", "whitehorse2", "whitehorse3", "whitehorse4", "whitehorse5", "whitehorse6"]
    profiling(account_list)
