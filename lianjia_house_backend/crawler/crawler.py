"""
链家二手房爬虫
"""
import base64
import re
import requests
import time
import random
import threading
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver  #
from selenium.webdriver.chrome.options import Options
import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from lianjia_backend.settings import logger

headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate,br',
           'Accept-Language': 'zh-CN,zh;q=0.9',
           'Cache-Control': 'no-cache',
           'Connection': 'keep-alive',
           'Cookie': 'uuid=d1e3a8e4-0b61-47ec-dc29-52a76270c028; ganji_uuid=9056650704920054735139; Hm_lvt_936a6d5df3f3d309bda39e92da3dd52f=1604132547; antipas=230j50108s0O75X45551839h277; lg=1; cityDomain=www; user_city_id=-1; clueSourceCode=%2A%2300; sessionid=af0f21bb-4b26-41b3-c904-9fc2a27e9b30; close_finance_popup=2021-03-07; cainfo=%7B%22ca_a%22%3A%22-%22%2C%22ca_b%22%3A%22-%22%2C%22ca_s%22%3A%22seo_baidu%22%2C%22ca_n%22%3A%22default%22%2C%22ca_medium%22%3A%22-%22%2C%22ca_term%22%3A%22-%22%2C%22ca_content%22%3A%22-%22%2C%22ca_campaign%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22scode%22%3A%22-%22%2C%22keyword%22%3A%22-%22%2C%22ca_keywordid%22%3A%22-%22%2C%22display_finance_flag%22%3A%22-%22%2C%22platform%22%3A%221%22%2C%22version%22%3A1%2C%22client_ab%22%3A%22-%22%2C%22guid%22%3A%22d1e3a8e4-0b61-47ec-dc29-52a76270c028%22%2C%22ca_city%22%3A%22dazhou%22%2C%22sessionid%22%3A%22af0f21bb-4b26-41b3-c904-9fc2a27e9b30%22%7D; Hm_lvt_bf3ee5b290ce731c7a4ce7a617256354=1615011890,1615096103,1615105154; preTime=%7B%22last%22%3A1615105243%2C%22this%22%3A1615011888%2C%22pre%22%3A1615011888%7D; Hm_lpvt_bf3ee5b290ce731c7a4ce7a617256354=1615105245',
           'Host': 'www.baidu.com',
           'Pragma': 'no-cache',
           'Referer': 'https://www.baidu.com',
           'Upgrade-Insecure-Requests': '1',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}


