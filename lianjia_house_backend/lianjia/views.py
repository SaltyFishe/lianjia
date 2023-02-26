import os
import re
from datetime import datetime
from collections import OrderedDict

import rest_framework
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import permissions, generics
from rest_framework import views
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework_simplejwt import authentication
# from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from lianjia import serializer as g_serializer
from lianjia import models as g_model
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from lianjia_backend.settings import logger
from lianjia.filter import HouseDetailFilter
from selenium import webdriver

driver: webdriver = None


class Pagination(PageNumberPagination):
    '''
    自定义分页
    '''
    # 默认每页显示的个数
    page_size = 100
    # 可以动态改变每页显示的个数
    page_size_query_param = 'page_size'
    # 页码参数
    page_query_param = 'page'
    # 最多能显示多少页
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('code', 200),
            ('message', '数据获取成功！'),
            ('datas', data),
        ]))


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        try:
            # 用户登录返回token
            super().validate(attrs)
            refresh = self.get_token(self.user)
            info = {'code': 200, 'data': {}, 'message': ''}
            info['data'].update(token=str(refresh.access_token))
            info['data'].update(refresh=str(refresh))
            info['data'].update(username=self.user.username)
            info.update(code=200)
        except AuthenticationFailed as e:
            info = {'code': 500, 'data': {}, 'message': '账号或者密码错误！'}
        except Exception as e:
            info = {'code': 500, 'data': f'{e}', 'message': '登录时发生其他异常错误！'}
        return info


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# Create your views here.
class TestView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (authentication.JWTAuthentication,)

    def get(self, request):
        return Response('ok')


class LogoutView(views.APIView):

    def post(self, request):
        """
        :return:
        """
        return Response({
            'data': '',
            'message': '退出成功！',
            'code': 200
        })


class RegisterView(views.APIView):

    def post(self, request, **data):
        """
        注册
        :param request:
        :param data:
        :return:
        """

        phone = request.data.get('phone')
        reg = '^1(3[0-9]|4[5,7]|5[0,1,2,3,5,6,7,8,9]|6[2,5,6,7]|7[0,1,7,8]|8[0-9]|9[1,8,9])\d{8}$'
        # 校验手机号
        if not re.match(reg, phone):
            return Response({
                'data': '',
                'message': '手机号不正确！',
                'code': 500
            })
        username = request.data.get('username')
        password = request.data.get('password')
        password2 = request.data.get('password2')
        logger.debug(username, password, password2)
        if not password:
            return Response({
                'data': '',
                'message': '密码不能为空！',
                'code': 500
            })
        if password2 != password:
            return Response({
                'data': '',
                'message': '两次密码不一致！',
                'code': 500
            })
        users = User.objects.filter(username=phone)
        if users:
            return Response({
                'data': '',
                'message': '账号已存在！',
                'code': 500
            })
        try:
            user = User.objects.create_user(username=phone, password=password2)
            g_model.MyUser.objects.create(user=user, user_name=username)
            if user:
                return Response({
                    'data': '',
                    'message': '注册成功！',
                    'code': 200
                })
        except Exception as e:
            return Response({
                'data': f'{e}',
                'message': '注册失败！',
                'code': 500
            })


class ModifyPersonInfoView(views.APIView):
    """
    修改个人资料
    """
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (authentication.JWTAuthentication,)

    def post(self, request, **data):
        try:
            user = request.user
            # 修改密码
            if request.data.get('password'):
                old_password = request.data.get('password')
                check = user.check_password(old_password)
                if not check:
                    return Response({
                        "code": 500,
                        "data": None,
                        "message": "旧密码不正确"
                    })
                new_password = request.data.get('newPassword')
                new_password2 = request.data.get('newPassword2')
                if new_password2 != new_password:
                    return Response({
                        "code": 500,
                        "data": None,
                        "message": "两次新密码不一致"
                    })
                user.set_password(new_password)
                user.save()
                return Response({
                    "code": 200,
                    "data": None,
                    "message": "密码修改成功！"
                })
            else:  # 修改个人信息
                phone = request.data.get('phone')
                user_name = request.data.get('userName')
                birthday = request.data.get('birthday')
                sex = request.data.get('sex')
                city = request.data.get('city')
                my_users = g_model.MyUser.objects.filter(user=user)
                if my_users:
                    my_user = my_users[0]
                    if phone:
                        reg = '^1(3[0-9]|4[5,7]|5[0,1,2,3,5,6,7,8,9]|6[2,5,6,7]|7[0,1,7,8]|8[0-9]|9[1,8,9])\d{8}$'
                        # 校验手机号
                        if not re.match(reg, phone):
                            return Response({
                                'data': '',
                                'message': '手机号不正确！',
                                'code': 500
                            })
                        user.username = phone
                        user.save()
                    if user_name:
                        my_user.user_name = user_name
                    if birthday:
                        try:
                            datetime.strptime(birthday, '%Y-%m-%d')
                        except Exception as e:
                            return Response({
                                'data': '',
                                'message': '生日日期格式错误！',
                                'code': 500
                            })
                        my_user.birthday = birthday
                    if sex:
                        my_user.sex = sex
                    if city:
                        my_user.city = city
                    my_user.save()
                return Response({
                    "code": 200,
                    "data": None,
                    "message": "个人信息修改成功！"
                })
        except Exception as e:
            return Response({
                'code': 500,
                'data': {"errors": "{}".format(e)},
                'message': "修改失败!"
            })


