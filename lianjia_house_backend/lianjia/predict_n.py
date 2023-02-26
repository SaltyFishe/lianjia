import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib as mpl
import os

import matplotlib.pyplot as plt
from IPython.display import display
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lianjia_backend.settings')
django.setup()
from lianjia.models import House
from django_pandas.io import read_frame
# 指定画布风格
# plt.style.use("fivethirtyeight")
# plt.rcParams['font.sans-serif'] = ['SimHei']
# plt.rcParams['axes.unicode_minus'] = False
# 检查Python版本
from sys import version_info

if version_info.major != 3:
    raise Exception('请使用Python 3 来完成此项目')
# df = pd.read_csv("lianjia.csv")
columns = ['house_id', 'community', 'toward', 'layout', 'elevator', 'area', 'district',
           'address', 'layer', 'size', 'decorate', 'unit_price', 'price', 'year',
           'latitude', 'longitude']
qs = House.objects.all()
df = read_frame(qs)
# anjuke_df['District'] = anjuke_df['Region'].str.extract(r'.+?-(.+?)-.+?', expand=False)
# house_id无意义可去除，重新摆放列位置
data = pd.DataFrame(df, columns=columns)
# 检查缺失值情况
data.info()
# 删除价格缺失的行
misn = len(data.loc[(data['price'].isnull()), 'price'])
print('1、price缺失值数量为：' + str(misn))
# data.loc[(data['price'].isnull()), 'price']
data = data[pd.notnull(data['price'])]
misn = len(data.loc[(data['price'].isnull()), 'price'])
print('2、price缺失值数量为：' + str(misn))
# display(data.head())
# 总价前五的房子
data.sort_values('price', ascending=False).head(5)

# 特征值是数值的一些统计值，包括平均数，标准差，中位数，最小值，最大值，25%分位数，75%分位数。
data.describe()

# 按区域分析数量
df_house_count = data.groupby('area')['house_id'].count().sort_values(ascending=False)
df_house_count.columns = ['Region', 'Count']

# plt.figure(figsize=(10, 10))
# plt.title(u'各区域二手房数量百分比', fontsize=18)
# explode = [0] * len(df_house_count)
# explode[0] = 0.2
# plt.pie(df_house_count, radius=3, autopct='%1.f%%', shadow=True, labels=df_house_count.index, explode=explode)
# plt.axis('equal')

# plt.show()
# plt.close()
# 按区域分析数量和价格
df_house_mean = data.groupby('area')['unit_price'].mean().sort_values(
    ascending=False).to_frame().reset_index()
df_house_mean
# s-size点大小 c-color点颜色
# plt.figure(figsize=(8, 6))
# plt.scatter(data['longitude'], data['latitude'], s=data['unit_price'] / 500, c=data['price'], alpha=0.5)
#
# plt.grid()


# 极差分析
def d_range(df, *cols):
    krange = list()
    for col in cols:
        crange = df[col].max() - df[col].min()
        krange.append(crange)
    return krange


key1 = "unit_price"
dr = d_range(data, key1)
print(f"极差是{dr}")
# 发现价差相差17万，发现一个是地下室，另一个是2层别墅
data[data["unit_price"] == data[key1].min()]
data[data["unit_price"] == data[key1].max()]

# 频率分布情况
data['price'].hist(bins=10)

gcut = pd.cut(data["price"], 50, right=False)
gcut_count = gcut.value_counts(sort=False)
data['priceRange'] = gcut.values
print(data.head(10))

# 区间出现频率
# r_zj = pd.DataFrame(gcut_count)
# r_zj.rename(columns={gcut_count.name: '频数'}, inplace=True)
# r_zj['频率'] = r_zj['频数'] / r_zj['频数'].sum()
# r_zj['累计频率'] = r_zj['频率'].cumsum()
# r_zj['频率%'] = r_zj['频率'].apply(lambda x: "%.2f%%" % (x * 100))
# r_zj['累计频率%'] = r_zj['累计频率'].apply(lambda x: "%.2f%%" % (x * 100))
# r_zj.style.bar(subset=['频率', '累计频率'])

