# Generated by Django 3.2.12 on 2022-05-22 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lianjia', '0006_alter_house_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='house',
            name='year',
            field=models.FloatField(help_text='ζηζΆι΄', max_length=500, null=True),
        ),
    ]
