from django.db import models


class BaseModel(models.Model):
    is_delete = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)

    # 设置 abstract = True 来声明基表，作为基表的Model不能在数据库中形成对应的表
    class Meta:
        abstract = True


class MyUser(BaseModel):
    """
    扩展用户表 以前面的basemodel为基表
    """
    from django.contrib.auth.models import User
    # django.contrlib.auth.models有一个AbstractUser模块，用于添加新的类继承,后续创建不再需要重复写isdelete和createtime
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    # 使用扩展表添加中文字段，外键需要进行级联操作
    user_name = models.CharField(max_length=100, null=True, help_text='用户昵称')


class House(BaseModel):
    """
    基本信息 同理以basemodel为基表
    """
    house_id = models.CharField(null=True, max_length=200, help_text='房屋ID')
    title = models.CharField(null=True, max_length=200, help_text='标题')
    area = models.CharField(null=True, max_length=200, help_text='地区')
    district = models.CharField(null=True, max_length=200, help_text='街道')
    address = models.CharField(null=True, max_length=200, help_text='详细地址')
    community = models.CharField(null=True, max_length=200, help_text='小区')
    price = models.FloatField(null=True, help_text='价格，单位万元')
    layout = models.CharField(null=True, max_length=200, help_text='房子布局， 几房几厅')
    size = models.FloatField(null=True, help_text='房子大小， 多少平米')
    unit_price = models.FloatField(null=True, help_text='房子均价')
    toward = models.CharField(null=True, max_length=200, help_text='朝向')
    decorate = models.CharField(null=True, max_length=200, help_text='装修类型')
    layer = models.CharField(null=True, max_length=200, help_text='楼层')
    image_url = models.CharField(null=True, max_length=500, help_text='图片地址')
    year = models.FloatField(null=True, max_length=500, help_text='挂牌时间')
    elevator = models.CharField(null=True, max_length=500, help_text='是否有电梯')
    latitude = models.CharField(null=True, max_length=500, help_text='经度')
    longitude = models.CharField(null=True, max_length=500, help_text='维度')
    type = models.CharField(null=True, max_length=200, help_text='交易权属，例如商品房')
    use = models.CharField(null=True, max_length=200, help_text='房屋用途，例如普通住宅')
