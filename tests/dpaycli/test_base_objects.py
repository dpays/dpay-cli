from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import super
import unittest
from dpaycli import DPay, exceptions
from dpaycli.instance import set_shared_dpay_instance
from dpaycli.account import Account
from dpaycli.witness import Witness
from dpaycli.nodelist import NodeList


class Testcases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        nodelist = NodeList()
        nodelist.update_nodes(dpay_instance=DPay(node=nodelist.get_nodes(normal=True, appbase=True), num_retries=10))
        cls.bts = DPay(
            node=nodelist.get_nodes(),
            nobroadcast=True,
            num_retries=10
        )
        set_shared_dpay_instance(cls.bts)

    def test_Account(self):
        with self.assertRaises(
            exceptions.AccountDoesNotExistsException
        ):
            Account("FOObarNonExisting")

        c = Account("test")
        self.assertEqual(c["name"], "test")
        self.assertIsInstance(c, Account)

    def test_Witness(self):
        with self.assertRaises(
            exceptions.WitnessDoesNotExistsException
        ):
            Witness("FOObarNonExisting")

        c = Witness("jesta")
        self.assertEqual(c["owner"], "jesta")
        self.assertIsInstance(c.account, Account)