# 朝向 频率分布 定性字段 # 可视化显示
# cx_g = data['toward'].value_counts(sort=True)
# r_cx = pd.DataFrame(cx_g)
#
# r_cx.rename(columns={cx_g.name: '频数'}, inplace=True)
# r_cx['频率'] = r_cx['频数'] / r_cx['频数'].sum()
# r_cx['累计频率'] = r_cx['频率'].cumsum()
# r_cx['频率%'] = r_cx['频率'].apply(lambda x: "%.2f%%" % (x * 100))
# r_cx['累计频率%'] = r_cx['累计频率'].apply(lambda x: "%.2f%%" % (x * 100))
# r_cx.style.bar(subset=['频率', '累计频率'])
#
# # 定性字段 除直方图外，绘制饼图
# plt.figure(num=1, figsize=(40, 20))
# r_cx['频率'].plot(kind='bar', width=0.8, rot=0, color='k', grid=True, alpha=0.5)
# plt.xticks(rotation=90)
# plt.title("朝向分布频率直方图")
#
# plt.figure(num=2)
# plt.pie(r_cx['频数'],
#         labels=r_cx.index,
#         autopct='%.2f%%',
#         shadow=True)
# plt.axis("equal")

# 对二手房区域分组对比二手房数量和每平米房价
df_house_count = df.groupby('area')['price'].count().sort_values(
    ascending=False).to_frame().reset_index()
df_house_mean = df.groupby('area')['unit_price'].mean().sort_values(ascending=False).to_frame().reset_index()

f, [ax1, ax2, ax3] = plt.subplots(3, 1, figsize=(20, 15))
sns.barplot(x='area', y='unit_price', palette="Blues_d", data=df_house_mean, ax=ax1)
ax1.set_title('杭州各大区二手房每平米单价对比', fontsize=15)
ax1.set_xlabel('区域')
ax1.set_ylabel('每平米单价')

sns.barplot(x='area', y='price', palette="Greens_d", data=df_house_count, ax=ax2)
ax2.set_title('杭州各大区二手房数量对比', fontsize=15)
ax2.set_xlabel('区域')
ax2.set_ylabel('数量')

sns.boxplot(x='area', y='price', data=df, ax=ax3)
ax3.set_title('杭州各大区二手房房屋总价', fontsize=15)
ax3.set_xlabel('区域')
ax3.set_ylabel('房屋总价')

data.loc[data['price'] == data.price.max()]

# f, [ax1, ax2] = plt.subplots(1, 2, figsize=(20, 5))
# 建房面积的分布情况
# sns.distplot(data['size'], bins=50, ax=ax1, color='r')
# sns.kdeplot(data['size'], shade=True, ax=ax1)
# # 建房面积和出售价格的关系
# sns.regplot(x='size', y='price', data=data, ax=ax2)
# ax1.set_xlabel('面积')
# ax1.set_ylabel('总价')
# plt.show()
# plt.close()

# f, ax1 = plt.subplots(figsize=(40, 60))
# sns.countplot(y='layout', data=data, ax=ax1)
# ax1.set_title('房屋户型', fontsize=15)
# ax1.set_xlabel('数量')
# ax1.set_ylabel('户型')
# plt.show()
# plt.close()

data['decorate'].value_counts()

# 画幅设置
f, [ax1, ax2, ax3] = plt.subplots(1, 3, figsize=(20, 5))
sns.countplot(data['decorate'], ax=ax1)
ax1.set_xlabel('户型')
ax1.set_ylabel('数量')
sns.barplot(x='decorate', y='price', data=data, ax=ax2)
sns.boxplot(x='decorate', y='price', data=data, ax=ax3)
# plt.show()

misn = len(data.loc[(data['elevator'].isnull()), 'elevator'])
print('elevator缺失值数量为：' + str(misn))

data.loc[(df['elevator'].isnull()), 'elevator'] = "暂无数据"
f, [ax1, ax2] = plt.subplots(1, 2, figsize=(20, 10))
sns.countplot(data['elevator'], ax=ax1)
ax1.set_title('有无电梯数量对比', fontsize=15)
ax1.set_xlabel('是否有电梯')
ax1.set_ylabel('数量')

sns.barplot(x='elevator', y='price', data=data, ax=ax2)
ax2.set_title('有无电梯房价对比', fontsize=15)
ax2.set_xlabel('是否有电梯')
ax2.set_ylabel('总价')
# plt.show()

# 年份 装修 价格分析
grid = sns.FacetGrid(df, row='elevator', col='decorate', palette='seismic', size=4)
grid.map(plt.scatter, 'year', 'price')
grid.add_legend()

columns = ['size', 'unit_price', 'price', 'year']
dataNew = data[columns]
fig = plt.figure(figsize=(12, 12))
sns.heatmap(dataNew.corr(), vmax=1, square=True, annot=True)

