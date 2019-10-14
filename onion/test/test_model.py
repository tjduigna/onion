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


class TestModel(TestCase):

    def new_data(self, kind='food'):
        return pd.DataFrame(self.d['data'][kind])

    def setUp(self):
        self.d = onion.load_yml(path('mwe.yml'))
        df = self.new_data()
        self.m = onion.Model(df)

    def test_init(self):
        assert self.m.tokens.all()
        assert self.m.tfidf
        assert self.m.corp
        assert self.m.sim
        assert self.m.ref

    def test_init_convert(self):
        onion.Model(self.d['data']['food'])
        with pytest.raises(ValueError):
            onion.Model('')

    def test_init_path(self):
        with pytest.raises(NotImplementedError):
            self.m._init_path('')

    def test_predict(self):
        ret = self.m.predict(self.new_data('cheese'))
        assert not ret.empty

    def test_indexed(self):
        df = self.new_data()
        df['index'] = range(len(df.index))
        m = onion.Model(df)
        ret = m.predict(self.new_data('bread'))
        assert not ret.empty
        assert 'index' in ret.columns
