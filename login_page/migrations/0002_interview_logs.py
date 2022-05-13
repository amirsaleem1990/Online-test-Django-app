# Generated by Django 3.2.4 on 2021-07-19 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_page', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='interview_logs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interview_id', models.IntegerField()),
                ('user_id', models.IntegerField()),
                ('Question_number', models.IntegerField()),
                ('Q_id', models.IntegerField()),
                ('Question', models.TextField(max_length=255)),
                ('Selected_option', models.TextField(max_length=255)),
                ('Options', models.TextField(max_length=255)),
                ('Correct_answer', models.TextField(max_length=255)),
            ],
            options={
                'db_table': 'interview_logs',
            },
        ),
    ]
