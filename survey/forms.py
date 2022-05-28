from django import forms
from django.forms import ModelForm
from .models import SurveyQuestion
from crispy_forms.bootstrap import InlineRadios
from crispy_forms.layout import Div,Layout
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class SurveyForm(forms.Form):
    CHOICES=[('option1','1'),
            ('option2','2'),
            ('option3','3'),
            ('option4','4'),
            ('option5','5'),]

    score = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, required=False)
    #Div(InlineRadios('score'), css_class="col-md-3")
    def __init__(self, *args, **kwargs):
        super(SurveyForm,self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            InlineRadios('score' , id='inlineRadio')
        )
        
        self.helper.form_tag = False


class QuestionForm(ModelForm):
        class Meta:
            model = SurveyQuestion
            fields = ['question']