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
from dpaycli.witness import Witness
from dpayclibase import operations
from dpaycli.transactionbuilder import TransactionBuilder
from dpaycligraphenebase.account import PasswordKey, PrivateKey, PublicKey
from dpaycli.dpay import DPay
from dpaycli.utils import parse_time, formatTimedelta
from dpaycliapi.exceptions import NumRetriesReached
from dpaycli.nodelist import NodeList
from dpayclibase.transactions import getBlockParams
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# example wif
wif = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"


if __name__ == "__main__":
    stm_online = DPay()
    ref_block_num, ref_block_prefix = getBlockParams(stm_online)
    print("ref_block_num %d - ref_block_prefix %d" % (ref_block_num, ref_block_prefix))

    stm = DPay(offline=True)

    op = operations.Transfer({'from': 'dpayclibot',
                              'to': 'holger80',
                              'amount': "0.001 BBD",
                              'memo': ""})
    tb = TransactionBuilder(dpay_instance=stm)

    tb.appendOps([op])
    tb.appendWif(wif)
    tb.constructTx(ref_block_num=ref_block_num, ref_block_prefix=ref_block_prefix)
    tx = tb.sign(reconstruct_tx=False)
    print(tx.json())
