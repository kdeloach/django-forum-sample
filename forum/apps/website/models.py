# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Topic(models.Model):
    title = models.CharField(max_length=120)
    body = models.TextField()


class Comment(models.Model):
    body = models.TextField()
    topic = models.ForeignKey(Topic, related_name='comments')
