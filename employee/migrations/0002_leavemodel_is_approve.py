# Generated by Django 2.2 on 2021-01-06 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='leavemodel',
            name='is_approve',
            field=models.NullBooleanField(),
        ),
    ]
