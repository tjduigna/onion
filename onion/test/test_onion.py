# -*- coding: utf-8 -*-
# Copyright 2019, Onion Development Team
# Distributed under the terms of the Apache License 2.0

import os
from functools import partial
from unittest import TestCase

import pytest
import pandas as pd

import onion


path = partial(os.path.join, onion._root, 'static')


class TestOnion(TestCase):

#    def setUp(self):
#        g = onion.load_yml(path('mwe.yml'))
#        self.primary = g.pop('primary')
        #self.graph = g.pop('graph')
        #self.data = {
        #    key: pd.DataFrame.from_dict(val)
        #    for key, val in g.pop('data').items()
        #}
        #self.onion = onion.Onion.from_fp(path('mwe.yml'))

    #def test_init(self):
    #    onion.Onion(self.primary, self.graph, self.data)

    def test_load_yml(self):
        r = onion.load_yml('fldsntexist')
        assert not r
        r = onion.load_yml(path('mwe.yml'), cache=True)
        assert r
        n = onion.load_yml(path('mwe.yml'), cache=True)
        assert r is n

    def test_init(self):
        onion.Onion.from_file(path('mwe.yml'),
                              cfg=path('cfg.yml'))
