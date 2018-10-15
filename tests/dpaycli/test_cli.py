from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import str
from builtins import super
import unittest
import mock
import click
from click.testing import CliRunner
from pprint import pprint
from dpaycli import DPay, exceptions
from dpaycli.account import Account
from dpaycli.amount import Amount
from dpaycligraphenebase.account import PrivateKey
from dpaycli.cli import cli, balance
from dpaycli.instance import set_shared_dpay_instance, shared_dpay_instance
from dpayclibase.operationids import getOperationNameForId
from dpaycli.nodelist import NodeList

wif = "5Jt2wTfhUt5GkZHV1HYVfkEaJ6XnY8D2iA4qjtK9nnGXAhThM3w"
posting_key = "5Jh1Gtu2j4Yi16TfhoDmg8Qj3ULcgRi7A49JXdfUUTVPkaFaRKz"
memo_key = "5KPbCuocX26aMxN9CDPdUex4wCbfw9NoT5P7UhcqgDwxXa47bit"
pub_key = "STX52xMqKegLk4tdpNcUXU9Rw5DtdM9fxf3f12Gp55v1UjLX3ELZf"


class Testcases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nodelist = NodeList()
        cls.nodelist.update_nodes()
        cls.nodelist.update_nodes(dpay_instance=DPay(node=cls.nodelist.get_nodes(normal=True, appbase=True), num_retries=10))
        # stm = shared_dpay_instance()
        # stm.config.refreshBackup()
        runner = CliRunner()
        result = runner.invoke(cli, ['-o', 'set', 'default_vote_weight', '100'])
        if result.exit_code != 0:
            raise AssertionError(str(result))
        result = runner.invoke(cli, ['-o', 'set', 'default_account', 'dpaycli'])
        if result.exit_code != 0:
            raise AssertionError(str(result))
        result = runner.invoke(cli, ['-o', 'set', 'nodes', str(cls.nodelist.get_testnet())])
        if result.exit_code != 0:
            raise AssertionError(str(result))
        result = runner.invoke(cli, ['createwallet', '--wipe'], input="test\ntest\n")
        if result.exit_code != 0:
            raise AssertionError(str(result))
        result = runner.invoke(cli, ['addkey'], input="test\n" + wif + "\n")
        if result.exit_code != 0:
            raise AssertionError(str(result))
        result = runner.invoke(cli, ['addkey'], input="test\n" + posting_key + "\n")
        if result.exit_code != 0:
            raise AssertionError(str(result))
        result = runner.invoke(cli, ['addkey'], input="test\n" + memo_key + "\n")
        if result.exit_code != 0:
            raise AssertionError(str(result))

    @classmethod
    def tearDownClass(cls):
        stm = shared_dpay_instance()
        stm.config.recover_with_latest_backup()

    def test_balance(self):
        runner = CliRunner()
        runner.invoke(cli, ['set', 'nodes', str(self.nodelist.get_testnet())])
        result = runner.invoke(cli, ['balance', 'dpaycli', 'dpaycli1'])
        self.assertEqual(result.exit_code, 0)

    def test_interest(self):
        runner = CliRunner()
        runner.invoke(cli, ['set', 'nodes', str(self.nodelist.get_testnet())])
        result = runner.invoke(cli, ['interest', 'dpaycli', 'dpaycli1'])
        self.assertEqual(result.exit_code, 0)

    def test_config(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['config'])
        self.assertEqual(result.exit_code, 0)

    def test_addkey(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['createwallet', '--wipe'], input="test\ntest\n")
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ['addkey'], input="test\n" + wif + "\n")
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ['addkey'], input="test\n" + posting_key + "\n")
        self.assertEqual(result.exit_code, 0)

    def test_parsewif(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['parsewif'], input=wif + "\nexit\n")
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ['parsewif', '--unsafe-import-key', wif])
        self.assertEqual(result.exit_code, 0)

    def test_delkey(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['delkey', '--confirm', pub_key], input="test\n")
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ['addkey'], input="test\n" + wif + "\n")
        self.assertEqual(result.exit_code, 0)

    def test_listkeys(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['listkeys'])
        self.assertEqual(result.exit_code, 0)

    def test_listaccounts(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['listaccounts'])
        self.assertEqual(result.exit_code, 0)

    def test_info(self):
        runner = CliRunner()
        runner.invoke(cli, ['-o', 'set', 'nodes', str(self.nodelist.get_testnet())])
        result = runner.invoke(cli, ['info'])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ['info', 'dpaycli'])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ['info', '100'])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ['info', '--', '-1'])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ['info', pub_key])
        self.assertEqual(result.exit_code, 0)

    def test_info2(self):
        runner = CliRunner()
        runner.invoke(cli, ['-o', 'set', 'nodes', self.nodelist.get_nodes()])
        result = runner.invoke(cli, ['info', '--', '-1:1'])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ['info', 'gtg'])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ['info', "@gtg/witness-gtg-log"])
        self.assertEqual(result.exit_code, 0)
        runner.invoke(cli, ['-o', 'set', 'nodes', str(self.nodelist.get_testnet())])

    def test_changepassword(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['changewalletpassphrase'], input="test\ntest\ntest\n")
        self.assertEqual(result.exit_code, 0)

    def test_walletinfo(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['walletinfo'])
        self.assertEqual(result.exit_code, 0)

    def test_keygen(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['keygen'])
        self.assertEqual(result.exit_code, 0)

    def test_set(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['-o', 'set', 'set_default_vote_weight', '100'])
        self.assertEqual(result.exit_code, 0)

    def test_upvote(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['-o', 'upvote', '@test/abcd'], input="test\n")
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ['-o', 'upvote', '@test/abcd', '100'], input="test\n")
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ['-o', 'upvote', '--weight', '100', '@test/abcd'], input="test\n")
        self.assertEqual(result.exit_code, 0)

    def test_downvote(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['-o', 'downvote', '@test/abcd'], input="test\n")
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ['-o', 'downvote', '@test/abcd', '100'], input="test\n")
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ['-o', 'downvote', '--weight', '100', '@test/abcd'], input="test\n")
        self.assertEqual(result.exit_code, 0)

    def test_transfer(self):
        runner = CliRunner()
        runner.invoke(cli, ['-o', 'set', 'nodes', str(self.nodelist.get_testnet())])
        result = runner.invoke(cli, ['transfer', 'dpaycli1', '1', 'BBD', 'test'], input="test\n")
        self.assertEqual(result.exit_code, 0)

    def test_powerdownroute(self):
        runner = CliRunner()
        runner.invoke(cli, ['-o', 'set', 'nodes', str(self.nodelist.get_testnet())])
        result = runner.invoke(cli, ['powerdownroute', 'dpaycli1'], input="test\n")
        self.assertEqual(result.exit_code, 0)

    def test_convert(self):
        runner = CliRunner()
        runner.invoke(cli, ['-o', 'set', 'nodes', str(self.nodelist.get_testnet())])
        result = runner.invoke(cli, ['convert', '1'], input="test\n")
        self.assertEqual(result.exit_code, 0)

    def test_powerup(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['powerup', '1'], input="test\n")
        self.assertEqual(result.exit_code, 0)

    def test_powerdown(self):
        runner = CliRunner()
        runner.invoke(cli, ['-o', 'set', 'nodes', str(self.nodelist.get_testnet())])
        result = runner.invoke(cli, ['-d', 'powerdown', '1e3'], input="test\n")
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ['-d', 'powerdown', '0'], input="test\n")
        self.assertEqual(result.exit_code, 0)

    def test_updatememokey(self):
        runner = CliRunner()
        runner.invoke(cli, ['-o', 'set', 'nodes', str(self.nodelist.get_testnet())])
        result = runner.invoke(cli, ['-d', 'updatememokey'], input="test\ntest\ntest\n")
        self.assertEqual(result.exit_code, 0)

    def test_permissions(self):
        runner = CliRunner()
        runner.invoke(cli, ['-o', 'set', 'nodes', str(self.nodelist.get_testnet())])
        result = runner.invoke(cli, ['permissions', 'dpaycli'])
        self.assertEqual(result.exit_code, 0)

    def test_follower(self):
        runner = CliRunner()
        runner.invoke(cli, ['-o', 'set', 'nodes', str(self.nodelist.get_testnet())])
        result = runner.invoke(cli, ['follower', 'dpaycli1'])
        self.assertEqual(result.exit_code, 0)

    def test_following(self):
        runner = CliRunner()
        runner.invoke(cli, ['-o', 'set', 'nodes', str(self.nodelist.get_testnet())])
        result = runner.invoke(cli, ['following', 'dpaycli'])
        self.assertEqual(result.exit_code, 0)

    def test_muter(self):
        runner = CliRunner()
        runner.invoke(cli, ['-o', 'set', 'nodes', str(self.nodelist.get_testnet())])
        result = runner.invoke(cli, ['muter', 'dpaycli1'])
        self.assertEqual(result.exit_code, 0)

    def test_muting(self):
        runner = CliRunner()
        runner.invoke(cli, ['-o', 'set', 'nodes', str(self.nodelist.get_testnet())])
        result = runner.invoke(cli, ['muting', 'dpaycli'])
        self.assertEqual(result.exit_code, 0)

    def test_allow_disallow(self):
        runner = CliRunner()
        runner.invoke(cli, ['-o', 'set', 'nodes', str(self.nodelist.get_testnet())])
        result = runner.invoke(cli, ['-d', 'allow', '--account', 'dpaycli', '--permission', 'posting', 'dpaycli1'], input="test\n")
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ['-d', 'disallow', '--account', 'dpaycli', '--permission', 'posting', 'dpaycli1'], input="test\n")
        self.assertEqual(result.exit_code, 0)

    def test_witnesses(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['witnesses'])
        self.assertEqual(result.exit_code, 0)

    def test_votes(self):
        runner = CliRunner()
        runner.invoke(cli, ['-o', 'set', 'nodes', self.nodelist.get_nodes()])
        result = runner.invoke(cli, ['votes', '--direction', 'out', 'test'])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ['votes', '--direction', 'in', 'test'])
        runner.invoke(cli, ['-o', 'set', 'nodes', str(self.nodelist.get_testnet())])
        self.assertEqual(result.exit_code, 0)

    def test_approvewitness(self):
        runner = CliRunner()
        runner.invoke(cli, ['-o', 'set', 'nodes', str(self.nodelist.get_testnet())])
        result = runner.invoke(cli, ['-o', 'approvewitness', 'dpaycli1'], input="test\n")
        self.assertEqual(result.exit_code, 0)

    def test_disapprovewitness(self):
        runner = CliRunner()
        runner.invoke(cli, ['-o', 'set', 'nodes', str(self.nodelist.get_testnet())])
        result = runner.invoke(cli, ['-o', 'disapprovewitness', 'dpaycli1'], input="test\n")
        self.assertEqual(result.exit_code, 0)

    def test_newaccount(self):
        runner = CliRunner()
        runner.invoke(cli, ['-o', 'set', 'nodes', str(self.nodelist.get_testnet())])
        result = runner.invoke(cli, ['-d', 'newaccount', 'dpaycli3'], input="test\ntest\ntest\n")
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ['-d', 'newaccount', 'dpaycli3'], input="test\ntest\ntest\n")
        self.assertEqual(result.exit_code, 0)

    def test_importaccount(self):
        runner = CliRunner()
        runner.invoke(cli, ['-o', 'set', 'nodes', str(self.nodelist.get_testnet())])
        result = runner.invoke(cli, ['importaccount', '--roles', '["owner", "active", "posting", "memo"]', 'dpaycli2'], input="test\numybjvCafrt8LdoCjEimQiQ4\n")
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ['delkey', '--confirm', 'STX7mLs2hns87f7kbf3o2HBqNoEaXiTeeU89eVF6iUCrMQJFzBsPo'], input="test\n")
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ['delkey', '--confirm', 'STX7rUmnpnCp9oZqMQeRKDB7GvXTM9KFvhzbA3AKcabgTBfQZgHZp'], input="test\n")
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ['delkey', '--confirm', 'STX6qGWHsCpmHbphnQbS2yfhvhJXDUVDwnsbnrMZkTqfnkNEZRoLP'], input="test\n")
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ['delkey', '--confirm', 'STX8Wvi74GYzBKgnUmiLvptzvxmPtXfjGPJL8QY3rebecXaxGGQyV'], input="test\n")
        self.assertEqual(result.exit_code, 0)

    def test_orderbook(self):
        runner = CliRunner()
        runner.invoke(cli, ['-o', 'set', 'nodes', self.nodelist.get_nodes()])
        result = runner.invoke(cli, ['orderbook'])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ['orderbook', '--show-date'])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ['orderbook', '--chart'])
        runner.invoke(cli, ['-o', 'set', 'nodes', str(self.nodelist.get_testnet())])
        self.assertEqual(result.exit_code, 0)

    def test_buy(self):
        runner = CliRunner()
        runner.invoke(cli, ['-o', 'set', 'nodes', self.nodelist.get_nodes()])
        result = runner.invoke(cli, ['-d', '-x', 'buy', '1', 'BEX', '2.2'], input="test\n")
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ['-d', '-x', 'buy', '1', 'BEX'], input="y\ntest\n")
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ['-d', '-x', 'buy', '1', 'BBD', '2.2'], input="test\n")
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ['-d', '-x', 'buy', '1', 'BBD'], input="y\ntest\n")
        runner.invoke(cli, ['-o', 'set', 'nodes', str(self.nodelist.get_testnet())])
        self.assertEqual(result.exit_code, 0)

    def test_sell(self):
        runner = CliRunner()
        runner.invoke(cli, ['-o', 'set', 'nodes', self.nodelist.get_nodes()])
        result = runner.invoke(cli, ['-d', '-x', 'sell', '1', 'BEX', '2.2'], input="test\n")
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ['-d', '-x', 'sell', '1', 'BBD', '2.2'], input="test\n")
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ['-d', '-x', 'sell', '1', 'BEX'], input="y\ntest\n")
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ['-d', '-x', 'sell', '1', 'BBD'], input="y\ntest\n")
        runner.invoke(cli, ['-o', 'set', 'nodes', str(self.nodelist.get_testnet())])
        self.assertEqual(result.exit_code, 0)

    def test_cancel(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['-d', 'cancel', '5'], input="test\n")
        self.assertEqual(result.exit_code, 0)

    def test_openorders(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['openorders'])
        self.assertEqual(result.exit_code, 0)

    def test_repost(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['-o', 'repost', '@test/abcde'], input="test\n")
        self.assertEqual(result.exit_code, 0)

    def test_follow_unfollow(self):
        runner = CliRunner()
        runner.invoke(cli, ['-o', 'set', 'nodes', str(self.nodelist.get_testnet())])
        result = runner.invoke(cli, ['-d', 'follow', 'dpaycli1'], input="test\n")
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ['-d', 'unfollow', 'dpaycli1'], input="test\n")
        self.assertEqual(result.exit_code, 0)

    def test_mute_unmute(self):
        runner = CliRunner()
        runner.invoke(cli, ['-o', 'set', 'nodes', str(self.nodelist.get_testnet())])
        result = runner.invoke(cli, ['-d', 'mute', 'dpaycli1'], input="test\n")
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ['-d', 'unfollow', 'dpaycli1'], input="test\n")
        self.assertEqual(result.exit_code, 0)

    def test_witnesscreate(self):
        runner = CliRunner()
        runner.invoke(cli, ['-o', 'set', 'nodes', str(self.nodelist.get_testnet())])
        result = runner.invoke(cli, ['-d', 'witnesscreate', 'dpaycli', pub_key], input="test\n")
        self.assertEqual(result.exit_code, 0)

    def test_witnessupdate(self):
        runner = CliRunner()
        runner.invoke(cli, ['-o', 'set', 'nodes', self.nodelist.get_nodes()])
        result = runner.invoke(cli, ['-o', 'nextnode'])
        runner.invoke(cli, ['-o', 'witnessupdate', 'gtg', '--maximum_block_size', 65000, '--account_creation_fee', 0.1, '--bbd_interest_rate', 0, '--url', 'https://google.de', '--signing_key', wif])
        self.assertEqual(result.exit_code, 0)

    def test_profile(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['setprofile', 'url', 'https://google.de'], input="test\n")
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ['delprofile', 'url'], input="test\n")
        self.assertEqual(result.exit_code, 0)

    def test_claimreward(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['-d', 'claimreward'], input="test\n")
        result = runner.invoke(cli, ['-d', 'claimreward', '--claim_all_dpay'], input="test\n")
        result = runner.invoke(cli, ['-d', 'claimreward', '--claim_all_bbd'], input="test\n")
        result = runner.invoke(cli, ['-d', 'claimreward', '--claim_all_vests'], input="test\n")
        self.assertEqual(result.exit_code, 0)

    def test_power(self):
        runner = CliRunner()
        runner.invoke(cli, ['-o', 'set', 'nodes', self.nodelist.get_nodes()])
        result = runner.invoke(cli, ['power'])
        self.assertEqual(result.exit_code, 0)
        runner.invoke(cli, ['-o', 'set', 'nodes', str(self.nodelist.get_testnet())])

    def test_nextnode(self):
        runner = CliRunner()
        runner.invoke(cli, ['-o', 'set', 'nodes', self.nodelist.get_nodes()])
        result = runner.invoke(cli, ['-o', 'nextnode'])
        self.assertEqual(result.exit_code, 0)
        runner.invoke(cli, ['-o', 'set', 'nodes', str(self.nodelist.get_testnet())])

    def test_pingnode(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['pingnode'])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ['pingnode', '--raw'])
        self.assertEqual(result.exit_code, 0)

    def test_updatenodes(self):
        runner = CliRunner()
        runner.invoke(cli, ['-o', 'set', 'nodes', self.nodelist.get_nodes()])
        result = runner.invoke(cli, ['updatenodes', '--test'])
        self.assertEqual(result.exit_code, 0)
        runner.invoke(cli, ['-o', 'set', 'nodes', str(self.nodelist.get_testnet())])

    def test_currentnode(self):
        runner = CliRunner()
        runner.invoke(cli, ['-o', 'set', 'nodes', self.nodelist.get_nodes()])
        result = runner.invoke(cli, ['currentnode'])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ['currentnode', '--url'])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ['currentnode', '--version'])
        self.assertEqual(result.exit_code, 0)
        runner.invoke(cli, ['-o', 'set', 'nodes', str(self.nodelist.get_testnet())])

    def test_ticker(self):
        runner = CliRunner()
        runner.invoke(cli, ['-o', 'set', 'nodes', self.nodelist.get_nodes()])
        result = runner.invoke(cli, ['ticker'])
        runner.invoke(cli, ['-o', 'set', 'nodes', str(self.nodelist.get_testnet())])
        self.assertEqual(result.exit_code, 0)

    def test_pricehistory(self):
        runner = CliRunner()
        runner.invoke(cli, ['-o', 'set', 'nodes', self.nodelist.get_nodes()])
        result = runner.invoke(cli, ['pricehistory'])
        runner.invoke(cli, ['-o', 'set', 'nodes', str(self.nodelist.get_testnet())])
        self.assertEqual(result.exit_code, 0)

    def test_pending(self):
        runner = CliRunner()
        runner.invoke(cli, ['-o', 'set', 'nodes', self.nodelist.get_nodes()])
        result = runner.invoke(cli, ['pending', 'holger80'])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ['pending', '--post', '--comment', '--curation', 'holger80'])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ['pending', '--post', '--comment', '--curation', '--permlink', '--days', '1', 'holger80'])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ['pending', '--post', '--comment', '--curation', '--author', '--days', '1', 'holger80'])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ['pending', '--post', '--comment', '--curation', '--author', '--title', '--days', '1', 'holger80'])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ['pending', '--post', '--comment', '--curation', '--author', '--permlink', '--length', '30', '--days', '1', 'holger80'])
        self.assertEqual(result.exit_code, 0)
        runner.invoke(cli, ['-o', 'set', 'nodes', str(self.nodelist.get_testnet())])

    def test_rewards(self):
        runner = CliRunner()
        runner.invoke(cli, ['-o', 'set', 'nodes', self.nodelist.get_nodes()])
        result = runner.invoke(cli, ['rewards', 'holger80'])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ['rewards', '--post', '--comment', '--curation', 'holger80'])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ['rewards', '--post', '--comment', '--curation', '--permlink', 'holger80'])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ['rewards', '--post', '--comment', '--curation', '--author', 'holger80'])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ['rewards', '--post', '--comment', '--curation', '--author', '--title', 'holger80'])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ['rewards', '--post', '--comment', '--curation', '--author', '--permlink', '--length', '30', 'holger80'])
        self.assertEqual(result.exit_code, 0)
        runner.invoke(cli, ['-o', 'set', 'nodes', str(self.nodelist.get_testnet())])

    def test_curation(self):
        runner = CliRunner()
        runner.invoke(cli, ['-o', 'set', 'nodes', self.nodelist.get_nodes()])
        result = runner.invoke(cli, ['curation', "@gtg/witness-gtg-log"])
        runner.invoke(cli, ['-o', 'set', 'nodes', str(self.nodelist.get_testnet())])
        self.assertEqual(result.exit_code, 0)

    def test_verify(self):
        runner = CliRunner()
        runner.invoke(cli, ['-o', 'set', 'nodes', self.nodelist.get_nodes(normal=False, appbase=True)])
        result = runner.invoke(cli, ['verify', '--trx', '3', '25304468'])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ['verify', '--trx', '5', '25304468'])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ['verify', '--trx', '0'])
        self.assertEqual(result.exit_code, 0)
        runner.invoke(cli, ['-o', 'set', 'nodes', str(self.nodelist.get_testnet())])
        self.assertEqual(result.exit_code, 0)

    def test_tradehistory(self):
        runner = CliRunner()
        runner.invoke(cli, ['-o', 'set', 'nodes', self.nodelist.get_nodes()])
        result = runner.invoke(cli, ['tradehistory'])
        runner.invoke(cli, ['-o', 'set', 'nodes', str(self.nodelist.get_testnet())])
        self.assertEqual(result.exit_code, 0)
