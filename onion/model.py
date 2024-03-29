# -*- coding: utf-8 -*-
# Copyright 2019, Onion Development Team
# Distributed under the terms of the Apache License 2.0

import os
import numpy as np
import pandas as pd

from gensim.corpora import Dictionary
from gensim.models import TfidfModel
from gensim.similarities import Similarity

import onion
from onion.processor import Processor


class Model(Processor):
    """Encapsulate a gensim similarity
    model for use in an onion.
    """

    def predict(self, entities):
        """Evaluate entities against the similarity
        model.

        Args:
            entities (pd.DataFrame): data
        """
        entities = self._to_df(entities)
        s = self.tokenize(entities)
        bow = s.apply(self.ref.doc2bow)
        tfs = bow.apply(self.tfidf.__getitem__)
        ans = tfs.apply(self.sim.__getitem__)
        idxs = np.stack((-ans).apply(np.ndarray.argsort))
        ans = np.stack(ans)
        d0 = np.repeat(range(idxs.shape[0]), idxs.shape[1])
        s0 = pd.Series(d0)
        d1  = idxs.flatten()
        s1 = pd.Series(d1)
        ret = pd.DataFrame.from_dict({
            'id': range(len(d0)),
            'sample': d0,
            'guess': s0.map(s).apply(' '.join),
            'conf': ans[(d0, d1)],
            'check': s1.map(dict(enumerate(self.tokens))).apply(' '.join),
        })
        if self.index is not None:
            ret['index'] = s1.map(dict(enumerate(self.index)))
        return ret

    def _to_df(self, df):
        if not isinstance(df, pd.DataFrame):
            try:
                df = pd.DataFrame(df)
            except ValueError:
                raise
        return df

    def __init__(self, df, cfg=None, path=None, idx_col='index'):
        """Builds a gensim model and exposes a convenient
        pandas-centric API with a top level predict method
        that accepts a dataframe and returns a dataframe.

        Args:
            df (pd.DataFrame): the data
            cfg (str,dict): configuration for Processor
            path (str): location for model saving
        """
        df = self._to_df(df)
        super().__init__(cfg)
        self.path = self._init_path(path)
        self.index = None
        print(idx_col, df.columns)
        if idx_col in df.columns:
            self.index = df.pop('index')

        self.tokens = self.tokenize(df)
        self.ref = Dictionary(self.tokens)
        self.corp = [self.ref.doc2bow(tok) for tok in self.tokens]
        self.tfidf = TfidfModel(self.corp)
        self.sim = Similarity(self.path, self.corp, len(self.ref))

    def _init_path(self, path):
        """Handle different types for path"""
        if path is None:
            return os.path.join(onion._base)
        raise NotImplementedError("support path args")
