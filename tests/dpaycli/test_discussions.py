from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import super
import unittest
from parameterized import parameterized
from pprint import pprint
from dpaycli import DPay
from dpaycli.discussions import (
    Query, Discussions_by_trending, Comment_discussions_by_payout,
    Post_discussions_by_payout, Discussions_by_created, Discussions_by_active,
    Discussions_by_cashout, Discussions_by_votes,
    Discussions_by_children, Discussions_by_hot, Discussions_by_feed, Discussions_by_blog,
    Discussions_by_comments, Discussions_by_promoted, Discussions
)
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
            use_condenser=True,
            nobroadcast=True,
            keys={"active": wif},
            num_retries=10
        )
        # from getpass import getpass
        # self.bts.wallet.unlock(getpass())
        set_shared_dpay_instance(cls.bts)
        cls.bts.set_default_account("test")

    def test_trending(self):
        bts = self.bts
        query = Query()
        query["limit"] = 10
        query["tag"] = "dsocial"
        d = Discussions_by_trending(query, dpay_instance=bts)
        self.assertEqual(len(d), 10)

    def test_comment_payout(self):
        bts = self.bts
        query = Query()
        query["limit"] = 10
        query["tag"] = "dsocial"
        d = Comment_discussions_by_payout(query, dpay_instance=bts)
        self.assertEqual(len(d), 10)

    def test_post_payout(self):
        bts = self.bts

        query = Query()
        query["limit"] = 10
        query["tag"] = "dsocial"
        d = Post_discussions_by_payout(query, dpay_instance=bts)
        self.assertEqual(len(d), 10)

    def test_created(self):
        bts = self.bts
        query = Query()
        query["limit"] = 10
        query["tag"] = "dsocial"
        d = Discussions_by_created(query, dpay_instance=bts)
        self.assertEqual(len(d), 10)

    def test_active(self):
        bts = self.bts
        query = Query()
        query["limit"] = 10
        query["tag"] = "dsocial"
        d = Discussions_by_active(query, dpay_instance=bts)
        self.assertEqual(len(d), 10)

    def test_cashout(self):
        bts = self.bts
        query = Query(limit=10)
        Discussions_by_cashout(query, dpay_instance=bts)
        # self.assertEqual(len(d), 10)

    def test_votes(self):
        bts = self.bts
        query = Query()
        query["limit"] = 10
        query["tag"] = "dsocial"
        d = Discussions_by_votes(query, dpay_instance=bts)
        self.assertEqual(len(d), 10)

    def test_children(self):
        bts = self.bts
        query = Query()
        query["limit"] = 10
        query["tag"] = "dsocial"
        d = Discussions_by_children(query, dpay_instance=bts)
        self.assertEqual(len(d), 10)

    def test_feed(self):
        bts = self.bts
        query = Query()
        query["limit"] = 10
        query["tag"] = "gtg"
        d = Discussions_by_feed(query, dpay_instance=bts)
        self.assertEqual(len(d), 10)

    def test_blog(self):
        bts = self.bts
        query = Query()
        query["limit"] = 10
        query["tag"] = "gtg"
        d = Discussions_by_blog(query, dpay_instance=bts)
        self.assertEqual(len(d), 10)

    def test_comments(self):
        bts = self.bts
        query = Query()
        query["limit"] = 10
        query["filter_tags"] = ["gtg"]
        query["start_author"] = "gtg"
        d = Discussions_by_comments(query, dpay_instance=bts)
        self.assertEqual(len(d), 10)

    def test_promoted(self):
        bts = self.bts
        query = Query()
        query["limit"] = 10
        query["tag"] = "dsocial"
        d = Discussions_by_promoted(query, dpay_instance=bts)
        discussions = Discussions(dpay_instance=bts)
        d2 = []
        for dd in discussions.get_discussions("promoted", query, limit=10):
            d2.append(dd)
        self.assertEqual(len(d), 10)
        self.assertEqual(len(d2), 10)
