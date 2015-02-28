# -*- coding: utf-8 -*-
import uuid
from django.db import models

class Subject(models.Model):
    id = models.CharField(primary_key=True, max_length=32)
    title = models.CharField(max_length=50)
    field1 = models.CharField(max_length=50)
    field2 = models.CharField(max_length=50)
    field3 = models.CharField(max_length=50)
    field4 = models.CharField(max_length=50)
    public = models .BooleanField(default=True)
    def save(self, *args, **kwargs):
        if self.id is None:
            self.id = uuid.uuid4().hex
            while Subject.objects.filter(id=self.id):
                self.id = uuid.uuid4().hex
        super(Subject, self).save(*args, **kwargs)
    
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
    field1 = models.TextField(blank=True)
    field2 = models.TextField(blank=True)
    field3 = models.TextField(blank=True)
    field4 = models.TextField(blank=True)
    url = models.URLField(blank=True, null=True)
    def __unicode__(self):
        return self.title

class Comment(models.Model):
    text = models.TextField()
    date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey('auth.User')
    practice = models.ForeignKey(Practice)