# 完善数据集，删除无意义特征，将特征数字化
drop_out = ['house_id', 'community', 'toward', 'layout', 'address', 'district',
            'layer', 'latitude', 'longitude', 'priceRange', 'unit_price']
# drop_out = ['house_id', 'community', 'toward', 'layout','address', 'district',
#             'layer', 'priceRange', 'unit_price']
data = data.drop(drop_out, axis=1)
# print(data['price'].isnull().value_counts()) # 50 True
data.dropna(axis=0, subset=['price', 'year', 'decorate'], inplace=True)

data.loc[data['elevator'] == '暂无数据', 'elevator'] = '无'
data['elevator'].fillna(value="无")
print(data['elevator'].value_counts())
data.isnull().any()

# 汉字到数字的映射字典
# loc_map = {'上城': 1, '西湖': 2, '滨江': 3, '下城': 4, '拱墅': 5, '江干': 6, '萧山': 7, '余杭': 8, '钱塘新区': 9, '富阳': 10, '临安': 11}
loc_map = {
    '花山区': 1,
    '雨山区': 2,
    '当涂县': 3,
}
renovation_map = {'简装': 0, '精装': 1, '其他': 2, '毛坯': 3}
elevator_map = {'有': 1, '无': 0}

# df['Layout_room_num'] = df['Layout'].str.extract('(^\d).*', expand=False).astype('int64')
data['area'] = data['area'].map(loc_map)
data['decorate'] = data['decorate'].map(renovation_map)
data['elevator'] = data['elevator'].map(elevator_map)
print('二手房房价有数据 {0} 条，字段 {1} 个。'.format(*data.shape))
# 分配数据集-训练集和测试集
prices = data['price']
features = data.drop('price', axis=1)
# 将连续数值型特征 Year 离散化，做分箱处理，pandas的 qcut 按中位数对“Year”特征进行分箱，分割数为8等份
data['year'] = pd.qcut(data['year'], 8).astype('object')
print(data.isnull().any())
print(data.head(10))

# 转换训练测试集格式为数组
features = np.array(features)
prices = np.array(prices)

# 导入sklearn进行训练测试集划分
from sklearn.model_selection import train_test_split


from sklearn.model_selection import KFold
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import make_scorer
from sklearn.model_selection import GridSearchCV


# 利用GridSearchCV计算最优解
def fit_model(X, y):
    """ 基于输入数据 [X,y]，利于网格搜索找到最优的决策树模型"""

    cross_validator = KFold(10, shuffle=True)

    regressor = DecisionTreeRegressor()

    params = {'max_depth': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}

    scoring_fnc = make_scorer(performance_metric)

    grid = GridSearchCV(estimator=regressor, param_grid=params, scoring=scoring_fnc, cv=cross_validator)

    # 基于输入数据 [X,y]，进行网格搜索
    grid = grid.fit(X, y)
    #     print pd.DataFrame(grid.cv_results_)
    return grid.best_estimator_


# 计算R2分数
def performance_metric(y_true, y_predict):
    """计算并返回预测值相比于预测值的分数"""
    from sklearn.metrics import r2_score
    score = r2_score(y_true, y_predict)

    return score


# import visuals as vs

# 分析模型
# vs.ModelLearning(features_train, prices_train)
# vs.ModelComplexity(features_train, prices_train)
features_train, features_test, prices_train, prices_test = train_test_split(features, prices, test_size=0.2,
                                                                            random_state=0)
def predict():

    optimal_reg1 = fit_model(features_train, prices_train)

    # 输出最优模型的 'max_depth' 参数
    print("最理想模型的参数 'max_depth' 是 {} 。".format(optimal_reg1.get_params()['max_depth']))

    predicted_value = optimal_reg1.predict(features_test)
    r2 = performance_metric(prices_test, predicted_value)

    print("最优模型在测试数据上 R^2 分数 {:,.2f}。".format(r2))
    return optimal_reg1



if __name__ == '__main__':

    optimal_reg1 = predict()
    # # 生成三个客户的数据
    client_data = [
        [0, 2, 50, 0, 2005],  # 客户 1 电梯，区域，面积，毛坯， 年份
        [0, 2, 98, 1, 2000]  # 客户 2]  # 客户 3
    ]

    # 进行预测
    predicted_price = optimal_reg1.predict(client_data)
    for i, price in enumerate(predicted_price):
        print("Predicted selling price for Client {}'s home: ${:,.2f}".format(i + 1, price))
