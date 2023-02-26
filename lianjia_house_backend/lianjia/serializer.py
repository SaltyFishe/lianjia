from django.db.models import Sum, Count, Avg
from rest_framework import serializers
from lianjia.models import House


class HouseInfoSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(required=False)

    class Meta:
        model = House
        fields = '__all__'
        depth = 1

    def get_url(self, object):
        return f'https://mas.lianjia.com/ershoufang/{object.house_id}.html'


class GeneralAnalysisSerializer(serializers.Serializer):

    def analysis(self):
        """

        :return:
        """
        total = House.objects.count()
        jingzhuang = House.objects.filter(decorate='精装').count()
        maopei = House.objects.filter(decorate='毛坯').count()
        total_price = House.objects.all().aggregate(Sum('price'))
        return {'total': total, 'jingzhuang': jingzhuang, 'maopei': maopei, 'total_price': total_price}

    def area_analysis(self):
        """
        区域统计
        :return:
        """
        return House.objects.values("area").annotate(count=Count(id))

    def community_analysis(self):
        """
        小区统计
        :return:
        """
        return House.objects.values("community").annotate(count=Count(id))

    def price_analysis(self):
        """
        价格区间统计
        :return:
        """
        prices = []
        count1 = House.objects.filter(price__range=(0, 30)).count()
        prices.append({'name': '0~30万', 'value': count1})
        count2 = House.objects.filter(price__range=(31, 60)).count()
        prices.append({'name': '31~60万', 'value': count2})
        count3 = House.objects.filter(price__range=(61, 91)).count()
        prices.append({'name': '61~91万', 'value': count3})
        count4 = House.objects.filter(price__range=(91, 120)).count()
        prices.append({'name': '91~120万', 'value': count4})
        count5 = House.objects.filter(price__gt=120).count()
        prices.append({'name': '121~万', 'value': count5})
        return prices

    def decorate_analysis(self):
        """
        房子装修情况统计
        :return:
        """
        return House.objects.values("decorate").annotate(count=Count(id))

    def size_price_analysis(self):
        """

        :return:
        """
        datas = []
        houses = House.objects.all()
        houses = HouseInfoSerializer(instance=houses, many=True)
        for c in houses.data:
            datas.append([c.get('size'), c.get('price')])
        return datas