class UserInfo(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (authentication.JWTAuthentication,)

    # 依靠前端返回的token判读用户token身份
    def get(self, request, **data):
        """
        :return:
        """
        user = request.user
        my_users = g_model.MyUser.objects.filter(user=user)
        return Response(
            {
                'code': 200,
                'data': {
                    "user_name": my_users[0].user_name if my_users else '',
                    "name": request.user.username,
                    "roles": ["管理员" if request.user.is_staff else "普通用户"],
                    "avatar": "https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif"
                },
                'message': '获取成功'
            }
        )


class Crawler(views.APIView):
    """
    启动爬虫
    """

    def post(self, request):
        global driver
        from crawler.crawler import start

        try:
            driver = start()
            return Response({
                "code": 200,
                "data": {},
                "message": "下发成功"
            })
        except Exception as e:
            logger.error(e)
            return Response({
                "code": 500,
                "data": {},
                "message": f"下发失败, {e}"
            })

    def get(self, request):
        """
        获取日志进行显示
        :param request:
        :return:
        """
        dir = os.path.join("logs")
        if not dir:
            return Response({
                "code": 200,
                "data": [],
                "message": "获取日志成功！"
            })
        log_files = os.listdir(dir)
        if not log_files:
            return Response({
                "code": 200,
                "data": [],
                "message": "获取日志成功！"
            })
        new_log_file = log_files[-1]  # 最新的日志文件
        with open(os.path.join(dir, new_log_file), encoding='utf8') as f:
            lines = f.readlines()
            if lines.__len__() <= 20:
                return Response({
                    "code": 200,
                    "data": lines,  # 展示最近的20行
                    "message": "获取日志成功！"
                })
            else:
                return Response({
                    "code": 200,
                    "data": lines[len(lines) - 20:],  # 展示最近的20行
                    "message": "获取日志成功！"
                })

    def patch(self, request):
        """
        删除爬虫任务
        :param request:
        :return:
        """
        global driver
        try:
            os.system("taskkill /f /im chromedriver.exe")
            os.system("taskkill /f /im chromedri*.exe")
            # driver.close()
            return Response({
                "code": 200,
                "data": None,
                "message": "终止成功！"
            })
        except Exception as e:
            return Response({
                "code": 200,
                "data": None,
                "message": f"终止失败！ {e}"
            })


class HouseDataView(generics.ListAPIView):
    """
    获取二手房数据
    """
    pagination_class = Pagination  # 分页
    serializer_class = g_serializer.HouseInfoSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = HouseDetailFilter
    search_fields = ('house__title',)

    # 查询指令会经过filter过滤后返回一个queryset对象，用这个函数进行关键字（title）查找
    def get_queryset(self):
        title = self.request.query_params.get('title')
        return g_model.House.objects.filter(title__contains=title) if title else g_model.House.objects.all()


class LastHouseView(generics.ListAPIView):
    serializer_class = g_serializer.HouseInfoSerializer

    # 这个查找最近的三条数据，放主页
    def get_queryset(self):
        return g_model.House.objects.all().order_by('-id')[0:3]

    def get(self, request, *args, **kwargs):
        respone = self.list(request, *args, **kwargs)
        return Response(
            {'code': 200, 'data': respone.data, 'msg': '查询成功'}
        )


class GeneralAnalysisView(generics.GenericAPIView):
    """
    概览数据统计
    """

    def get(self, request, **data):
        """
        获取普通统计数据
        :param request:
        :param data:
        :return:
        """
        try:
            se = g_serializer.GeneralAnalysisSerializer(data=data)
            if se.is_valid(raise_exception=True):
                return Response({
                    "code": 200,
                    "data": se.analysis(),
                    "message": "获取普通分析数据成功！"
                })
        except Exception as e:
            return Response({
                'code': 500,
                'data': {"errors": "{}".format(e)},
                'message': "获取普通分析数据失败!"
            })


class AreaAnalysisView(generics.GenericAPIView):
    """
    获取根据地区的分析
    """

    def get(self, request, **data):
        try:
            se = g_serializer.GeneralAnalysisSerializer(data=data)
            if se.is_valid(raise_exception=True):
                return Response({
                    "code": 200,
                    "data": se.area_analysis(),
                    "message": "获取区域分析数据成功！"
                })
        except Exception as e:
            return Response({
                'code': 500,
                'data': {"errors": "{}".format(e)},
                'message': "获取区域分析数据失败!"
            })


class CommunityAnalysisView(generics.GenericAPIView):
    """
    获取小区房源分析
    """

    def get(self, request, **data):
        try:
            se = g_serializer.GeneralAnalysisSerializer(data=data)
            if se.is_valid(raise_exception=True):
                return Response({
                    "code": 200,
                    "data": se.community_analysis(),
                    "message": "获取小区分析数据成功！"
                })
        except Exception as e:
            return Response({
                'code': 500,
                'data': {"errors": "{}".format(e)},
                'message': "获取小区分析数据失败!"
            })


class PriceAnalysisView(views.APIView):
    """
    各价位统计
    """

    def get(self, request, **data):
        try:
            se = g_serializer.GeneralAnalysisSerializer(data=data)
            if se.is_valid(raise_exception=True):
                return Response({
                    "code": 200,
                    "data": se.price_analysis(),
                    "message": "获取各价位统计数据成功！"
                })
        except Exception as e:
            return Response({
                'code': 500,
                'data': {"errors": "{}".format(e)},
                'message': "获取各价位统计数据失败!"
            })


class DecorateAnalysisView(views.APIView):
    """
    装修情况统计
    """

    def get(self, request, **data):
        try:
            se = g_serializer.GeneralAnalysisSerializer(data=data)
            if se.is_valid(raise_exception=True):
                return Response({
                    "code": 200,
                    "data": se.decorate_analysis(),
                    "message": "获取装修统计数据成功！"
                })
        except Exception as e:
            return Response({
                'code': 500,
                'data': {"errors": "{}".format(e)},
                'message': "获取装修统计数据失败!"
            })


class SizePriceAnalysisView(views.APIView):
    """
    房屋大小及价格关系数据统计
    """

    def get(self, request, **data):
        try:
            se = g_serializer.GeneralAnalysisSerializer(data=data)
            if se.is_valid(raise_exception=True):
                return Response({
                    "code": 200,
                    "data": se.size_price_analysis(),
                    "message": "获取大小价格关系数据成功！"
                })
        except Exception as e:
            return Response({
                'code': 500,
                'data': {"errors": "{}".format(e)},
                'message': "获取大小价格数据失败!"
            })


optimal_reg1 = None


class PredictView(views.APIView):
    """
    房价预测
    """

    def post(self, request):
        """

        """
        global optimal_reg1

        # optimal_reg1 = predict()
        if not optimal_reg1:
            return Response({
                'code': 500,
                'data': None,
                'message': "数据集未进行训练，请先进行训练"
            })
        else:
            loc_map = {
                '花山区': 9,
                '雨山区': 10,
                '当涂县': 11,
            }
            renovation_map = {'简装': 0, '精装': 1, '其他': 2, '毛坯': 3}
            data = request.data
            elevator = data.get('elevator')
            region = data.get('region')
            area = data.get('area')
            year = data.get('year')
            decorate = data.get('decorate')
            house_data = [
                int(elevator),
                loc_map.get(region, 1),
                float(area),
                renovation_map.get(decorate, 0),
                int(year)
            ]
            # house_data = [0, 2, 50, 0, 1989]
            price = optimal_reg1.predict([house_data])
            price = price[0] / 2
            return Response({
                'code': 200,
                'data': price,
                'message': "success"
            })

    def put(self, request):
        """

        """
        global optimal_reg1

        from lianjia.predict import predict
        optimal_reg1 = predict()
        return Response({
            'code': 200,
            'data': {},
            'message': "更新训练结果成功"
        })
