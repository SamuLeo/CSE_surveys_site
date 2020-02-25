# Generated by Django 3.0.3 on 2020-02-19 17:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0013_auto_20200218_2317'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiagnosisType',
            fields=[
                ('value', models.CharField(max_length=50, primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': 'Type Of Diagnosis',
                'verbose_name_plural': 'Types Of Diagnosis',
            },
        ),
        migrations.AlterModelOptions(
            name='caregiver_survey_question_answer',
            options={'ordering': ['caregiver', 'date', 'survey', 'question', 'answer'], 'verbose_name': "Caregiver's Answer", 'verbose_name_plural': "Caregiver's Answers"},
        ),
        migrations.AlterModelOptions(
            name='patient_survey_question_answer',
            options={'ordering': ['patient', 'date', 'survey', 'question', 'answer'], 'verbose_name': "Patient's Answer", 'verbose_name_plural': "Patient's Answers"},
        ),
        migrations.RenameField(
            model_name='patient',
            old_name='resignation_date',
            new_name='diagnosis_date',
        ),
        migrations.AddField(
            model_name='caregiver',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='discharge_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='transplant_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='surveys.TransplantType'),
        ),
        migrations.AddField(
            model_name='patient',
            name='diagnosis_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='surveys.DiagnosisType'),
        ),
    ]
