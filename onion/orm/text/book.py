# -*- coding: utf-8 -*-
# Copyright 2019, Greatery Development Team
# Distributed under the terms of the Apache License 2.0

from tortoise.models import Model
from tortoise import fields

class Book(Model):
    pk = 'id'
    ui = ['id', 'sentence']
    id = fields.IntField(pk=True)
    sentence = fields.TextField()

    def __str__(self):
        cnt = len(self.sentence)
        if cnt > 33:
            return f"{self.sentence[:30]}..."
        return f"{self.sentence}"
