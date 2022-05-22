from django.contrib import admin

from survey.models import SurveyQuestion
from .models import Week,SurveyQuestion

# Register your models here.
admin.site.register(Week)
admin.site.register(SurveyQuestion)