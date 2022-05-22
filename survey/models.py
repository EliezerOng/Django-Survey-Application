from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator

# Create your models here.
class Week(models.Model):

    week_number = models.IntegerField(primary_key=True,default=1,
                                    validators=[MinValueValidator(1),MaxValueValidator(13)])
    
    def __str__(self):
        return str(self.week_number)

class SurveyQuestion(models.Model):

    question = models.CharField(max_length=200)
    week = models.ForeignKey('Week',db_column='week_number', on_delete=models.CASCADE, default=1)
    total_responses = models.IntegerField(default=0)
    total_score = models.IntegerField(default=0)
    average_score = models.FloatField(default=0)

    def __str__(self):
        return f"Week: {self.week}, Question: {self.question}, Total Responses: {self.total_responses}, Total Score: {self.total_score}, Average Score: {self.average_score}" 

