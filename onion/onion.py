# -*- coding: utf-8 -*-
# Copyright 2019, Onion Development Team
# Distributed under the terms of the Apache License 2.0

import os
import pandas as pd

import onion
from onion.model import Model


class Onion:
    """Heirarchical architecture for some
    NLP models provided by gensim. Assumes
    complex input data structures.

    Args:
        graph (dict): {outer: [inter1, inter2],
                       inter1: [inner1, inner2],
                       inter2: [inner3, inner4]}
        data (dict): same key structure as graph,
                     values containing dataframes
    """

    @classmethod
    def from_file(cls, arch, data=None, cfg=None, path=None):
        """Loads an onion architecture from a yml
        file. Data can be specified in the yml as
        well or provided directly.

        Args:
            arch (str): path to yml with architecture
            data (dict): data for models (must conform
                         to the architecture in yml)
            cfg (str,dict): processor config
            path (str): path to model storage location

        Returns:
            Onion container of models
        """
        arch = onion.load_yml(arch)
        graph = arch.pop('graph')
        return cls(primary=graph.pop('primary'),
                   graph=graph, data=arch.pop('data'),
                   cfg=cfg)

    def init_model(self, df, cfg=None, path=None):
        """Create a new onion Model from a dataframe.

        Args:
            df (pd.DataFrame): the data
            cfg (str,dict): processor config
            path (str): path to model storage location
        """
        cfg = cfg or self._cfg
        path = path or self._path
        return Model(df, cfg=cfg, path=path)

    def _init_models(self):
        """Run through the graph and the provided data
        and generate some models for each concept in
        both (for now).
        """
        # Dummy models on the architecture
        prim = self._graph.pop(self._primary)
        self._graph_models[self._primary] = self.init_model(prim)
        for key, vals in self._graph.items():
            self._graph_models[key] = self.init_model(vals)
        self._graph[self._primary] = prim
        # The actual models on real data
        if self._data is None:
            return
        prim = self._data.pop(self._primary)
        self._models[self._primary] = self.init_model(prim)
        for key, vals in self._data.items():
            self._models[key] = self.init_model(vals)
        self._data[self._primary] = prim

    def __init__(self, primary, graph, data, cfg=None, path=None):
        # TODO : simplify constructor
        self._order = []
        self._graph = graph
        self._data = data
        self._graph_models = {}
        self._models = {}
        self._primary = primary
        self._cfg = cfg
        self._path = path
        self._init_models()
