# This Python file uses the following encoding: utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import unittest
import json
from dpaycligraphenebase import objects
from dpaycligraphenebase import types
from dpaycli.amount import Amount
from dpaycli import DPay


class Testcases(unittest.TestCase):
    def test_GrapheneObject(self):
        j = {"a": 2, "b": "abcde", "c": ["a", "b"]}
        j2 = objects.GrapheneObject(j)
        self.assertEqual(j, j2.data)
        self.assertEqual(json.loads(j2.__str__()), j2.json())

        a = objects.Array(['1000', 3, '@@000000013'])
        j = {"a": a}
        j2 = objects.GrapheneObject(j)
        self.assertEqual(j, j2.data)
        self.assertEqual(json.loads(j2.__str__()), j2.json())

        a = types.Array(['1000', 3, '@@000000013'])
        j = {"a": a}
        j2 = objects.GrapheneObject(j)
        self.assertEqual(j, j2.data)
        self.assertEqual(json.loads(j2.__str__()), j2.json())
