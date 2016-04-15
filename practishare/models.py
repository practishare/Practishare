# coding: utf8
from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse_lazy
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify

class User(AbstractUser):
    title       = models.CharField(max_length=100, blank=True, verbose_name=u"Civilité", default="M")
    lastname    = models.CharField(max_length=100, blank=True, verbose_name=u"Nom")
    firstname   = models.CharField(max_length=100, blank=True, verbose_name=u"Prénom")
    readonly    = models.BooleanField(default=False, verbose_name=u"Invité")
    
    def get_absolute_url(self):
        return reverse_lazy("user_edit", args=(self.username,))
    def get_full_name(self):
        return ("%s %s"%(self.firstname, self.lastname)).strip() or self.username
    def __unicode__(self):
        return self.get_full_name()
    def get_duplicates(self):
        return User.objects.filter(lastname__icontains=self.lastname, firstname__icontains=self.firstname, city=self.city).exclude(pk=self.pk)

@receiver(pre_save, sender=User)
def user_presave(sender, instance, *args, **kwargs):
    """signal handler to generate usernames, avoiding duplicates"""
    if not instance.username:
        instance.username = slugify(instance.lastname)[:20]
        while User.objects.filter(username=instance.username).exists():
            homonyms = User.objects.filter(username__startswith=instance.username+"-") #users with same name
            counter = max([0]+ map(lambda u: get_slugnb(u.username), homonyms)) + 1 #max counter in username
            instance.username = '%s-%d' % (slugify(instance.lastname)[:20], counter)
@receiver(post_save, sender=User)
def user_postsave(sender, instance, *args, **kwargs):
    """signal handler to ensure user has a primary group"""
    if not instance.membership_set.filter(primary=True).exists():
        primary = instance.membership_set.order_by('since').first()
        if primary:
            primary.primary = True
            primary.save()