from __future__ import print_function
import sys
from datetime import timedelta
import time
import io
from dpaycli import DPay
from dpaycli.account import Account
from dpaycli.amount import Amount
from dpaycli.utils import parse_time
from dpay.account import Account as dpayAccount
from dpay.post import Post as dpayPost
from dpay import DPay as dpayDPay
import logging
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":
    stm = DPay("https://api.dpays.io")
    dpaycli_acc = Account("whitehorse", dpay_instance=stm)
    stm2 = dpayDPay(nodes=["https://api.dpays.io"])
    dpay_acc = dpayAccount("whitehorse", dpayd_instance=stm2)

    # profile
    print("dpaycli_acc.profile  {}".format(dpaycli_acc.profile))
    print("dpay_acc.profile {}".format(dpay_acc.profile))
    # bp
    print("dpaycli_acc.bp  {}".format(dpaycli_acc.bp))
    print("dpay_acc.bp {}".format(dpay_acc.bp))
    # rep
    print("dpaycli_acc.rep  {}".format(dpaycli_acc.rep))
    print("dpay_acc.rep {}".format(dpay_acc.rep))
    # balances
    print("dpaycli_acc.balances  {}".format(dpaycli_acc.balances))
    print("dpay_acc.balances {}".format(dpay_acc.balances))
    # get_balances()
    print("dpaycli_acc.get_balances()  {}".format(dpaycli_acc.get_balances()))
    print("dpay_acc.get_balances() {}".format(dpay_acc.get_balances()))
    # reputation()
    print("dpaycli_acc.get_reputation()  {}".format(dpaycli_acc.get_reputation()))
    print("dpay_acc.reputation() {}".format(dpay_acc.reputation()))
    # voting_power()
    print("dpaycli_acc.get_voting_power()  {}".format(dpaycli_acc.get_voting_power()))
    print("dpay_acc.voting_power() {}".format(dpay_acc.voting_power()))
    # get_followers()
    print("dpaycli_acc.get_followers()  {}".format(dpaycli_acc.get_followers()))
    print("dpay_acc.get_followers() {}".format(dpay_acc.get_followers()))
    # get_following()
    print("dpaycli_acc.get_following()  {}".format(dpaycli_acc.get_following()))
    print("dpay_acc.get_following() {}".format(dpay_acc.get_following()))
    # has_voted()
    print("dpaycli_acc.has_voted()  {}".format(dpaycli_acc.has_voted("@holger80/api-methods-list-for-appbase")))
    print("dpay_acc.has_voted() {}".format(dpay_acc.has_voted(dpayPost("@holger80/api-methods-list-for-appbase"))))
    # curation_stats()
    print("dpaycli_acc.curation_stats()  {}".format(dpaycli_acc.curation_stats()))
    print("dpay_acc.curation_stats() {}".format(dpay_acc.curation_stats()))
    # virtual_op_count
    print("dpaycli_acc.virtual_op_count()  {}".format(dpaycli_acc.virtual_op_count()))
    print("dpay_acc.virtual_op_count() {}".format(dpay_acc.virtual_op_count()))
    # get_account_votes
    print("dpaycli_acc.get_account_votes()  {}".format(dpaycli_acc.get_account_votes()))
    print("dpay_acc.get_account_votes() {}".format(dpay_acc.get_account_votes()))
    # get_withdraw_routes
    print("dpaycli_acc.get_withdraw_routes()  {}".format(dpaycli_acc.get_withdraw_routes()))
    print("dpay_acc.get_withdraw_routes() {}".format(dpay_acc.get_withdraw_routes()))
    # get_conversion_requests
    print("dpaycli_acc.get_conversion_requests()  {}".format(dpaycli_acc.get_conversion_requests()))
    print("dpay_acc.get_conversion_requests() {}".format(dpay_acc.get_conversion_requests()))
    # export
    # history
    dpaycli_hist = []
    for h in dpaycli_acc.history(only_ops=["transfer"]):
        dpaycli_hist.append(h)
        if len(dpaycli_hist) >= 10:
            break
    dpay_hist = []
    for h in dpay_acc.history(filter_by="transfer", start=0):
        dpay_hist.append(h)
        if len(dpay_hist) >= 10:
            break
    print("dpaycli_acc.history()  {}".format(dpaycli_hist))
    print("dpay_acc.history() {}".format(dpay_hist))
    # history_reverse
    dpaycli_hist = []
    for h in dpaycli_acc.history_reverse(only_ops=["transfer"]):
        dpaycli_hist.append(h)
        if len(dpaycli_hist) >= 10:
            break
    dpay_hist = []
    for h in dpay_acc.history_reverse(filter_by="transfer"):
        dpay_hist.append(h)
        if len(dpay_hist) >= 10:
            break
    print("dpaycli_acc.history_reverse()  {}".format(dpaycli_hist))
    print("dpay_acc.history_reverse() {}".format(dpay_hist))
