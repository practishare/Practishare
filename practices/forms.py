from django.forms import ModelForm
from practices.models import Practice

class PracticeForm(ModelForm):
    class Meta:
        model = Practice
        exclude = ['author']
