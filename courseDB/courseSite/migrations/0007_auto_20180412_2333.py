# Generated by Django 2.0.2 on 2018-04-13 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courseSite', '0006_auto_20180412_2331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='times',
            field=models.CharField(max_length=20),
        ),
    ]