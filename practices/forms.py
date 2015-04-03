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
        elif kwargs.has_key('instance'):
            axisid = kwargs['instance'].axis.id
        self.fields['value'] = forms.ModelChoiceField(queryset=AxisValue.objects.filter(axis=axisid), label=Axis.objects.get(pk=axisid).title)
        self.fields['value'].widget.attrs={ 'required': 'true' }

class FieldForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FieldForm, self).__init__(*args, **kwargs)
        self.fields['field'].widget = forms.HiddenInput()
        if kwargs.has_key('initial'):
            fieldid = kwargs['initial']['field']
        elif kwargs.has_key('instance'):
            fieldid = kwargs['instance'].field.id
        self.fields['value'] = forms.CharField(label=Field.objects.get(pk=fieldid).name)

def getInlines(subject, data=None, practice=None):
    """Generates formsets for the practice, depending on the subject"""
    axis_list = map(lambda a: {'axis': a.id}, subject.axis_set.exclude(practiceaxisvalue__practice=practice))
    field_list = map(lambda f: {'field': f.id}, subject.field_set.exclude(practicefieldvalue__practice=practice))
    axis_nb = len(map(lambda a: {'axis': a.id}, subject.axis_set.all()))
    field_nb = len(map(lambda f: {'field': f.id}, subject.field_set.all()))
    AxisFormSet = inlineformset_factory(Practice, PracticeAxisValue, can_delete=False, form=AxisForm, extra=len(axis_list), max_num=axis_nb)
    FieldFormSet = inlineformset_factory(Practice, PracticeFieldValue, can_delete=False, form=FieldForm, extra=len(field_list), max_num=field_nb)
    
    return [AxisFormSet(data, initial=axis_list, instance=practice), FieldFormSet(data, initial=field_list, instance=practice)]
