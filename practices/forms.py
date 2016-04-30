# -*- coding: utf-8 -*-
from django import forms
from practices.models import *

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
