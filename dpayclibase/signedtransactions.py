from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import int, str
from dpaycligraphenebase.signedtransactions import Signed_Transaction as GrapheneSigned_Transaction
from .operations import Operation
from dpaycligraphenebase.chains import known_chains
import logging
log = logging.getLogger(__name__)


class Signed_Transaction(GrapheneSigned_Transaction):
    """ Create a signed transaction and offer method to create the
        signature

        :param num refNum: parameter ref_block_num (see ``getBlockParams``)
        :param num refPrefix: parameter ref_block_prefix (see ``getBlockParams``)
        :param str expiration: expiration date
        :param Array operations:  array of operations
        :param dict custom_chains: custom chain which should be added to the known chains
    """
    def __init__(self, *args, **kwargs):
        self.known_chains = known_chains
        custom_chain = kwargs.get("custom_chains", {})
        if len(custom_chain) > 0:
            for c in custom_chain:
                if c not in self.known_chains:
                    self.known_chains[c] = custom_chain[c]
        super(Signed_Transaction, self).__init__(*args, **kwargs)

    def add_custom_chains(self, custom_chain):
        if len(custom_chain) > 0:
            for c in custom_chain:
                if c not in self.known_chains:
                    self.known_chains[c] = custom_chain[c]

    def sign(self, wifkeys, chain=u"BEX"):
        return super(Signed_Transaction, self).sign(wifkeys, chain)

    def verify(self, pubkeys=[], chain=u"BEX", recover_parameter=False):
        return super(Signed_Transaction, self).verify(pubkeys, chain, recover_parameter)

    def getOperationKlass(self):
        return Operation

    def getKnownChains(self):
        return self.known_chains
