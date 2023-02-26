# Generated by Django 3.2.12 on 2022-05-22 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lianjia', '0003_alter_housetransactioninfo_house'),
    ]

    operations = [
        migrations.AddField(
            model_name='house',
            name='address',
            field=models.CharField(help_text='详细地址', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='house',
            name='district',
            field=models.CharField(help_text='街道', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='house',
            name='elevator',
            field=models.CharField(help_text='是否有电梯', max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='house',
            name='latitude',
            field=models.CharField(help_text='经度', max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='house',
            name='longitude',
            field=models.CharField(help_text='维度', max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='house',
            name='type',
            field=models.CharField(help_text='交易权属，例如商品房', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='house',
            name='use',
            field=models.CharField(help_text='房屋用途，例如普通住宅', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='house',
            name='year',
            field=models.CharField(help_text='挂牌时间', max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='house',
            name='price',
            field=models.FloatField(help_text='价格，单位万元', null=True),
        ),
        migrations.DeleteModel(
            name='HouseTransactionInfo',
        ),
    ]