# Generated by Django 3.2.13 on 2022-04-30 15:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='House',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_delete', models.BooleanField(default=False)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('house_id', models.CharField(help_text='房屋ID', max_length=200, null=True)),
                ('title', models.CharField(help_text='标题', max_length=200, null=True)),
                ('area', models.CharField(help_text='地区', max_length=200, null=True)),
                ('community', models.CharField(help_text='小区', max_length=200, null=True)),
                ('price', models.IntegerField(help_text='价格，单位元', null=True)),
                ('layout', models.CharField(help_text='房子布局， 几房几厅', max_length=200, null=True)),
                ('size', models.IntegerField(help_text='房子大小， 多少平米', null=True)),
                ('toward', models.CharField(help_text='朝向', max_length=200, null=True)),
                ('decorate', models.CharField(help_text='装修类型', max_length=200, null=True)),
                ('layer', models.CharField(help_text='楼层', max_length=200, null=True)),
                ('tags', models.CharField(help_text='标签', max_length=200, null=True)),
                ('image_url', models.CharField(help_text='图片地址', max_length=500, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_delete', models.BooleanField(default=False)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('user_name', models.CharField(help_text='用户昵称', max_length=100, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HouseTransactionInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_delete', models.BooleanField(default=False)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('listed_date', models.DateField(help_text='挂牌时间', null=True)),
                ('type', models.CharField(help_text='房子类型，公寓/普通住宅', max_length=200, null=True)),
                ('house', models.ForeignKey(help_text='房子外键', on_delete=django.db.models.deletion.CASCADE, to='lianjia.house')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
