from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import range
from builtins import super
import mock
import string
import unittest
from parameterized import parameterized
import random
import json
from pprint import pprint
from dpaycli import DPay
from dpaycli.amount import Amount
from dpaycli.memo import Memo
from dpaycli.version import version as dpaycli_version
from dpaycli.wallet import Wallet
from dpaycli.witness import Witness
from dpaycli.account import Account
from dpaycligraphenebase.account import PrivateKey
from dpaycli.instance import set_shared_dpay_instance, shared_dpay_instance
from dpaycli.nodelist import NodeList
# Py3 compatibility
import sys
core_unit = "DWB"
wif = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"


class Testcases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        stm = shared_dpay_instance()
        stm.config.refreshBackup()
        nodelist = NodeList()
        nodelist.update_nodes(dpay_instance=DPay(node=nodelist.get_nodes(normal=True, appbase=True), num_retries=10))

        cls.stm = DPay(
            node=nodelist.get_nodes(),
            nobroadcast=True,
            # We want to bundle many operations into a single transaction
            bundle=True,
            num_retries=10
            # Overwrite wallet to use this list of wifs only
        )
        cls.testnet = DPay(
            node="https://testnet.dpaydev.com",
            nobroadcast=True,
            bundle=True,
            num_retries=10
        )
        cls.stm.set_default_account("test")
        set_shared_dpay_instance(cls.stm)
        # self.stm.newWallet("TestingOneTwoThree")

        cls.wallet = Wallet(dpay_instance=cls.stm)
        cls.wallet.wipe(True)
        cls.wallet.newWallet(pwd="TestingOneTwoThree")
        cls.wallet.unlock(pwd="TestingOneTwoThree")
        cls.wallet.addPrivateKey(wif)

    @classmethod
    def tearDownClass(cls):
        stm = shared_dpay_instance()
        stm.config.recover_with_latest_backup()

    @parameterized.expand([
        ("normal"),
        ("testnet"),
    ])
    def test_set_default_account(self, node_param):
        if node_param == "normal":
            stm = self.stm
        elif node_param == "testnet":
            stm = self.testnet
        stm.set_default_account("test")

        self.assertEqual(stm.config["default_account"], "test")
