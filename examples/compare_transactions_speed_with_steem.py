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
import time

from dpay import DPay as dpayDPay
from dpaybase.account import PrivateKey as dpayPrivateKey
from dpaybase.transactions import SignedTransaction as dpaySignedTransaction
from dpaybase import operations as dpayOperations
from timeit import default_timer as timer


class DPayCliTest(object):

    def setup(self):
        self.prefix = u"BEX"
        self.default_prefix = u"DWB"
        self.wif = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"
        self.ref_block_num = 34294
        self.ref_block_prefix = 3707022213
        self.expiration = "2016-04-06T08:29:27"
        self.stm = DPay(offline=True)

    def doit(self, printWire=False, ops=None):
        ops = [Operation(ops)]
        tx = Signed_Transaction(ref_block_num=self.ref_block_num,
                                ref_block_prefix=self.ref_block_prefix,
                                expiration=self.expiration,
                                operations=ops)
        start = timer()
        tx = tx.sign([self.wif], chain=self.prefix)
        end1 = timer()
        tx.verify([PrivateKey(self.wif, prefix=u"DWB").pubkey], self.prefix)
        end2 = timer()
        return end2 - end1, end1 - start


class DPayTest(object):

    def setup(self):
        self.prefix = u"BEX"
        self.default_prefix = u"DWB"
        self.wif = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"
        self.ref_block_num = 34294
        self.ref_block_prefix = 3707022213
        self.expiration = "2016-04-06T08:29:27"

    def doit(self, printWire=False, ops=None):
        ops = [dpayOperations.Operation(ops)]
        tx = dpaySignedTransaction(ref_block_num=self.ref_block_num,
                                    ref_block_prefix=self.ref_block_prefix,
                                    expiration=self.expiration,
                                    operations=ops)
        start = timer()
        tx = tx.sign([self.wif], chain=self.prefix)
        end1 = timer()
        tx.verify([dpayPrivateKey(self.wif, prefix=u"DWB").pubkey], self.prefix)
        end2 = timer()
        return end2 - end1, end1 - start


if __name__ == "__main__":
    dpay_test = DPayTest()
    dpaycli_test = DPayCliTest()
    dpay_test.setup()
    dpaycli_test.setup()
    dpay_times = []
    dpaycli_times = []
    loops = 50
    for i in range(0, loops):
        print(i)
        opDPay = dpayOperations.Transfer(**{
            "from": "foo",
            "to": "baar",
            "amount": "111.110 BEX",
            "memo": "Fooo"
        })
        opDPayCli = operations.Transfer(**{
            "from": "foo",
            "to": "baar",
            "amount": Amount("111.110 BEX", dpay_instance=DPay(offline=True)),
            "memo": "Fooo"
        })

        t_s, t_v = dpay_test.doit(ops=opDPay)
        dpay_times.append([t_s, t_v])

        t_s, t_v = dpaycli_test.doit(ops=opDPayCli)
        dpaycli_times.append([t_s, t_v])

    dpay_dt = [0, 0]
    dpaycli_dt = [0, 0]
    for i in range(0, loops):
        dpay_dt[0] += dpay_times[i][0]
        dpay_dt[1] += dpay_times[i][1]
        dpaycli_dt[0] += dpaycli_times[i][0]
        dpaycli_dt[1] += dpaycli_times[i][1]
    print("dpay vs dpaycli:\n")
    print("dpay: sign: %.2f s, verification %.2f s" % (dpay_dt[0] / loops, dpay_dt[1] / loops))
    print("dpaycli:  sign: %.2f s, verification %.2f s" % (dpaycli_dt[0] / loops, dpaycli_dt[1] / loops))
    print("------------------------------------")
    print("dpaycli is %.2f %% (sign) and %.2f %% (verify) faster than dpay" %
          (dpay_dt[0] / dpaycli_dt[0] * 100, dpay_dt[1] / dpaycli_dt[1] * 100))
