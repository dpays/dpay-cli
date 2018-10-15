from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import range
from builtins import super
import mock
import string
import unittest
import random
from pprint import pprint
from dpaycli import DPay
from dpaycli.exceptions import (
    InsufficientAuthorityError,
    MissingKeyError,
    InvalidWifError,
    WalletLocked
)
from dpaycliapi import exceptions
from dpaycli.amount import Amount
from dpaycli.witness import Witness
from dpaycli.account import Account
from dpaycli.instance import set_shared_dpay_instance, shared_dpay_instance
from dpaycli.blockchain import Blockchain
from dpaycli.block import Block
from dpaycli.memo import Memo
from dpaycli.transactionbuilder import TransactionBuilder
from dpayclibase.operations import Transfer
from dpaycligraphenebase.account import PasswordKey, PrivateKey, PublicKey
from dpaycli.utils import parse_time, formatTimedelta
from dpaycliapi.rpcutils import NumRetriesReached
from dpaycli.nodelist import NodeList

# Py3 compatibility
import sys

core_unit = "STX"


class Testcases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        nodelist = NodeList()
        # stm = shared_dpay_instance()
        # stm.config.refreshBackup()
        cls.bts = DPay(
            node=nodelist.get_testnet(),
            nobroadcast=True,
            num_retries=10,
            expiration=120,
        )
        # from getpass import getpass
        # self.bts.wallet.unlock(getpass())
        cls.bts.set_default_account("dpaycli")

        # Test account "dpaycli"
        cls.active_key = "5Jt2wTfhUt5GkZHV1HYVfkEaJ6XnY8D2iA4qjtK9nnGXAhThM3w"
        cls.posting_key = "5Jh1Gtu2j4Yi16TfhoDmg8Qj3ULcgRi7A49JXdfUUTVPkaFaRKz"
        cls.memo_key = "5KPbCuocX26aMxN9CDPdUex4wCbfw9NoT5P7UhcqgDwxXa47bit"

        # Test account "dpaycli1"
        cls.active_key1 = "5Jo9SinzpdAiCDLDJVwuN7K5JcusKmzFnHpEAtPoBHaC1B5RDUd"
        cls.posting_key1 = "5JGNhDXuDLusTR3nbmpWAw4dcmE8WfSM8odzqcQ6mDhJHP8YkQo"
        cls.memo_key1 = "5KA2ddfAffjfRFoe1UhQjJtKnGsBn9xcsdPQTfMt1fQuErDAkWr"

        cls.active_private_key_of_dpaycli4 = '5JkZZEUWrDsu3pYF7aknSo7BLJx7VfxB3SaRtQaHhsPouDYjxzi'
        cls.active_private_key_of_dpaycli5 = '5Hvbm9VjRbd1B3ft8Lm81csaqQudwFwPGdiRKrCmTKcomFS3Z9J'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        stm = self.bts
        stm.nobroadcast = True
        stm.wallet.wipe(True)
        stm.wallet.create("123")
        stm.wallet.unlock("123")

        stm.wallet.addPrivateKey(self.active_key1)
        stm.wallet.addPrivateKey(self.memo_key1)
        stm.wallet.addPrivateKey(self.posting_key1)

        stm.wallet.addPrivateKey(self.active_key)
        stm.wallet.addPrivateKey(self.memo_key)
        stm.wallet.addPrivateKey(self.posting_key)
        stm.wallet.addPrivateKey(self.active_private_key_of_dpaycli4)
        stm.wallet.addPrivateKey(self.active_private_key_of_dpaycli5)

    @classmethod
    def tearDownClass(cls):
        stm = shared_dpay_instance()
        stm.config.recover_with_latest_backup()

    def test_wallet_keys(self):
        stm = self.bts
        stm.wallet.unlock("123")
        priv_key = stm.wallet.getPrivateKeyForPublicKey(str(PrivateKey(self.posting_key, prefix=stm.prefix).pubkey))
        self.assertEqual(str(priv_key), self.posting_key)
        priv_key = stm.wallet.getKeyForAccount("dpaycli", "active")
        self.assertEqual(str(priv_key), self.active_key)
        priv_key = stm.wallet.getKeyForAccount("dpaycli1", "posting")
        self.assertEqual(str(priv_key), self.posting_key1)

        priv_key = stm.wallet.getPrivateKeyForPublicKey(str(PrivateKey(self.active_private_key_of_dpaycli4, prefix=stm.prefix).pubkey))
        self.assertEqual(str(priv_key), self.active_private_key_of_dpaycli4)
        priv_key = stm.wallet.getKeyForAccount("dpaycli4", "active")
        self.assertEqual(str(priv_key), self.active_private_key_of_dpaycli4)

        priv_key = stm.wallet.getPrivateKeyForPublicKey(str(PrivateKey(self.active_private_key_of_dpaycli5, prefix=stm.prefix).pubkey))
        self.assertEqual(str(priv_key), self.active_private_key_of_dpaycli5)
        priv_key = stm.wallet.getKeyForAccount("dpaycli5", "active")
        self.assertEqual(str(priv_key), self.active_private_key_of_dpaycli5)

    def test_transfer(self):
        bts = self.bts
        bts.nobroadcast = False
        bts.wallet.unlock("123")
        # bts.wallet.addPrivateKey(self.active_key)
        # bts.prefix ="STX"
        acc = Account("dpaycli", dpay_instance=bts)
        tx = acc.transfer(
            "dpaycli1", 1.33, "BBD", memo="Foobar")
        self.assertEqual(
            tx["operations"][0][0],
            "transfer"
        )
        self.assertEqual(len(tx['signatures']), 1)
        op = tx["operations"][0][1]
        self.assertIn("memo", op)
        self.assertEqual(op["from"], "dpaycli")
        self.assertEqual(op["to"], "dpaycli1")
        amount = Amount(op["amount"], dpay_instance=bts)
        self.assertEqual(float(amount), 1.33)
        bts.nobroadcast = True

    def test_transfer_memo(self):
        bts = self.bts
        bts.nobroadcast = False
        bts.wallet.unlock("123")
        acc = Account("dpaycli", dpay_instance=bts)
        tx = acc.transfer(
            "dpaycli1", 1.33, "BBD", memo="#Foobar")
        self.assertEqual(
            tx["operations"][0][0],
            "transfer"
        )
        op = tx["operations"][0][1]
        self.assertIn("memo", op)
        self.assertIn("#", op["memo"])
        m = Memo(from_account=op["from"], to_account=op["to"], dpay_instance=bts)
        memo = m.decrypt(op["memo"])
        self.assertEqual(memo, "Foobar")

        self.assertEqual(op["from"], "dpaycli")
        self.assertEqual(op["to"], "dpaycli1")
        amount = Amount(op["amount"], dpay_instance=bts)
        self.assertEqual(float(amount), 1.33)
        bts.nobroadcast = True

    @unittest.skip
    def test_transfer_1of1(self):
        dpay = self.bts
        dpay.nobroadcast = False
        tx = TransactionBuilder(use_condenser_api=True, dpay_instance=dpay)
        tx.appendOps(Transfer(**{"from": 'dpaycli',
                                 "to": 'dpaycli1',
                                 "amount": Amount("0.01 BEX", dpay_instance=dpay),
                                 "memo": '1 of 1 transaction'}))
        self.assertEqual(
            tx["operations"][0]["type"],
            "transfer_operation"
        )
        tx.appendWif(self.active_key)
        tx.sign()
        tx.sign()
        self.assertEqual(len(tx['signatures']), 1)
        tx.broadcast()
        dpay.nobroadcast = True

    @unittest.skip
    def test_transfer_2of2_simple(self):
        # Send a 2 of 2 transaction from elf which needs dpaycli4's cosign to send funds
        dpay = self.bts
        dpay.nobroadcast = False
        tx = TransactionBuilder(use_condenser_api=True, dpay_instance=dpay)
        tx.appendOps(Transfer(**{"from": 'dpaycli5',
                                 "to": 'dpaycli1',
                                 "amount": Amount("0.01 BEX", dpay_instance=dpay),
                                 "memo": '2 of 2 simple transaction'}))

        tx.appendWif(self.active_private_key_of_dpaycli5)
        tx.sign()
        tx.clearWifs()
        tx.appendWif(self.active_private_key_of_dpaycli4)
        tx.sign(reconstruct_tx=False)
        self.assertEqual(len(tx['signatures']), 2)
        tx.broadcast()
        dpay.nobroadcast = True

    @unittest.skip
    def test_transfer_2of2_wallet(self):
        # Send a 2 of 2 transaction from dpaycli5 which needs dpaycli4's cosign to send
        # priv key of dpaycli5 and dpaycli4 are stored in the wallet
        # appendSigner fetches both keys and signs automatically with both keys.
        dpay = self.bts
        dpay.nobroadcast = False
        dpay.wallet.unlock("123")

        tx = TransactionBuilder(use_condenser_api=True, dpay_instance=dpay)
        tx.appendOps(Transfer(**{"from": 'dpaycli5',
                                 "to": 'dpaycli1',
                                 "amount": Amount("0.01 BEX", dpay_instance=dpay),
                                 "memo": '2 of 2 serialized/deserialized transaction'}))

        tx.appendSigner("dpaycli5", "active")
        tx.sign()
        self.assertEqual(len(tx['signatures']), 2)
        tx.broadcast()
        dpay.nobroadcast = True

    @unittest.skip
    def test_transfer_2of2_serialized_deserialized(self):
        # Send a 2 of 2 transaction from dpaycli5 which needs dpaycli4's cosign to send
        # funds but sign the transaction with dpaycli5's key and then serialize the transaction
        # and deserialize the transaction.  After that, sign with dpaycli4's key.
        dpay = self.bts
        dpay.nobroadcast = False
        dpay.wallet.unlock("123")
        # dpay.wallet.removeAccount("dpaycli4")
        dpay.wallet.removePrivateKeyFromPublicKey(str(PublicKey(self.active_private_key_of_dpaycli4, prefix=core_unit)))

        tx = TransactionBuilder(use_condenser_api=True, dpay_instance=dpay)
        tx.appendOps(Transfer(**{"from": 'dpaycli5',
                                 "to": 'dpaycli1',
                                 "amount": Amount("0.01 BEX", dpay_instance=dpay),
                                 "memo": '2 of 2 serialized/deserialized transaction'}))

        tx.appendSigner("dpaycli5", "active")
        tx.addSigningInformation("dpaycli5", "active")
        tx.sign()
        tx.clearWifs()
        self.assertEqual(len(tx['signatures']), 1)
        # dpay.wallet.removeAccount("dpaycli5")
        dpay.wallet.removePrivateKeyFromPublicKey(str(PublicKey(self.active_private_key_of_dpaycli5, prefix=core_unit)))
        tx_json = tx.json()
        del tx
        new_tx = TransactionBuilder(tx=tx_json, dpay_instance=dpay)
        self.assertEqual(len(new_tx['signatures']), 1)
        dpay.wallet.addPrivateKey(self.active_private_key_of_dpaycli4)
        new_tx.appendMissingSignatures()
        new_tx.sign(reconstruct_tx=False)
        self.assertEqual(len(new_tx['signatures']), 2)
        new_tx.broadcast()
        dpay.nobroadcast = True

    @unittest.skip
    def test_transfer_2of2_offline(self):
        # Send a 2 of 2 transaction from dpaycli5 which needs dpaycli4's cosign to send
        # funds but sign the transaction with dpaycli5's key and then serialize the transaction
        # and deserialize the transaction.  After that, sign with dpaycli4's key.
        dpay = self.bts
        dpay.nobroadcast = False
        dpay.wallet.unlock("123")
        # dpay.wallet.removeAccount("dpaycli4")
        dpay.wallet.removePrivateKeyFromPublicKey(str(PublicKey(self.active_private_key_of_dpaycli4, prefix=core_unit)))

        tx = TransactionBuilder(use_condenser_api=True, dpay_instance=dpay)
        tx.appendOps(Transfer(**{"from": 'dpaycli5',
                                 "to": 'dpaycli',
                                 "amount": Amount("0.01 BEX", dpay_instance=dpay),
                                 "memo": '2 of 2 serialized/deserialized transaction'}))

        tx.appendSigner("dpaycli5", "active")
        tx.addSigningInformation("dpaycli5", "active")
        tx.sign()
        tx.clearWifs()
        self.assertEqual(len(tx['signatures']), 1)
        # dpay.wallet.removeAccount("dpaycli5")
        dpay.wallet.removePrivateKeyFromPublicKey(str(PublicKey(self.active_private_key_of_dpaycli5, prefix=core_unit)))
        dpay.wallet.addPrivateKey(self.active_private_key_of_dpaycli4)
        tx.appendMissingSignatures()
        tx.sign(reconstruct_tx=False)
        self.assertEqual(len(tx['signatures']), 2)
        tx.broadcast()
        dpay.nobroadcast = True
        dpay.wallet.addPrivateKey(self.active_private_key_of_dpaycli5)

    @unittest.skip
    def test_transfer_2of2_wif(self):
        nodelist = NodeList()
        # Send a 2 of 2 transaction from elf which needs dpaycli4's cosign to send
        # funds but sign the transaction with elf's key and then serialize the transaction
        # and deserialize the transaction.  After that, sign with dpaycli4's key.
        dpay = DPay(
            node=nodelist.get_testnet(),
            num_retries=10,
            keys=[self.active_private_key_of_dpaycli5],
            expiration=360,
        )

        tx = TransactionBuilder(use_condenser_api=True, dpay_instance=dpay)
        tx.appendOps(Transfer(**{"from": 'dpaycli5',
                                 "to": 'dpaycli',
                                 "amount": Amount("0.01 BEX", dpay_instance=dpay),
                                 "memo": '2 of 2 serialized/deserialized transaction'}))

        tx.appendSigner("dpaycli5", "active")
        tx.addSigningInformation("dpaycli5", "active")
        tx.sign()
        tx.clearWifs()
        self.assertEqual(len(tx['signatures']), 1)
        tx_json = tx.json()
        del dpay
        del tx

        dpay = DPay(
            node=nodelist.get_testnet(),
            num_retries=10,
            keys=[self.active_private_key_of_dpaycli4],
            expiration=360,
        )
        new_tx = TransactionBuilder(tx=tx_json, dpay_instance=dpay)
        new_tx.appendMissingSignatures()
        new_tx.sign(reconstruct_tx=False)
        self.assertEqual(len(new_tx['signatures']), 2)
        new_tx.broadcast()

    @unittest.skip
    def test_verifyAuthority(self):
        stm = self.bts
        stm.wallet.unlock("123")
        tx = TransactionBuilder(use_condenser_api=True, dpay_instance=stm)
        tx.appendOps(Transfer(**{"from": "dpaycli",
                                 "to": "dpaycli1",
                                 "amount": Amount("1.300 BBD", dpay_instance=stm),
                                 "memo": "Foobar"}))
        account = Account("dpaycli", dpay_instance=stm)
        tx.appendSigner(account, "active")
        self.assertTrue(len(tx.wifs) > 0)
        tx.sign()
        tx.verify_authority()
        self.assertTrue(len(tx["signatures"]) > 0)

    def test_create_account(self):
        bts = self.bts
        name = ''.join(random.choice(string.ascii_lowercase) for _ in range(12))
        key1 = PrivateKey()
        key2 = PrivateKey()
        key3 = PrivateKey()
        key4 = PrivateKey()
        key5 = PrivateKey()
        tx = bts.create_account(
            name,
            creator="dpaycli",
            owner_key=format(key1.pubkey, core_unit),
            active_key=format(key2.pubkey, core_unit),
            posting_key=format(key3.pubkey, core_unit),
            memo_key=format(key4.pubkey, core_unit),
            additional_owner_keys=[format(key5.pubkey, core_unit)],
            additional_active_keys=[format(key5.pubkey, core_unit)],
            additional_owner_accounts=["dpaycli1"],  # 1.2.0
            additional_active_accounts=["dpaycli1"],
            storekeys=False
        )
        self.assertEqual(
            tx["operations"][0][0],
            "account_create"
        )
        op = tx["operations"][0][1]
        role = "active"
        self.assertIn(
            format(key5.pubkey, core_unit),
            [x[0] for x in op[role]["key_auths"]])
        self.assertIn(
            format(key5.pubkey, core_unit),
            [x[0] for x in op[role]["key_auths"]])
        self.assertIn(
            "dpaycli1",
            [x[0] for x in op[role]["account_auths"]])
        role = "owner"
        self.assertIn(
            format(key5.pubkey, core_unit),
            [x[0] for x in op[role]["key_auths"]])
        self.assertIn(
            format(key5.pubkey, core_unit),
            [x[0] for x in op[role]["key_auths"]])
        self.assertIn(
            "dpaycli1",
            [x[0] for x in op[role]["account_auths"]])
        self.assertEqual(
            op["creator"],
            "dpaycli")

    def test_connect(self):
        nodelist = NodeList()
        self.bts.connect(node=nodelist.get_testnet())
        bts = self.bts
        self.assertEqual(bts.prefix, "STX")

    def test_set_default_account(self):
        self.bts.set_default_account("dpaycli")

    def test_info(self):
        info = self.bts.info()
        for key in ['current_witness',
                    'head_block_id',
                    'head_block_number',
                    'id',
                    'last_irreversible_block_num',
                    'current_witness',
                    'total_pow',
                    'time']:
            self.assertTrue(key in info)

    def test_finalizeOps(self):
        bts = self.bts
        tx1 = bts.new_tx()
        tx2 = bts.new_tx()

        acc = Account("dpaycli", dpay_instance=bts)
        acc.transfer("dpaycli1", 1, "BEX", append_to=tx1)
        acc.transfer("dpaycli1", 2, "BEX", append_to=tx2)
        acc.transfer("dpaycli1", 3, "BEX", append_to=tx1)
        tx1 = tx1.json()
        tx2 = tx2.json()
        ops1 = tx1["operations"]
        ops2 = tx2["operations"]
        self.assertEqual(len(ops1), 2)
        self.assertEqual(len(ops2), 1)

    def test_weight_threshold(self):
        bts = self.bts
        auth = {'account_auths': [['test', 1]],
                'extensions': [],
                'key_auths': [
                    ['STX55VCzsb47NZwWe5F3qyQKedX9iHBHMVVFSc96PDvV7wuj7W86n', 1],
                    ['STX7GM9YXcsoAJAgKbqW2oVj7bnNXFNL4pk9NugqKWPmuhoEDbkDv', 1]],
                'weight_threshold': 3}  # threshold fine
        bts._test_weights_treshold(auth)
        auth = {'account_auths': [['test', 1]],
                'extensions': [],
                'key_auths': [
                    ['STX55VCzsb47NZwWe5F3qyQKedX9iHBHMVVFSc96PDvV7wuj7W86n', 1],
                    ['STX7GM9YXcsoAJAgKbqW2oVj7bnNXFNL4pk9NugqKWPmuhoEDbkDv', 1]],
                'weight_threshold': 4}  # too high

        with self.assertRaises(ValueError):
            bts._test_weights_treshold(auth)

    def test_allow(self):
        bts = self.bts
        self.assertIn(bts.prefix, "STX")
        acc = Account("dpaycli", dpay_instance=bts)
        self.assertIn(acc.dpay.prefix, "STX")
        tx = acc.allow(
            "STX55VCzsb47NZwWe5F3qyQKedX9iHBHMVVFSc96PDvV7wuj7W86n",
            account="dpaycli",
            weight=1,
            threshold=1,
            permission="active",
        )
        self.assertEqual(
            (tx["operations"][0][0]),
            "account_update"
        )
        op = tx["operations"][0][1]
        self.assertIn("active", op)
        self.assertIn(
            ["STX55VCzsb47NZwWe5F3qyQKedX9iHBHMVVFSc96PDvV7wuj7W86n", '1'],
            op["active"]["key_auths"])
        self.assertEqual(op["active"]["weight_threshold"], 1)

    def test_disallow(self):
        bts = self.bts
        acc = Account("dpaycli", dpay_instance=bts)
        if sys.version > '3':
            _assertRaisesRegex = self.assertRaisesRegex
        else:
            _assertRaisesRegex = self.assertRaisesRegexp
        with _assertRaisesRegex(ValueError, ".*Changes nothing.*"):
            acc.disallow(
                "STX55VCzsb47NZwWe5F3qyQKedX9iHBHMVVFSc96PDvV7wuj7W86n",
                weight=1,
                threshold=1,
                permission="active"
            )
        with _assertRaisesRegex(ValueError, ".*Changes nothing!.*"):
            acc.disallow(
                "STX6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV",
                weight=1,
                threshold=1,
                permission="active"
            )

    def test_update_memo_key(self):
        bts = self.bts
        bts.wallet.unlock("123")
        self.assertEqual(bts.prefix, "STX")
        acc = Account("dpaycli", dpay_instance=bts)
        tx = acc.update_memo_key("STX55VCzsb47NZwWe5F3qyQKedX9iHBHMVVFSc96PDvV7wuj7W86n")
        self.assertEqual(
            (tx["operations"][0][0]),
            "account_update"
        )
        op = tx["operations"][0][1]
        self.assertEqual(
            op["memo_key"],
            "STX55VCzsb47NZwWe5F3qyQKedX9iHBHMVVFSc96PDvV7wuj7W86n")

    def test_approvewitness(self):
        bts = self.bts
        w = Account("dpaycli", dpay_instance=bts)
        tx = w.approvewitness("dpaycli1")
        self.assertEqual(
            (tx["operations"][0][0]),
            "account_witness_vote"
        )
        op = tx["operations"][0][1]
        self.assertIn(
            "dpaycli1",
            op["witness"])

    def test_appendWif(self):
        nodelist = NodeList()
        stm = DPay(node=nodelist.get_testnet(),
                    nobroadcast=True,
                    expiration=120,
                    num_retries=10)
        tx = TransactionBuilder(use_condenser_api=True, dpay_instance=stm)
        tx.appendOps(Transfer(**{"from": "dpaycli",
                                 "to": "dpaycli1",
                                 "amount": Amount("1 BEX", dpay_instance=stm),
                                 "memo": ""}))
        with self.assertRaises(
            MissingKeyError
        ):
            tx.sign()
        with self.assertRaises(
            InvalidWifError
        ):
            tx.appendWif("abcdefg")
        tx.appendWif(self.active_key)
        tx.sign()
        self.assertTrue(len(tx["signatures"]) > 0)

    def test_appendSigner(self):
        nodelist = NodeList()
        stm = DPay(node=nodelist.get_testnet(),
                    keys=[self.active_key],
                    nobroadcast=True,
                    expiration=120,
                    num_retries=10)
        tx = TransactionBuilder(use_condenser_api=True, dpay_instance=stm)
        tx.appendOps(Transfer(**{"from": "dpaycli",
                                 "to": "dpaycli1",
                                 "amount": Amount("1 BEX", dpay_instance=stm),
                                 "memo": ""}))
        account = Account("dpaycli", dpay_instance=stm)
        with self.assertRaises(
            AssertionError
        ):
            tx.appendSigner(account, "abcdefg")
        tx.appendSigner(account, "active")
        self.assertTrue(len(tx.wifs) > 0)
        tx.sign()
        self.assertTrue(len(tx["signatures"]) > 0)

    @unittest.skip
    def test_verifyAuthorityException(self):
        nodelist = NodeList()
        stm = DPay(node=nodelist.get_testnet(),
                    keys=[self.posting_key],
                    nobroadcast=True,
                    expiration=120,
                    num_retries=10)
        tx = TransactionBuilder(use_condenser_api=True, dpay_instance=stm)
        tx.appendOps(Transfer(**{"from": "dpaycli",
                                 "to": "dpaycli1",
                                 "amount": Amount("1 BEX", dpay_instance=stm),
                                 "memo": ""}))
        account = Account("dpaycli2", dpay_instance=stm)
        tx.appendSigner(account, "active")
        tx.appendWif(self.posting_key)
        self.assertTrue(len(tx.wifs) > 0)
        tx.sign()
        with self.assertRaises(
            exceptions.MissingRequiredActiveAuthority
        ):
            tx.verify_authority()
        self.assertTrue(len(tx["signatures"]) > 0)

    def test_Transfer_broadcast(self):
        nodelist = NodeList()
        stm = DPay(node=nodelist.get_testnet(),
                    keys=[self.active_key],
                    nobroadcast=True,
                    expiration=120,
                    num_retries=10)

        tx = TransactionBuilder(use_condenser_api=True, expiration=10, dpay_instance=stm)
        tx.appendOps(Transfer(**{"from": "dpaycli",
                                 "to": "dpaycli1",
                                 "amount": Amount("1 BEX", dpay_instance=stm),
                                 "memo": ""}))
        tx.appendSigner("dpaycli", "active")
        tx.sign()
        tx.broadcast()

    def test_TransactionConstructor(self):
        stm = self.bts
        opTransfer = Transfer(**{"from": "dpaycli",
                                 "to": "dpaycli1",
                                 "amount": Amount("1 BEX", dpay_instance=stm),
                                 "memo": ""})
        tx1 = TransactionBuilder(use_condenser_api=True, dpay_instance=stm)
        tx1.appendOps(opTransfer)
        tx = TransactionBuilder(tx1, dpay_instance=stm)
        self.assertFalse(tx.is_empty())
        self.assertTrue(len(tx.list_operations()) == 1)
        self.assertTrue(repr(tx) is not None)
        self.assertTrue(str(tx) is not None)
        account = Account("dpaycli", dpay_instance=stm)
        tx.appendSigner(account, "active")
        self.assertTrue(len(tx.wifs) > 0)
        tx.sign()
        self.assertTrue(len(tx["signatures"]) > 0)

    def test_follow_active_key(self):
        nodelist = NodeList()
        stm = DPay(node=nodelist.get_testnet(),
                    keys=[self.active_key],
                    nobroadcast=True,
                    expiration=120,
                    num_retries=10)
        account = Account("dpaycli", dpay_instance=stm)
        account.follow("dpaycli1")

    def test_follow_posting_key(self):
        nodelist = NodeList()
        stm = DPay(node=nodelist.get_testnet(),
                    keys=[self.posting_key],
                    nobroadcast=True,
                    expiration=120,
                    num_retries=10)
        account = Account("dpaycli", dpay_instance=stm)
        account.follow("dpaycli1")
