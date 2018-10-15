from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import super
import unittest
from parameterized import parameterized
from dpaycli import DPay
from dpaycli.instance import set_shared_dpay_instance
from dpaycli.transactionbuilder import TransactionBuilder
from dpayclibase.signedtransactions import Signed_Transaction
from dpayclibase.operations import Transfer
from dpaycli.account import Account
from dpaycli.block import Block
from dpaycligraphenebase.base58 import Base58
from dpaycli.amount import Amount
from dpaycli.exceptions import (
    InsufficientAuthorityError,
    MissingKeyError,
    InvalidWifError,
    WalletLocked
)
from dpaycliapi import exceptions
from dpaycli.wallet import Wallet
from dpaycli.utils import formatTimeFromNow
from dpaycli.nodelist import NodeList
wif = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"


class Testcases(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        nodelist = NodeList()
        nodelist.update_nodes(dpay_instance=DPay(node=nodelist.get_nodes(normal=True, appbase=True), num_retries=10))
        cls.stm = DPay(
            node=nodelist.get_nodes(),
            keys={"active": wif, "owner": wif, "memo": wif},
            nobroadcast=True,
            num_retries=10
        )
        cls.testnet = DPay(
            node="https://testnet.dpaydev.com",
            nobroadcast=True,
            keys={"active": wif, "owner": wif, "memo": wif},
            num_retries=10
        )
        set_shared_dpay_instance(cls.stm)
        cls.stm.set_default_account("test")

    def test_emptyTransaction(self):
        stm = self.stm
        tx = TransactionBuilder(dpay_instance=stm)
        self.assertTrue(tx.is_empty())
        self.assertTrue(tx["ref_block_num"] is not None)

    def test_verify_transaction(self):
        stm = self.stm
        block = Block(22005665, dpay_instance=stm)
        trx = block.transactions[28]
        signed_tx = Signed_Transaction(trx)
        key = signed_tx.verify(chain=stm.chain_params, recover_parameter=False)
        public_key = format(Base58(key[0]), stm.prefix)
        self.assertEqual(public_key, "DWB4tzr1wjmuov9ftXR6QNv7qDWsbShMBPQpuwatZsfSc5pKjRDfq")
