# Generated by Django 2.2 on 2021-01-24 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_holidays'),
    ]

    operations = [
        migrations.AlterField(
            model_name='holidays',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
