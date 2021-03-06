# This Python file uses the following encoding: utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import next
import re
import time
import math
import json
from dpaycli.instance import shared_dpay_instance
from dpaycli.account import Account
import logging
log = logging.getLogger(__name__)


class NodeList(list):
    """ Returns a node list

        .. code-block:: python

            from dpaycli.nodelist import NodeList
            n = NodeList()
            nodes_urls = n.get_nodes()

    """
    def __init__(self):
        nodes = [
            {
                "url": "https://greatchain.dpaynodes.com",
                "version": "0.20.5",
                "type": "appbase",
                "owner": "dpay",
                "score": 100
            }]
        super(NodeList, self).__init__(nodes)

    def update_nodes(self, weights=None, dpay_instance=None):
        """ Reads metadata from fullnodeupdate and recalculates the nodes score

            :params list/dict weight: can be used to weight the different benchmarks

            .. code-block:: python
                from dpaycli.nodelist import NodeList
                nl = NodeList()
                weights = [0, 0.1, 0.2, 1]
                nl.update_nodes(weights)
                weights = {'block': 0.1, 'history': 0.1, 'apicall': 1, 'config': 1}
                nl.update_nodes(weights)
        """
        dpay = dpay_instance or shared_dpay_instance()
        metadata = None
        account = None
        cnt = 0
        while metadata is None and cnt < 5:
            cnt += 1
            try:
                account = Account("fullnodeupdate", dpay_instance=dpay)
                metadata = json.loads(account["json_metadata"])
            except:
                dpay.rpc.next()
                account = None
                metadata = None
        if metadata is None:
            return
        report = metadata["report"]
        failing_nodes = metadata["failing_nodes"]
        parameter = metadata["parameter"]
        benchmarks = parameter["benchmarks"]
        if weights is None:
            weights_dict = {}
            for benchmark in benchmarks:
                weights_dict[benchmark] = (1. / len(benchmarks))
        elif isinstance(weights, list):
            weights_dict = {}
            i = 0
            weight_sum = 0
            for w in weights:
                weight_sum += w
            for benchmark in benchmarks:
                if i < len(weights):
                    weights_dict[benchmark] = weights[i] / weight_sum
                else:
                    weights_dict[benchmark] = 0.
                i += 1
        elif isinstance(weights, dict):
            weights_dict = {}
            i = 0
            weight_sum = 0
            for w in weights:
                weight_sum += weights[w]
            for benchmark in benchmarks:
                if benchmark in weights:
                    weights_dict[benchmark] = weights[benchmark] / weight_sum
                else:
                    weights_dict[benchmark] = 0.

        max_score = len(report) + 1
        new_nodes = []
        for node in self:
            new_node = node.copy()
            for report_node in report:
                if node["url"] == report_node["node"]:
                    new_node["version"] = report_node["version"]
                    scores = []
                    for benchmark in benchmarks:
                        result = report_node[benchmark]
                        rank = result["rank"]
                        if not result["ok"]:
                            rank = max_score + 1
                        score = (max_score - rank) / (max_score - 1) * 100
                        weighted_score = score * weights_dict[benchmark]
                        scores.append(weighted_score)
                    sum_score = 0
                    for score in scores:
                        sum_score += score
                    new_node["score"] = sum_score
            for node_failing in failing_nodes:
                if node["url"] == node_failing:
                    new_node["score"] = -1
            new_nodes.append(new_node)
        super(NodeList, self).__init__(new_nodes)

    def get_nodes(self, normal=True, appbase=True, dev=False, testnet=False, testnetdev=False, wss=True, https=True, not_working=False):
        """ Returns nodes as list

            :param bool normal: when True, nodes with version 0.19.5 are included
            :param bool appbase: when True, nodes with version 0.19.11 are included
            :param bool dev: when True, dev nodes with version 0.19.11 are included
            :param bool testnet: when True, testnet nodes are included
            :param bool testnetdev: When True, testnet-dev nodes are included
            :param bool not_working: When True, all nodes including not working ones will be returned

        """
        node_list = []
        node_type_list = []
        if normal:
            node_type_list.append("normal")
        if appbase:
            node_type_list.append("appbase")
        if dev:
            node_type_list.append("appbase-dev")
        if testnet:
            node_type_list.append("testnet")
        if testnetdev:
            node_type_list.append("testnet-dev")
        for node in self:
            if node["type"] in node_type_list and (node["score"] >= 0 or not_working):
                if not https and node["url"][:5] == 'https':
                    continue
                if not wss and node["url"][:3] == 'wss':
                    continue
                node_list.append(node)

        return [node["url"] for node in sorted(node_list, key=lambda self: self['score'], reverse=True)]

    def get_testnet(self, testnet=True, testnetdev=False):
        """Returns testnet nodes"""
        return self.get_nodes(normal=False, appbase=False, testnet=testnet, testnetdev=testnetdev)
