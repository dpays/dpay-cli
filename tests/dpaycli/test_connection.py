import unittest
from dpaycli import DPay
from dpaycli.account import Account
from dpaycli.instance import set_shared_dpay_instance, SharedInstance
from dpaycli.blockchainobject import BlockchainObject
from dpaycli.nodelist import NodeList

import logging
log = logging.getLogger()


class Testcases(unittest.TestCase):

    def test_stm1stm2(self):
        nodelist = NodeList()
        nodelist.update_nodes(dpay_instance=DPay(node=nodelist.get_nodes(normal=True, appbase=True), num_retries=10))
        b1 = DPay(
            node=nodelist.get_testnet(testnet=True, testnetdev=False),
            nobroadcast=True,
            num_retries=10
        )

        b2 = DPay(
            node=nodelist.get_nodes(),
            nobroadcast=True,
            num_retries=10
        )

        self.assertNotEqual(b1.rpc.url, b2.rpc.url)

    def test_default_connection(self):
        nodelist = NodeList()
        nodelist.update_nodes(dpay_instance=DPay(node=nodelist.get_nodes(normal=True, appbase=True), num_retries=10))
        b1 = DPay(
            node=nodelist.get_testnet(testnet=True, testnetdev=False),
            nobroadcast=True,
        )
        set_shared_dpay_instance(b1)
        test = Account("dpaycli")

        b2 = DPay(
            node=nodelist.get_nodes(),
            nobroadcast=True,
        )
        set_shared_dpay_instance(b2)

        bts = Account("dpaycli")

        self.assertEqual(test.dpay.prefix, "STX")
        self.assertEqual(bts.dpay.prefix, "DWB")
