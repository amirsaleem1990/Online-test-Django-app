# Generated by Django 3.2.4 on 2021-07-19 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_page', '0005_interview_logs_dificulty_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='interview_logs',
            name='score',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
