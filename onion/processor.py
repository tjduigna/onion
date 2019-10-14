# -*- coding: utf-8 -*-
# Copyright 2019, Onion Development Team
# Distributed under the terms of the Apache License 2.0

import os
import string

import nltk
from nltk.tokenize import word_tokenize

import onion

nltk.data.path.insert(0, os.path.join(onion._root, 'static'))


class Processor:
    """Configuration driven word pre-processing
    methods
    """

    def normalize(self, df):
        """Iterate over columns of a dataframe
        and convert to upper case as well as
        replace all puncuation with blank spaces.

        Args:
            df (pd.DataFrame): the data
        """
        punc = '\\' + '|\\'.join(string.punctuation)
        for col in df.columns:
            df[col] = df[col].astype(str).str.upper()
            df[col] = df[col].str.replace(punc, ' ').str.strip()
        return df

    def clear_fields(self, df):
        """Remove entries containing substrings"""
        # TODO : provide optional run-time args
        # Remove individual fields from a Series based
        # on presence of a sub-string within that field.
        clear_fields = self.opts.get('clear_fields', [])
        if clear_fields:
            for col in df.columns:
                for field in clear_fields:
                    idx = df[col].str.contains(field.upper(), na=False)
                    df.loc[idx, col] = ''
                    df[col] = df[col].fillna('')
        return df

    def map_words(self, df):
        """Replace instances of one set of words with
        another set of words as determined by the map_words
        configuration parameter.

        Args:
            df (pd.DataFrame): the data
        """
        # TODO : provide optional run-time args
        # Updates keys to values in individual fields
        map_words = self.opts.get('map_words', {})
        if map_words:
            for col in df.columns:
                for old, new in map_words.items():
                    old = r'\b{}\b'.format(old.upper())
                    df[col] = df[col].str.replace(old, new.upper())
        return df

    def stop_words(self, srs):
        """Removes pre-defined stop words from
        being allowed to enter a corpus.
        """
        # Only allow single entries of words
        if self.opts.get('dedupe', False):
            def remove(lst, args):
                return list(set(lst).difference(args))
        else:
            def remove(lst, args):
                for arg in args:
                    try: lst.remove(arg)
                    except ValueError: pass
                return lst
        words = self.opts.get('stop_words', [])
        words = [word.upper() for word in words]
        return srs.apply(remove, args=(words,))

    def combine_columns(self, df):
        """Combine all columns in the dataset into a
        single series of lists, after being put through
        nltk's word_tokenize.
        """
        anc, *chn = df.columns
        kws = {'sep': ' ', 'na_rep': ' '}
        return df[anc].str.cat(others=df[chn], **kws
                              ).apply(word_tokenize)

    def tokenize(self, df):
        """Apply some preprocessing to the data before
        building a model against it. Preprocessing is
        determined by configuration parameters stored
        in yaml files.
        
        Args:
            df (pd.DataFrame): the data

        Returns:
            srs (pre-processed)
        """
        df = self.normalize(df)
        df = self.clear_fields(df)
        df = self.map_words(df)
        srs = self.combine_columns(df)
        return self.stop_words(srs)

    def _init_cfg(self, cfg):
        """Handle different forms of config"""
        if cfg is None:
            return {}
        if isinstance(cfg, str):
            return onion.load_yml(cfg)
        if isinstance(cfg, dict):
            return cfg
        raise Exception(f"cfg type '{type(cfg)}' not understood")

    def __init__(self, cfg):
        self.opts = self._init_cfg(cfg)
