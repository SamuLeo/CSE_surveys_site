# Generated by Django 3.0.3 on 2020-02-13 17:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransplantType',
            fields=[
                ('value', models.CharField(max_length=50, primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': 'Type Of Transplant',
                'verbose_name_plural': 'Types Of Transplant',
            },
        ),
        migrations.AlterModelOptions(
            name='answer',
            options={'verbose_name': 'Answer', 'verbose_name_plural': 'Answers'},
        ),
        migrations.AlterModelOptions(
            name='caregiver_survey_question_answer',
            options={'verbose_name': "Caregiver's Answer", 'verbose_name_plural': "Caregiver's Answers"},
        ),
        migrations.AlterModelOptions(
            name='patient',
            options={'verbose_name': 'Pazient', 'verbose_name_plural': 'Pazients'},
        ),
        migrations.AlterModelOptions(
            name='patient_survey_question_answer',
            options={'verbose_name': "Patient's Answer", 'verbose_name_plural': "Patient's Answers"},
        ),
        migrations.AlterModelOptions(
            name='question',
            options={'verbose_name': 'Question', 'verbose_name_plural': 'Questions'},
        ),
        migrations.AlterModelOptions(
            name='questiontype',
            options={'verbose_name': 'Type Of Question', 'verbose_name_plural': 'Types Of Question'},
        ),
        migrations.AlterModelOptions(
            name='survey',
            options={'verbose_name': 'Survey', 'verbose_name_plural': 'Surveys'},
        ),
        migrations.AlterField(
            model_name='patient',
            name='transplant_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='surveys.TransplantType'),
        ),
    ]
