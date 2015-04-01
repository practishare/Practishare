# -*- coding: utf-8 -*-
from django import forms
from practices.models import *
from django.forms.models import inlineformset_factory

class PracticeForm(forms.ModelForm):
    class Meta:
        model = Practice
        exclude = ['author', 'subject']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class AxisForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AxisForm, self).__init__(*args, **kwargs)
        self.fields['axis'].widget = forms.HiddenInput()
        if kwargs.has_key('initial'):
            axisid = kwargs['initial']['axis']
            self.fields['value'] = forms.ModelChoiceField(queryset=AxisValue.objects.filter(axis=axisid), label=Axis.objects.get(pk=axisid).title)

class FieldForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FieldForm, self).__init__(*args, **kwargs)
        self.fields['field'].widget = forms.HiddenInput()
        if kwargs.has_key('initial'):
            fieldid = kwargs['initial']['field']
            self.fields['value'] = forms.CharField(label=Field.objects.get(pk=fieldid).name)

def getInlines(subject, data=None, practice=None):
    """Generates formsets for the practice, depending on the subject"""
    axis_list = map(lambda a: {'axis': a.id}, subject.axis_set.all())
    field_list = map(lambda f: {'field': f.id}, subject.field_set.all())
##TODO: set extra and get axis in form init for label
    AxisFormSet = inlineformset_factory(Practice, PracticeAxisValue, can_delete=False, form=AxisForm, extra=0)#len(axis_list))
    FieldFormSet = inlineformset_factory(Practice, PracticeFieldValue, can_delete=False, form=FieldForm, extra=0)#len(field_list))
    
    return [AxisFormSet(data, initial=axis_list, instance=practice), FieldFormSet(data, initial=field_list, instance=practice)]
