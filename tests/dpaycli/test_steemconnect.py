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
from dpaycli import DPay, exceptions
from dpaycli.amount import Amount
from dpaycli.memo import Memo
from dpaycli.version import version as dpaycli_version
from dpaycli.wallet import Wallet
from dpaycli.witness import Witness
from dpaycli.account import Account
from dpaycligraphenebase.account import PrivateKey
from dpaycli.instance import set_shared_dpay_instance
from dpaycli.nodelist import NodeList
from dpaycli.dpayid import DPayID
# Py3 compatibility
import sys
core_unit = "DWB"


class Testcases(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        nodelist = NodeList()
        nodelist.update_nodes(dpay_instance=DPay(node=nodelist.get_nodes(normal=True, appbase=True), num_retries=10))
        cls.bts = DPay(
            node=nodelist.get_nodes(),
            nobroadcast=True,
            unsigned=True,
            data_refresh_time_seconds=900,
            num_retries=10)
        cls.testnet = DPay(
            node="https://testnet.dpaydev.com",
            nobroadcast=True,
            unsigned=True,
            data_refresh_time_seconds=900,
            num_retries=10)

        cls.account = Account("test", full=True, dpay_instance=cls.bts)
        cls.account_testnet = Account("test", full=True, dpay_instance=cls.testnet)

    def test_transfer(self):
        bts = self.bts
        acc = self.account
        acc.dpay.txbuffer.clear()
        tx = acc.transfer(
            "test1", 1.000, "BEX", memo="test")
        dpid = DPayID(dpay_instance=bts)
        url = dpid.url_from_tx(tx)
        url_test = 'https://go.dpayid.io/sign/transfer?from=test&to=test1&amount=1.000+BEX&memo=test'
        self.assertEqual(len(url), len(url_test))
        self.assertEqual(len(url.split('?')), 2)
        self.assertEqual(url.split('?')[0], url_test.split('?')[0])

        url_parts = (url.split('?')[1]).split('&')
        url_test_parts = (url_test.split('?')[1]).split('&')

        self.assertEqual(len(url_parts), 4)
        self.assertEqual(len(list(set(url_parts).intersection(set(url_test_parts)))), 4)

    @parameterized.expand([
        ("normal"),
        ("testnet"),
    ])
    def test_login_url(self, node_param):
        if node_param == "normal":
            bts = self.bts
        elif node_param == "testnet":
            bts = self.testnet
        dpid = DPayID(dpay_instance=bts)
        url = dpid.get_login_url("localhost", scope="login,vote")
        url_test = 'https://go.dpayid.io/oauth2/authorize?client_id=None&redirect_uri=localhost&scope=login,vote'
        self.assertEqual(len(url), len(url_test))
        self.assertEqual(len(url.split('?')), 2)
        self.assertEqual(url.split('?')[0], url_test.split('?')[0])

        url_parts = (url.split('?')[1]).split('&')
        url_test_parts = (url_test.split('?')[1]).split('&')

        self.assertEqual(len(url_parts), 3)
        self.assertEqual(len(list(set(url_parts).intersection(set(url_test_parts)))), 3)
