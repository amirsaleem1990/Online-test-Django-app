# Generated by Django 3.2.4 on 2021-07-23 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_page', '0007_auto_20210723_0802'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuditEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=64)),
                ('ip', models.GenericIPAddressField(null=True)),
                ('username', models.CharField(max_length=256, null=True)),
            ],
        ),
    ]
