from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import bytes
from builtins import chr
from builtins import range
from builtins import super
import random
from pprint import pprint
from binascii import hexlify
from collections import OrderedDict

from dpayclibase import (
    transactions,
    memo,
    operations,
    objects
)
from dpayclibase.objects import Operation
from dpayclibase.signedtransactions import Signed_Transaction
from dpaycligraphenebase.account import PrivateKey
from dpaycligraphenebase import account
from dpayclibase.operationids import getOperationNameForId
from dpaycligraphenebase.py23 import py23_bytes, bytes_types
from dpaycli.amount import Amount
from dpaycli.asset import Asset
from dpaycli.dpay import DPay

class Benchmark(object):
    goal_time = 2


class Transaction(Benchmark):
    def setup(self):
        self.prefix = u"BEX"
        self.default_prefix = u"DWB"
        self.wif = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"
        self.ref_block_num = 34294
        self.ref_block_prefix = 3707022213
        self.expiration = "2016-04-06T08:29:27"
        self.stm = DPay(
            offline=True
        )

    def doit(self, printWire=False, ops=None):
        if ops is None:
            ops = [Operation(self.op)]
        tx = Signed_Transaction(ref_block_num=self.ref_block_num,
                                ref_block_prefix=self.ref_block_prefix,
                                expiration=self.expiration,
                                operations=ops)
        tx = tx.sign([self.wif], chain=self.prefix)
        tx.verify([PrivateKey(self.wif, prefix=u"DWB").pubkey], self.prefix)
        txWire = hexlify(py23_bytes(tx)).decode("ascii")

    def time_emptyOp(self):
        self.doit(ops=[])

    def time_transfer(self):
        self.op = operations.Transfer(**{
            "from": "foo",
            "to": "baar",
            "amount": Amount("111.110 BEX", dpay_instance=self.stm),
            "memo": "Fooo",
            "prefix": self.default_prefix
        })
        self.doit()

    def time_create_account(self):
        self.op = operations.Account_create(
            **{
                'creator':
                'xeroc',
                'fee':
                '10.000 BEX',
                'json_metadata':
                '',
                'memo_key':
                'DWB6zLNtyFVToBsBZDsgMhgjpwysYVbsQD6YhP3kRkQhANUB4w7Qp',
                'new_account_name':
                'fsafaasf',
                'owner': {
                    'account_auths': [],
                    'key_auths': [[
                        'DWB5jYVokmZHdEpwo5oCG3ES2Ca4VYz'
                        'y6tM8pWWkGdgVnwo2mFLFq', 1
                    ], [
                        'DWB6zLNtyFVToBsBZDsgMhgjpwysYVb'
                        'sQD6YhP3kRkQhANUB4w7Qp', 1
                    ]],
                    'weight_threshold':
                    1
                },
                'active': {
                    'account_auths': [],
                    'key_auths': [[
                        'DWB6pbVDAjRFiw6fkiKYCrkz7PFeL7'
                        'XNAfefrsREwg8MKpJ9VYV9x', 1
                    ], [
                        'DWB6zLNtyFVToBsBZDsgMhgjpwysYV'
                        'bsQD6YhP3kRkQhANUB4w7Qp', 1
                    ]],
                    'weight_threshold':
                    1
                },
                'posting': {
                    'account_auths': [],
                    'key_auths': [[
                        'DWB8CemMDjdUWSV5wKotEimhK6c4d'
                        'Y7p2PdzC2qM1HpAP8aLtZfE7', 1
                    ], [
                        'DWB6zLNtyFVToBsBZDsgMhgjpwys'
                        'YVbsQD6YhP3kRkQhANUB4w7Qp', 1
                    ], [
                        'DWB6pbVDAjRFiw6fkiKYCrkz7PFeL'
                        '7XNAfefrsREwg8MKpJ9VYV9x', 1
                    ]],
                    'weight_threshold':
                    1
                },
                "prefix": self.default_prefix
            })

        self.doit()

    def time_Transfer_to_vesting(self):
        self.op = operations.Transfer_to_vesting(**{
            "from": "foo",
            "to": "baar",
            "amount": "111.110 BEX",
            "prefix": self.default_prefix
        })

        self.doit()

    def time_withdraw_vesting(self):
        self.op = operations.Withdraw_vesting(**{
            "account": "foo",
            "vesting_shares": "100 VESTS",
            "prefix": self.default_prefix
        })

        self.doit()

    def time_Comment(self):
        self.op = operations.Comment(
            **{
                "parent_author": "foobara",
                "parent_permlink": "foobarb",
                "author": "foobarc",
                "permlink": "foobard",
                "title": "foobare",
                "body": "foobarf",
                "json_metadata": {
                    "foo": "bar"
                },
                "prefix": self.default_prefix
            })

        self.doit()

    def time_Vote(self):
        self.op = operations.Vote(
            **{
                "voter": "foobara",
                "author": "foobarc",
                "permlink": "foobard",
                "weight": 1000,
                "prefix": self.default_prefix
            })

        self.doit()

    def time_Transfer_to_savings(self):
        self.op = operations.Transfer_to_savings(
            **{
                "from": "testuser",
                "to": "testuser",
                "amount": "1.000 BEX",
                "memo": "testmemo",
                "prefix": self.default_prefix
            })

        self.doit()

    def time_Transfer_from_savings(self):
        self.op = operations.Transfer_from_savings(
            **{
                "from": "testuser",
                "request_id": 9001,
                "to": "testser",
                "amount": "100.000 BBD",
                "memo": "memohere",
                "prefix": self.default_prefix
            })

        self.doit()

    def time_Cancel_transfer_from_savings(self):
        self.op = operations.Cancel_transfer_from_savings(**{
            "from": "tesuser",
            "request_id": 9001,
            "prefix": self.default_prefix
        })


        self.doit()

    def time_order_create(self):
        self.op = operations.Limit_order_create(
            **{
                "owner": "",
                "orderid": 0,
                "amount_to_sell": "0.000 BEX",
                "min_to_receive": "0.000 BEX",
                "fill_or_kill": False,
                "expiration": "2016-12-31T23:59:59",
                "prefix": self.default_prefix
            })

        self.doit()

    def time_account_update(self):
        self.op = operations.Account_update(
            **{
                "account":
                "streemian",
                "posting": {
                    "weight_threshold":
                    1,
                    "account_auths": [["xeroc", 1], ["fabian", 1]],
                    "key_auths": [[
                        "DWB6KChDK2sns9MwugxkoRvPEnyju"
                        "TxHN5upGsZ1EtanCffqBVVX3", 1
                    ], [
                        "DWB7sw22HqsXbz7D2CmJfmMwt9ri"
                        "mtk518dRzsR1f8Cgw52dQR1pR", 1
                    ]]
                },
                "owner": {
                    "weight_threshold":
                    1,
                    "account_auths": [],
                    "key_auths": [[
                        "DWB7sw22HqsXbz7D2CmJfmMwt9r"
                        "imtk518dRzsR1f8Cgw52dQR1pR", 1
                    ], [
                        "DWB6KChDK2sns9MwugxkoRvPEn"
                        "yjuTxHN5upGsZ1EtanCffqBVVX3", 1
                    ]]
                },
                "active": {
                    "weight_threshold":
                    2,
                    "account_auths": [],
                    "key_auths": [[
                        "DWB6KChDK2sns9MwugxkoRvPEnyju"
                        "TxHN5upGsZ1EtanCffqBVVX3", 1
                    ], [
                        "DWB7sw22HqsXbz7D2CmJfmMwt9ri"
                        "mtk518dRzsR1f8Cgw52dQR1pR", 1
                    ]]
                },
                "memo_key":
                "DWB728uLvStTeAkYJsQefks3FX8yfmpFHp8wXw3RY3kwey2JGDooR",
                "json_metadata":
                "",
                "prefix": self.default_prefix
            })

        self.doit()

    def time_order_cancel(self):
        self.op = operations.Limit_order_cancel(**{
            "owner": "",
            "orderid": 2141244,
            "prefix": self.default_prefix
        })

        self.doit()

    def time_set_route(self):
        self.op = operations.Set_withdraw_vesting_route(
            **{
                "from_account": "xeroc",
                "to_account": "xeroc",
                "percent": 1000,
                "auto_vest": False,
                "prefix": self.default_prefix
            })

        self.doit()

    def time_convert(self):
        self.op = operations.Convert(**{
            "owner": "xeroc",
            "requestid": 2342343235,
            "amount": "100.000 BBD",
            "prefix": self.default_prefix
        })

        self.doit()

    def time_utf8tests(self):
        self.op = operations.Comment(
            **{
                "parent_author": "",
                "parent_permlink": "",
                "author": "a",
                "permlink": "a",
                "title": "-",
                "body": "".join([chr(i) for i in range(0, 2048)]),
                "json_metadata": {},
                "prefix": self.default_prefix
            })

        self.doit()

    def time_feed_publish(self):
        self.op = operations.Feed_publish(
            **{
                "publisher": "xeroc",
                "exchange_rate": {
                    "base": "1.000 BBD",
                    "quote": "4.123 BEX"
                },
                "prefix": self.default_prefix
            })

        self.doit()

    def time_delete_comment(self):
        self.op = operations.Delete_comment(
            **{
                "author": "turbot",
                "permlink": "testpost",
                "prefix": self.default_prefix
            })

        self.doit()

    def time_witness_update(self):
        self.op = operations.Witness_update(
            **{
                "owner":
                "xeroc",
                "url":
                "foooobar",
                "block_signing_key":
                "DWB6zLNtyFVToBsBZDsgMhgjpwysYVbsQD6YhP3kRkQhANUB4w7Qp",
                "props": {
                    "account_creation_fee": "10.000 BEX",
                    "maximum_block_size": 1111111,
                    "bbd_interest_rate": 1000
                },
                "fee":
                "10.000 BEX",
                "prefix": self.default_prefix
            })

        self.doit()

    def time_witness_vote(self):
        self.op = operations.Account_witness_vote(**{
            "account": "xeroc",
            "witness": "chainsquad",
            "approve": True,
            "prefix": self.default_prefix
        })

        self.doit()

    def time_custom_json(self):
        self.op = operations.Custom_json(
            **{
                "json": [
                    "reblog",
                    OrderedDict(
                        [  # need an ordered dict to keep order for the test
                            ("account", "xeroc"), ("author", "chainsquad"), (
                                "permlink", "streemian-com-to-open-its-doors-"
                                "and-offer-a-20-discount")
                        ])
                ],
                "required_auths": [],
                "required_posting_auths": ["xeroc"],
                "id":
                "follow",
                "prefix": self.default_prefix
            })

        self.doit()

    def time_comment_options(self):
        self.op = operations.Comment_options(
            **{
                "author":
                "xeroc",
                "permlink":
                "piston",
                "max_accepted_payout":
                "1000000.000 BBD",
                "percent_dpay_dollars":
                10000,
                "allow_votes":
                True,
                "allow_curation_rewards":
                True,
                "beneficiaries": [{
                    "weight": 2000,
                    "account": "good-karma"
                }, {
                    "weight": 5000,
                    "account": "null"
                }],
                "prefix": self.default_prefix
            })

        self.doit()
