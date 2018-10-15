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

password = "secretPassword"
username = "dpaycli5"
useWallet = False
walletpassword = "123"

if __name__ == "__main__":
    testnet_node = "https://testnet.dpay.vc"
    stm = DPay(node=testnet_node)
    prefix = stm.prefix
    # curl --data "username=username&password=secretPassword" https://testnet.dpay.vc/create
    if useWallet:
        stm.wallet.wipe(True)
        stm.wallet.create(walletpassword)
        stm.wallet.unlock(walletpassword)
    active_key = PasswordKey(username, password, role="active", prefix=prefix)
    owner_key = PasswordKey(username, password, role="owner", prefix=prefix)
    posting_key = PasswordKey(username, password, role="posting", prefix=prefix)
    memo_key = PasswordKey(username, password, role="memo", prefix=prefix)
    active_pubkey = active_key.get_public_key()
    owner_pubkey = owner_key.get_public_key()
    posting_pubkey = posting_key.get_public_key()
    memo_pubkey = memo_key.get_public_key()
    active_privkey = active_key.get_private_key()
    posting_privkey = posting_key.get_private_key()
    owner_privkey = owner_key.get_private_key()
    memo_privkey = memo_key.get_private_key()
    if useWallet:
        stm.wallet.addPrivateKey(owner_privkey)
        stm.wallet.addPrivateKey(active_privkey)
        stm.wallet.addPrivateKey(memo_privkey)
        stm.wallet.addPrivateKey(posting_privkey)
    else:
        stm = DPay(node=testnet_node,
                    wif={'active': str(active_privkey),
                         'posting': str(posting_privkey),
                         'memo': str(memo_privkey)})
    account = Account(username, dpay_instance=stm)
    if account["name"] == "dpaycli":
        account.disallow("dpaycli1", permission='posting')
        account.allow('dpaycli1', weight=1, permission='posting', account=None)
        account.follow("dpaycli1")
    elif account["name"] == "dpaycli5":
        account.allow('dpaycli4', weight=2, permission='active', account=None)
    if useWallet:
        stm.wallet.getAccountFromPrivateKey(str(active_privkey))

    # stm.create_account("dpaycli1", creator=account, password=password1)

    account1 = Account("dpaycli1", dpay_instance=stm)
    b = Blockchain(dpay_instance=stm)
    blocknum = b.get_current_block().identifier

    account.transfer("dpaycli1", 1, "BBD", "test")
    b1 = Block(blocknum, dpay_instance=stm)
