# -*- coding: utf-8 -*-
# Copyright 2019, Greatery Development Team
# Distributed under the terms of the Apache License 2.0

from tortoise.models import Model
from tortoise import fields

class Tweet(Model):
    pk = 'id'
    ui = ['id', 'tweet']
    id = fields.IntField(pk=True)
    tweet = fields.TextField()

    def __str__(self):
        return f"{self.tweet}"
