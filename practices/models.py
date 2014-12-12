# -*- coding: utf-8 -*-
from django.db import models

class Subject(models.Model):
    title = models.CharField(max_length=50)
    field1 = models.CharField(max_length=50)
    field2 = models.CharField(max_length=50)
    field3 = models.CharField(max_length=50)
    field4 = models.CharField(max_length=50)
    def __unicode__(self):
        return self.title

class Axis(models.Model):
    subject = models.ForeignKey('Subject')
    title = models.CharField(max_length=50)
    value1 = models.CharField(max_length=50)
    value2 = models.CharField(max_length=50)
    value3 = models.CharField(max_length=50)
    value4 = models.CharField(max_length=50)
    def __unicode__(self):
        return self.title

class Practice(models.Model):
    subject = models.ForeignKey(Subject)
    title = models.CharField(max_length=50)
    author = models.ForeignKey('auth.User')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    axis1 = models.CharField(max_length=50)
    axis2 = models.CharField(max_length=50)
    field1 = models.CharField(max_length=50)
    field2 = models.CharField(max_length=50)
    field3 = models.CharField(max_length=50)
    field4 = models.CharField(max_length=50)
    def __unicode__(self):
        return self.title

