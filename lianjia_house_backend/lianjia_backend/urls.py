"""GZCarBusinessSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from lianjia import views
from django.conf.urls import url
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    # 登录、注册、token认证
    path('api/login', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/logout', views.LogoutView.as_view(), name='logout'),
    path('api/modify', views.ModifyPersonInfoView.as_view(), name='modify'),
    path('api/register', views.RegisterView.as_view(), name='register'),
    path('api/user/info', views.UserInfo.as_view(), name='user_info'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    # 爬虫接口
    url(r'api/crawler', views.Crawler.as_view()),
    # 源数据接口
    path('api/houses', views.HouseDataView.as_view(), name='houses'),
    # 首页的接口
    path('api/last', views.LastHouseView.as_view(), name='last'),
    # 图表的卡片统计
    url(r'api/statistics/general', views.GeneralAnalysisView.as_view()),
    url(r'api/statistics/area', views.AreaAnalysisView.as_view()),
    url(r'api/statistics/community', views.CommunityAnalysisView.as_view()),
    url(r'api/statistics/price', views.PriceAnalysisView.as_view()),
    url(r'api/statistics/decorate', views.DecorateAnalysisView.as_view()),
    url(r'api/statistics/size_price', views.SizePriceAnalysisView.as_view()),
    # 预测接口
    url(r'api/predict', views.PredictView.as_view()),

]
