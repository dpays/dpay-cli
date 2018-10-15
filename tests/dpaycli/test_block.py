from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import super
import unittest
from parameterized import parameterized
from pprint import pprint
from dpaycli import DPay, exceptions
from dpaycli.block import Block, BlockHeader
from datetime import datetime
from dpaycli.instance import set_shared_dpay_instance
from dpaycli.nodelist import NodeList

wif = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"


class Testcases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        nodelist = NodeList()
        nodelist.update_nodes(dpay_instance=DPay(node=nodelist.get_nodes(normal=True, appbase=True), num_retries=10))
        cls.bts = DPay(
            node=nodelist.get_nodes(),
            nobroadcast=True,
            keys={"active": wif},
            num_retries=10
        )
        cls.testnet = DPay(
            node="https://testnet.dpaydev.com",
            nobroadcast=True,
            keys={"active": wif},
            num_retries=10
        )
        cls.test_block_id = 19273700
        cls.test_block_id_testnet = 10000
        # from getpass import getpass
        # self.bts.wallet.unlock(getpass())
        set_shared_dpay_instance(cls.bts)
        cls.bts.set_default_account("test")

    @parameterized.expand([
        ("normal"),
        ("testnet"),
    ])
    def test_block(self, node_param):
        if node_param == "normal":
            bts = self.bts
            test_block_id = self.test_block_id
        else:
            bts = self.testnet
            test_block_id = self.test_block_id_testnet
        block = Block(test_block_id, dpay_instance=bts)
        self.assertEqual(block.identifier, test_block_id)
        self.assertTrue(isinstance(block.time(), datetime))
        self.assertTrue(isinstance(block, dict))

        self.assertTrue(len(block.operations))
        self.assertTrue(isinstance(block.ops_statistics(), dict))

        block2 = Block(test_block_id + 1, dpay_instance=bts)
        self.assertTrue(block2.time() > block.time())
        with self.assertRaises(
            exceptions.BlockDoesNotExistsException
        ):
            Block(0, dpay_instance=bts)

    def test_block_only_ops(self):
        bts = self.bts
        test_block_id = self.test_block_id
        block = Block(test_block_id, only_ops=True, dpay_instance=bts)
        self.assertEqual(block.identifier, test_block_id)
        self.assertTrue(isinstance(block.time(), datetime))
        self.assertTrue(isinstance(block, dict))

        self.assertTrue(len(block.operations))
        self.assertTrue(isinstance(block.ops_statistics(), dict))

        block2 = Block(test_block_id + 1, dpay_instance=bts)
        self.assertTrue(block2.time() > block.time())
        with self.assertRaises(
            exceptions.BlockDoesNotExistsException
        ):
            Block(0, dpay_instance=bts)

    @parameterized.expand([
        ("normal"),
        ("testnet"),
    ])
    def test_block_header(self, node_param):
        if node_param == "normal":
            bts = self.bts
            test_block_id = self.test_block_id
        else:
            bts = self.testnet
            test_block_id = self.test_block_id_testnet
        block = BlockHeader(test_block_id, dpay_instance=bts)
        self.assertEqual(block.identifier, test_block_id)
        self.assertTrue(isinstance(block.time(), datetime))
        self.assertTrue(isinstance(block, dict))

        block2 = BlockHeader(test_block_id + 1, dpay_instance=bts)
        self.assertTrue(block2.time() > block.time())
        with self.assertRaises(
            exceptions.BlockDoesNotExistsException
        ):
            BlockHeader(0, dpay_instance=bts)

    def test_export(self):
        bts = self.bts
        block_num = 2000000

        if bts.rpc.get_use_appbase():
            block = bts.rpc.get_block({"block_num": block_num}, api="block")
            if block and "block" in block:
                block = block["block"]
        else:
            block = bts.rpc.get_block(block_num)

        b = Block(block_num, dpay_instance=bts)
        keys = list(block.keys())
        json_content = b.json()

        for k in keys:
            if k not in "json_metadata":
                if isinstance(block[k], dict) and isinstance(json_content[k], list):
                    self.assertEqual(list(block[k].values()), json_content[k])
                else:
                    self.assertEqual(block[k], json_content[k])

        if bts.rpc.get_use_appbase():
            block = bts.rpc.get_block_header({"block_num": block_num}, api="block")
            if "header" in block:
                block = block["header"]
        else:
            block = bts.rpc.get_block_header(block_num)

        b = BlockHeader(block_num, dpay_instance=bts)
        keys = list(block.keys())
        json_content = b.json()

        for k in keys:
            if k not in "json_metadata":
                if isinstance(block[k], dict) and isinstance(json_content[k], list):
                    self.assertEqual(list(block[k].values()), json_content[k])
                else:
                    self.assertEqual(block[k], json_content[k])