class LianjiaCrawler:

    def __init__(self, ):
        self.host = 'https://mas.lianjia.com'
        self.url = "https://mas.lianjia.com/ershoufang/pg{page}/"
        self.driver = None
        self.set_up()

    def set_up(self):
        """
        初始化 浏览器的一些设置
        :return:
        """
        # chrome_options = Options()
        # chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # self.driver = webdriver.Chrome(chrome_options=chrome_options, executable_path='chromedriver.exe')
        chrome_options = Options()
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--disable-gpu')

        ua = 'Mozilla/5.0 (compatible; Baiduspider-render/2.0; +http://www.baidu.com/search/spider.html)'
        # https://www.cnblogs.com/xieqiankun/p/hide-webdriver.html
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # 改ua，替换为前面预设的ua
        chrome_options.add_argument('user-agent=' + ua)
        # 关闭图片加载，提高爬虫速度
        chrome_options.add_argument('blink-settings=imagesEnabled=false')
        self.driver = webdriver.Chrome(chrome_options=chrome_options, executable_path='chromedriver.exe')
        # self.driver.minimize_window()
        script = 'Object.defineProperty(navigator,"webdriver",{get:() => false,})'
        self.driver.execute_script(script)

    def get_house_detail(self, house_detail_url):
        """
        获取详细信息详情，用beautifulsoup解析
        :return:
        """
        from lianjia.models import House

        try:
            self.driver.get(house_detail_url)
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            # house_number 获取页面链接，随后依据获取的页面链接打开页面爬取
            house_number_div = soup.find('div', attrs={'class': 'houseRecord'})
            house_number_div_text = house_number_div.text
            house_number = house_number_div_text.replace('链家编号', '').replace('举报', '')
            print(f'{house_number}')
            # 解析基本信息
            title_h1 = soup.find('h1', attrs={'class': 'main'})
            title = title_h1.text
            # 爬虫用CSS选择器进行信息定位
            area_div = soup.find('div', attrs={'class': 'areaName'})
            areas_a = area_div.find_all('a')
            area = areas_a[0].text
            district = areas_a[1].text
            address = areas_a[2].text
            # area = area_div.find_all('span')[1].text.replace('\xa0', ' ').strip().split(' ')[0]

            community_div = soup.find('div', attrs={'class': 'communityName'})
            community_a = community_div.a
            community = community_a.text

            price_div = soup.find('div', attrs={'class': 'price'})
            price_span = price_div.find('span', attrs={'class': 'total'})
            price = price_span.text

            content_div = soup.find('div', attrs={'class': 'introContent'})
            lis = content_div.find('div', attrs={'class': 'content'}).find('ul').find_all('li')

            layout_li = lis[0]
            layout = layout_li.text.replace('房屋户型', '')

            layer_li = lis[1]
            layer = layer_li.text.replace('所在楼层', '').strip()

            size_li = lis[2]
            size = size_li.text.replace('建筑面积', '').replace('㎡', '')

            toward_li = lis[6]
            toward = toward_li.text.replace('房屋朝向', '')

            decorate_li = lis[8]
            decorate = decorate_li.text.replace('装修情况', '')

            elevator_li = lis[10]
            elevator = elevator_li.text.replace('配备电梯', '')

            # 首图
            image_div = soup.find('div', attrs={'class', 'imgContainer'})
            image_src = image_div.img.get('src')

            # 下面Django框架函数用于更新数据库数据，只有对应上所有的键才能添加
            house, _ = House.objects.update_or_create(
                defaults={
                    'title': title,
                    'area': area,
                    'district': district,
                    'address': address,
                    'community': community,
                    'price': price,
                    'layout': layout,
                    'size': size,
                    'unit_price': round(float(price) * 10000 / float(size)),
                    'toward': toward,
                    'decorate': decorate,
                    'layer': layer,
                    'image_url': image_src,
                    'elevator': elevator,
                },
                house_id=house_number
            )

            # 交易属性
            transaction_div = soup.find('div', attrs={"class": 'transaction'})
            transaction_content_div = transaction_div.find('div', attrs={"class": "content"})
            lis = transaction_content_div.find('ul').find_all('li')

            listed_date = lis[0].text.replace('挂牌时间', '').replace('\n', '')
            house.year = listed_date.split('-')[0]
            type = lis[1].text.replace('交易权属', '').replace('\n', '')
            house.type = type
            use = lis[3].text.replace('房屋用途', '').replace('\n', '')
            house.use = use
            house.save()

            # 经纬度
            data = html[html.find('resblockPosition'): html.find('resblockPosition') + 100]
            PATTENPOSITION = re.compile(r"resblockPosition:'(.*?),(.*?)',")
            points = re.findall(PATTENPOSITION, data)
            if points:
                house.latitude = points[0][0]
                house.longitude = points[0][1]
            house.save()
            logger.info(f'更新数据库表！')
        except Exception as e:
            logger.error(f'采集异常 {e}，等待一段时间')
            if 'ProtocolError' in str(e) or 'HTTPConnectionPool' in str(e):
                exit(0)
            # time.sleep(3 * 60)

    def get_page_info(self, page_num):
        """
        获取页面的内容
        :return:
        """

        assert page_num > 0

        url = self.url.format(page=page_num)
        self.driver.get(url)
        time.sleep(6)
        # html = self._request(url=url)
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        ul = soup.find('ul', attrs={'class': 'sellListContent'})
        lis = ul.find_all('li')
        for i, li in enumerate(lis):
            # print(li)
            house_detail_uri = li.a.get('href')
            access_url = house_detail_uri
            logger.info(f'采集{page_num}页共{len(lis)}个房子，当前第{i + 1}个房子的数据！url {access_url}')
            # cars = House.objects.filter(url=access_url)
            # if cars:
            #     logger.info(f'已存在，跳过！')
            #     continue
            time.sleep(2)
            self.get_house_detail(house_detail_uri)

    def run(self):
        """
        启动爬虫服务
        :return:
        """
        for i in range(1, 10000):
            logger.info(f'开始采集第{i}页数据！')
            try:
                self.get_page_info(i)
            except Exception as e:
                logger.info(f'采集异常，{e}')
                if 'ProtocolError' in str(e) or 'HTTPConnectionPool' in str(e):
                    break
            logger.info(f'采集第{i}页数据完成！')


def start():
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lianjia_backend.settings')
    django.setup()
    # 清理日志
    from lianjia_backend.settings import BASE_DIR
    logs_dir = os.path.join(BASE_DIR, 'logs')
    if logs_dir:
        log_file = os.path.join(logs_dir, 'system.log')
        if os.path.exists(log_file):
            try:
                os.remove(log_file)
            except Exception as e:
                print(e)

    gzc = LianjiaCrawler()
    gzc.run()
    # thread = threading.Thread(target=gzc.run, args=())
    # thread.start()
    logger.info('处理成功！')
    return gzc.driver


if __name__ == '__main__':
    start()
