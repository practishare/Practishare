# -*- coding: utf-8 -*-
from django.forms import ModelForm, ChoiceField
from practices.models import Practice, Comment

class PracticeForm(ModelForm):
    def __init__(self, subject, *args, **kwargs):
        super(PracticeForm, self).__init__(*args, **kwargs)
        axis1 = subject.axis_set.all()[0]
        axis2 = subject.axis_set.all()[1]
        self.fields['axis1'] = ChoiceField(choices=((axis1.value1,axis1.value1), (axis1.value2,axis1.value2), (axis1.value3,axis1.value3), (axis1.value4,axis1.value4)))
        self.fields['axis2'] = ChoiceField(choices=((axis2.value1,axis2.value1), (axis2.value2,axis2.value2), (axis2.value3,axis2.value3), (axis2.value4,axis2.value4)))
    
    class Meta:
        model = Practice
        exclude = ['author', 'subject']

class CommentForm(ModelForm):
     class Meta:
         model = Comment
         fields = ['text']
