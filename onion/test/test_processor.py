# -*- coding: utf-8 -*-
# Copyright 2019, Onion Development Team
# Distributed under the terms of the Apache License 2.0

import os
import string
from functools import partial
from unittest import TestCase

import pytest
import pandas as pd

import onion


path = partial(os.path.join, onion._root, 'static')


class TestProcessor(TestCase):

    def new_data(self, kind='food'):
        return pd.DataFrame(self.d['data'][kind])

    def count_in(self, df, flds):
        cnt = 0
        if isinstance(flds, list):
            for fld in flds:
                for col in df.columns:
                    cnt += df[col].str.contains(fld).sum()
        elif isinstance(flds, dict):
            for old, new in flds.items():
                for col in df.columns:
                    cnt += df[col].str.contains(old).sum()
        return cnt

    def count_not_in(self, df, flds):
        cnt = 0
        if isinstance(flds, list):
           for fld in flds:
               for col in df.columns:
                   cnt += df[col].str.contains(fld).any()
        elif isinstance(flds, dict):
            for old, new in flds.items():
                for col in df.columns:
                    cnt += df[col].str.contains(new.upper()).sum()
                    assert not df[col].str.contains(old.upper()).any()
        return cnt

    def setUp(self):
        self.d = onion.load_yml(path('mwe.yml'))
        self.p = onion.Processor(path('cfg.yml'))

    def test_normalize(self):
        orig = self.new_data()
        test = self.new_data()
        test = self.p.normalize(test)
        assert not orig.applymap(str.isupper).any().any()
        assert test.applymap(str.isupper).all().all()
        # TODO : add assertion about removing punctuation
        # punc = '\\' + '|\\'.join(string.punctuation)

    def test_clear_fields(self):
        flds = self.p.opts['clear_fields']
        test = self.new_data()
        assert self.count_in(test, flds)
        test = self.p.normalize(test)
        test = self.p.clear_fields(test)
        flds = [fld.upper() for fld in flds]
        assert not self.count_not_in(test, flds)

    def test_map_words(self):
        wrds = self.p.opts['map_words']
        test = self.new_data()
        assert self.count_in(test, wrds)
        test = self.p.normalize(test)
        test = self.p.map_words(test)
        assert self.count_not_in(test, wrds)

    def test_stop_words_no_dedupe(self):
        self.p.opts['dedupe'] = False
        wrds = self.p.opts['stop_words']
        test = self.new_data('cheese')
        assert self.count_in(test, wrds)
        test = self.p.normalize(test)
        srs = self.p.combine_columns(test)
        srs = self.p.stop_words(srs)
        for word in wrds:
            assert not srs.str.contains(word).any()

    def test_stop_words_dedupe(self):
        self.p.opts['dedupe'] = True
        wrds = self.p.opts['stop_words']
        test = self.new_data('cheese')
        assert self.count_in(test, wrds)
        test = self.p.normalize(test)
        srs = self.p.combine_columns(test)
        srs = self.p.stop_words(srs)
        for word in wrds:
            assert not srs.str.contains(word).any()

    def test_tokenize(self):
        test = self.new_data()
        ret = self.p.tokenize(test)

    def test_init_cfg(self):
        r = self.p._init_cfg({})
        assert isinstance(r, dict)
        r = self.p._init_cfg(path('cfg.yml'))
        assert r == self.p.opts
        r = self.p._init_cfg(None)
        assert isinstance(r, dict)
        with pytest.raises(Exception):
            self.p._init_cfg([])

