from django import forms
from django.forms import ModelForm
from .models import SurveyQuestion

class SurveyForm(forms.Form):
    CHOICES=[('option1','1'),
            ('option2','2'),
            ('option3','3'),
            ('option4','4'),
            ('option5','5'),]

    score = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, required=False)

class QuestionForm(ModelForm):
        class Meta:
            model = SurveyQuestion
            fields = ['question']