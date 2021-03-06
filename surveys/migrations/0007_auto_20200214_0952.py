# Generated by Django 3.0.3 on 2020-02-14 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0006_auto_20200214_0949'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='answer',
            options={'ordering': ['question', 'answer_sequence_number'], 'verbose_name': 'Answer', 'verbose_name_plural': 'Answers'},
        ),
        migrations.AlterModelOptions(
            name='question',
            options={'ordering': ['survey', 'question_sequence_number', 'question_subsequence_number'], 'verbose_name': 'Question', 'verbose_name_plural': 'Questions'},
        ),
        migrations.RemoveField(
            model_name='answer',
            name='answer_subsequence_number',
        ),
        migrations.AddField(
            model_name='question',
            name='question_subsequence_number',
            field=models.CharField(blank=True, max_length=1, null=True),
        ),
    ]
