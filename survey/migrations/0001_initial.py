# Generated by Django 4.0 on 2022-05-23 11:59

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Week',
            fields=[
                ('week_number', models.IntegerField(default=1, primary_key=True, serialize=False, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(13)])),
            ],
        ),
        migrations.CreateModel(
            name='SurveyQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('total_responses', models.IntegerField(default=0)),
                ('total_score', models.IntegerField(default=0)),
                ('average_score', models.FloatField(default=0)),
                ('option_1_count', models.IntegerField(default=0)),
                ('option_2_count', models.IntegerField(default=0)),
                ('option_3_count', models.IntegerField(default=0)),
                ('option_4_count', models.IntegerField(default=0)),
                ('option_5_count', models.IntegerField(default=0)),
                ('week', models.ForeignKey(db_column='week_number', default=1, on_delete=django.db.models.deletion.CASCADE, to='survey.week')),
            ],
        ),
    ]
