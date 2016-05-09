# -*- coding: utf-8 -*-
import uuid
from django.db import models

class Subject(models.Model):
    id = models.CharField(primary_key=True, max_length=32)
    title = models.CharField(max_length=50, verbose_name=u"Titre")
    public = models .BooleanField(default=True)
    author = models.ForeignKey('auth.User', default=1, verbose_name=u"Auteur") 
    def save(self, *args, **kwargs):
        if not self.id:
            self.id = uuid.uuid4().hex
            while Subject.objects.filter(id=self.id):
                self.id = uuid.uuid4().hex
        super(Subject, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return self.title

class Field(models.Model):
    subject = models.ForeignKey('Subject', verbose_name=u"Sujet")
    name = models.CharField(max_length=50, verbose_name=u"Nom")
    def __unicode__(self):
        return self.name

class Axis(models.Model):
    subject = models.ForeignKey('Subject', verbose_name=u"Titre")
    title = models.CharField(max_length=50, verbose_name=u"Titre")
    def __unicode__(self):
        return self.title

class AxisValue(models.Model):
    axis = models.ForeignKey('Axis', verbose_name=u"Axes")
    name = models.CharField(max_length=50, verbose_name=u"Valeur")
    def __unicode__(self):
        return self.name

class Practice(models.Model):
    subject = models.ForeignKey(Subject, verbose_name=u"Sujet")
    title = models.CharField(max_length=50, verbose_name=u"Titre")
    author = models.ForeignKey('auth.User', verbose_name=u"Auteur")
    created = models.DateTimeField(auto_now_add=True, verbose_name=u"Crée")
    updated = models.DateTimeField(auto_now=True, verbose_name=u"Mis à jour")
    url = models.URLField(blank=True, null=True)
    def __unicode__(self):
        return self.title

class PracticeFieldValue(models.Model):
    practice = models.ForeignKey(Practice)
    field = models.ForeignKey(Field)
    value = models.TextField(blank=True)
    class Meta:
        unique_together = (("practice", "field"),)

class PracticeAxisValue(models.Model):
    practice = models.ForeignKey(Practice)
    axis = models.ForeignKey(Axis)
    value = models.ForeignKey(AxisValue)
    class Meta:
        unique_together = (("practice", "axis"),)

class Comment(models.Model):
    text = models.TextField()
    date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey('auth.User')
    practice = models.ForeignKey(Practice)
