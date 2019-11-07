# -*- coding: utf-8 -*-
# Copyright 2019, Onion Development Team
# Distributed under the terms of the Apache License 2.0

import os
import yaml
import logging.config


_cfg = {}
_root = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(_root, 'conf', 'log.yml'), 'r') as f:
    logging.config.dictConfig(yaml.safe_load(f.read()))
_home = os.path.expanduser('~')
_base = os.path.join(_home, '.onion')
_log = logging.getLogger(__name__)
_log.setLevel(logging.DEBUG)


if not os.path.isdir(_base): os.makedirs(_base)


class Log:

    @property
    def log(self):
        return logging.getLogger(
            '.'.join([
                self.__module__,
                self.__class__.__name__
            ])
        )


def load_yml(abspath, cache=False):
    """Load a yml file and optionally cache
    it into a package level cache.

    Args:
        abspath (str): path to yml file
        cache (bool): if True, don't re-parse
                      if called again
    """
    r = {}
    if cache:
        r = _cfg.get(abspath, {})
        if r:
            return r
    try:
        with open(abspath, 'r') as f:
            # _cfg[abspath] = 
            r = yaml.safe_load(f.read())
    except FileNotFoundError as e:
        _log.error(f"file not found: {abspath}")
    if cache:
        _cfg[abspath] = r
    return r


from onion.processor import Processor
from onion.model import Model
from onion.onion import Onion
from onion import orm
