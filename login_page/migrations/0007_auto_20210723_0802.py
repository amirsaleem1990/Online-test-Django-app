# Generated by Django 3.2.4 on 2021-07-23 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_page', '0006_interview_logs_score'),
    ]

    operations = [
        migrations.DeleteModel(
            name='users',
        ),
        migrations.AddField(
            model_name='interview_info',
            name='ending_reason',
            field=models.TextField(default='null', max_length=255),
            preserve_default=False,
        ),
    ]
