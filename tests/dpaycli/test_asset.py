from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import str
from builtins import super
import unittest
from parameterized import parameterized
from dpaycli import DPay
from dpaycli.asset import Asset
from dpaycli.instance import set_shared_dpay_instance
from dpaycli.exceptions import AssetDoesNotExistsException
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
        cls.testnet = DPay(
            node="https://testnet.dpaydev.com",
            nobroadcast=True,
            num_retries=10
        )
        set_shared_dpay_instance(cls.bts)

    @parameterized.expand([
        ("normal"),
        ("testnet"),
    ])
    def test_assert(self, node_param):
        if node_param == "normal":
            stm = self.bts
        else:
            stm = self.testnet
        with self.assertRaises(AssetDoesNotExistsException):
            Asset("FOObarNonExisting", full=False, dpay_instance=stm)

    @parameterized.expand([
        ("normal", "BBD", "BBD", 3, "@@000000013"),
        ("normal", "BEX", "BEX", 3, "@@000000021"),
        ("normal", "VESTS", "VESTS", 6, "@@000000037"),
        ("normal", "@@000000013", "BBD", 3, "@@000000013"),
        ("normal", "@@000000021", "BEX", 3, "@@000000021"),
        ("normal", "@@000000037", "VESTS", 6, "@@000000037"),
    ])
    def test_properties(self, node_param, data, symbol_str, precision, asset_str):
        if node_param == "normal":
            stm = self.bts
        else:
            stm = self.testnet
        asset = Asset(data, full=False, dpay_instance=stm)
        self.assertEqual(asset.symbol, symbol_str)
        self.assertEqual(asset.precision, precision)
        self.assertEqual(asset.asset, asset_str)

    def test_assert_equal(self):
        stm = self.bts
        asset1 = Asset("BBD", full=False, dpay_instance=stm)
        asset2 = Asset("BBD", full=False, dpay_instance=stm)
        self.assertTrue(asset1 == asset2)
        self.assertTrue(asset1 == "BBD")
        self.assertTrue(asset2 == "BBD")
        asset3 = Asset("BEX", full=False, dpay_instance=stm)
        self.assertTrue(asset1 != asset3)
        self.assertTrue(asset3 != "BBD")
        self.assertTrue(asset1 != "BEX")

        a = {'asset': '@@000000021', 'precision': 3, 'id': 'BEX', 'symbol': 'BEX'}
        b = {'asset': '@@000000021', 'precision': 3, 'id': '@@000000021', 'symbol': 'BEX'}
        self.assertTrue(Asset(a, dpay_instance=stm) == Asset(b, dpay_instance=stm))

    """
    # Mocker comes from pytest-mock, providing an easy way to have patched objects
    # for the life of the test.
    def test_calls(mocker):
        asset = Asset("USD", lazy=True, dpay_instance=DPay(offline=True))
        method = mocker.patch.object(Asset, 'get_call_orders')
        asset.calls
        method.assert_called_with(10)
    """
