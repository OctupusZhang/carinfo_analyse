import re

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams['font.sans-serif'] = ['KaiTi']  # 定义字体，否则画图结果汉子无法显示
mpl.rcParams['font.serif'] = ['KaiTi']
fig = plt.figure(figsize=(10, 8))  # 900x900
# fig.add_subplot(2, 2, 1)  # 设置子画布，共2x2=4个，选择第一个画布
df = pd.read_csv('../results/carinfo.csv')


def draw_type_and_series():
    """
df_type.plot.bar(rot=30)  #x轴字体倾斜30度
plt.savefig('../results/car_type_amount_rank.png') #保存要放在show之前，否则保存图片为空白
plt.show()   #pandas画图实际调用的还是matplotlib库
plt.clf()    #清空画布，否则后面的图片会在之前的图片基础上叠加
df_series.plot.bar(rot=30)
plt.savefig('../results/car_series_amount_rank.png')
plt.clf()
    """
# df = df['品牌']
# df_type = df.groupby(by=['品牌']).size().sort_values(ascending=False)[0:10]
# df_series = df.groupby(by=['车系']).size().sort_values(ascending=False)[0:10]
    df_type = df['品牌'].value_counts()[0:10]
    df_series = df['车系'].value_counts()[0:10]
    df_type.plot.bar(rot=30)
    plt.savefig('../results/car_type_amount_rank.png')
    plt.clf()
    df_series.plot.bar(rot=30)
    plt.savefig('../results/car_series_amount_rank.png')
    plt.clf()


def draw_price():
    df_price = df['价格'].map(lambda x: float(x.strip('万')))
    # df_price = df_price.value_counts()
    # max_price = int(df_price.index.max())
    scale = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 25, 30, 35, 40, 45, 50, 60, 80, 100]
    labels = []
    amount = []
    for i in range(len(scale)):
        if i == 0:
            labels.append(f'小于{scale[i]}万')
            amount.append(df_price[df_price < scale[i]].count())
        if i == len(scale) - 1:
            labels.append(f'大于{scale[i]}万')
            amount.append(df_price[df_price >= scale[i]].count())
            break
        labels.append(f'{scale[i]}~{scale[i+1]}万')
        amount.append(df_price[(df_price < scale[i+1]) & (df_price >= scale[i])].count())  # 不能使用1<=df_price<2这种形式

    # fig, ax = plt.subplots()
    # ax.set_xticks([x for x in range(0, max_price+1, 7)]) #设定x轴范围与刻度
    # ax.set_xticklabels([str(x)+'万' for x in range(0, max_price+1, 7)], rotation=40) #设定x轴标签，若不设置，默认显示为上面设定的刻度范围
    df_price_new = pd.DataFrame(amount, labels)
    # print(df_new.sum())
    # plt.scatter(df_new.index, df_new)
    plt.xticks(rotation=30)  # 设置x轴参数
    plt.plot(df_price_new, 'ko-')
    plt.savefig('../results/price_range_rank.png')
    plt.clf()


def draw_year_price():
    car_series_list = df['车系'].value_counts().head().index
    year_list = df['上牌时间'].value_counts().index.sort_values()
    df_year_price = df[['上牌时间', '价格', '车系']]
    df_year_price = df_year_price.set_index(['车系', '上牌时间']).applymap(lambda x: float(x.strip('万')))

    ave_price_list = []
    for i in car_series_list:
        temp = []
        for j in year_list:
            try:
                ave_price = float('%.2f' % df_year_price.loc[f'{i}', f'{j}'].mean())
            except KeyError:
                ave_price = 0
            temp.append(ave_price)
        ave_price_list.append(temp)

    df_year_price = pd.DataFrame(ave_price_list, columns=year_list, index=car_series_list).T
    df_year_price[df_year_price == 0] = np.nan
    df_year_price = df_year_price.dropna()   #默认为0是对行操作，1对列操作，与mean，sum函数相反
    df_year_price.plot()
    plt.savefig('../results/price_year_rel.png')
    plt.clf()


def draw_distance_price():
    car_type_list = df['品牌'].value_counts().head().index
    dis_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16]
    reg = re.compile('\d公里')
    df_type = df['品牌']
    df_dis = df['里程'].map(lambda x: (float(x.strip('公里')) / 10000) if reg.findall(x) else float(x.strip('万公里')))
    df_price = df['价格'].map(lambda x: float(x.strip('万')))
    df_dis_price = pd.DataFrame(df_type)
    df_dis_price['里程'] = df_dis
    df_dis_price['价格'] = df_price
    df_dis_price = df_dis_price.set_index('品牌')

    ave_price_list = []
    for i in car_type_list:
        real_dis_list = []
        df_temp = df_dis_price.loc[i]
        tmp_ave_price = []
        for j in range(len(dis_list)):
            if j == 0:
                ave_price = df_temp[df_temp['里程'] < dis_list[j]]['价格'].mean()
                tmp_ave_price.append(ave_price)
                label = f'小于{dis_list[j]}万公里'
                real_dis_list.append(label)
            if j == len(dis_list) - 1:
                ave_price = df_temp[df_temp['里程'] >= dis_list[j]]['价格'].mean()
                tmp_ave_price.append(ave_price)
                label = f'大于{dis_list[j]}万公里'
                real_dis_list.append(label)
                break
            ave_price = df_temp[(df_temp['里程'] >= dis_list[j]) & (df_temp['里程'] < dis_list[j+1])]['价格'].mean()
            tmp_ave_price.append(ave_price)
            label = f'{dis_list[j]}~{dis_list[j+1]}万公里'
            real_dis_list.append(label)
        ave_price_list.append(tmp_ave_price)

    df_dis_price = pd.DataFrame(ave_price_list, index=car_type_list, columns=real_dis_list).T
    df_dis_price.plot(rot=30)
    plt.savefig('../results/price_dis_rel.png')
    plt.clf()


if __name__ == '__main__':
    draw_type_and_series()
    draw_price()
    draw_year_price()
    draw_distance_price()
