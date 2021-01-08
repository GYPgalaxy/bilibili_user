# -*- coding : utf-8 -*-
import pandas as pd
from plotly.offline import plot
import plotly.graph_objs as go
import re

# 读取b站用户信息文件


fh = pd.read_csv('./other_file/b.csv', encoding='utf-8')


# 绘制性别比例饼状图
def sex_pie():
    user_sex = fh.sex.tolist()
    user_man_count = user_sex.count('男')
    user_woman_count = user_sex.count('女')
    user_sb_count = user_sex.count('保密')

    data = go.Pie(
        labels=['男', '女', '保密'],
        values=[user_man_count, user_woman_count, user_sb_count],
        hoverinfo='label+percent+value',
        textinfo='percent,label',  # textinfo = 'value',
        textfont=dict(size=15, color='white'),
        marker=dict(
            line=dict(color='#000000', width=2))
    )
    mlayout = dict(title='前10万用户性别占比',
                   )

    fig = dict(data=data, layout=mlayout)
    plot(fig, filename='./userCartHTML/sex_pie.html')


# 绘制用户等级饼状图
def level_pie():
    user_level = fh.level.tolist()
    level_1 = user_level.count(1)
    level_2 = user_level.count(2)
    level_3 = user_level.count(3)
    level_4 = user_level.count(4)
    level_5 = user_level.count(5)
    level_6 = user_level.count(6)

    data = go.Pie(
        labels=['1级', '2级', '3级', '4级', '5级', '6级'],
        values=[level_1, level_2, level_3, level_4, level_5, level_6],

        hoverinfo='label+percent+value',
        textinfo='percent,label',  # textinfo = 'value',
        textfont=dict(size=15, color='white'),
        marker=dict(
            line=dict(color='#000000', width=2))
    )
    mlayout = dict(title='前10万用户等级分布',
                   )
    fig = dict(data=data, layout=mlayout)

    plot(fig, filename='./userCartHTML/level_pie.html')


# 绘制VIP等级饼状图
def vip_pie():
    user_vip = fh.vtype.tolist()
    vip_0 = user_vip.count(0)
    vip_1 = user_vip.count(1)
    vip_2 = user_vip.count(2)

    v_labels = ['非VIP用户', '包月VIP用户', '包年VIP用户']
    v_values = [vip_0, vip_1, vip_2]

    data = go.Pie(
        labels=v_labels,
        values=v_values,

        hoverinfo='label+percent+value',
        textinfo='percent,label',  # textinfo = 'value',
        textfont=dict(size=15, color='white'),
        marker=dict(
            line=dict(color='#000000', width=2))

    )
    mlayout = dict(title='前10万用户VIP等级分布',
                   )
    fig = dict(data=data, layout=mlayout)
    plot(fig, filename='./userCartHTML/vip_pie.html')


# 绘制生日条形图
def btd_hist():
    user_btd = fh.birthday.tolist()
    btd_m = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # 统计各月份数量
    for btd in user_btd:
        if re.match('1月', btd):
            btd_m[0] += 1
        elif re.match('2月', btd):
            btd_m[1] += 1
        elif re.match('3月', btd):
            btd_m[2] += 1
        elif re.match('4月', btd):
            btd_m[3] += 1
        elif re.match('5月', btd):
            btd_m[4] += 1
        elif re.match('6月', btd):
            btd_m[5] += 1
        elif re.match('7月', btd):
            btd_m[6] += 1
        elif re.match('8月', btd):
            btd_m[7] += 1
        elif re.match('9月', btd):
            btd_m[8] += 1
        elif re.match('10月', btd):
            btd_m[9] += 1
        elif re.match('11月', btd):
            btd_m[10] += 1
        elif re.match('12月', btd):
            btd_m[11] += 1

    data = go.Bar(
        x=['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月', ],
        y=btd_m,
        marker=dict(
            color=["#006e54", "#00a381", "#38b48b", "#00a497", "#80aba9",
                   "#5c9291", "#478384", "#43676b", "#80989b", "#2c4f54",
                   "#1f3134", "#47585c"],
        )
    )
    mlayout = dict(title='前10万用户生日月份分布',
                   )
    fig = dict(data=data, layout=mlayout)
    plot(fig, filename='./userCartHTML/btd_bar.html')


# 播放数饼状图
def ace_pie():
    user_ace = fh.archive.tolist()
    ace_num = [0, 0, 0, 0, 0, 0]
    for ace in user_ace:
        if ace == 0:
            ace_num[0] += 1
        elif 0 < ace < 10000:
            ace_num[1] += 1
        elif 10000 < ace < 100000:
            ace_num[2] += 1
        elif 100000 < ace < 1000000:
            ace_num[3] += 1
        elif 1000000 < ace < 5000000:
            ace_num[4] += 1
        elif 5000000 < ace:
            ace_num[5] += 1

    data = go.Pie(
        labels=['0', '0~1万', '1万~10万', '10万~100万', '100万~500万', '500万以上'],
        values=ace_num,

        hoverinfo='label+percent+value',
        textinfo='percent,label',  # textinfo = 'value',
        textfont=dict(size=15, color='white'),
        # marker=dict(
        #     line=dict(color='#000000', width=2))

    )
    mlayout = dict(title='前10万用户作品播放数量分布',
                   )
    fig = dict(data=data, layout=mlayout)
    plot(fig, filename='./userCartHTML/ace_pie.html')


# 获赞数饼状图
def likes_pie():
    user_likes = fh.likes.tolist()
    likes_num = [0, 0, 0, 0, 0, 0]
    for likes in user_likes:
        if likes == 0:
            likes_num[0] += 1
        elif 0 < likes < 500:
            likes_num[1] += 1
        elif 500 < likes < 2000:
            likes_num[2] += 1
        elif 2000 < likes < 5000:
            likes_num[3] += 1
        elif 5000 < likes < 10000:
            likes_num[4] += 1
        elif 10000 < likes:
            likes_num[5] += 1

    data = go.Pie(
        labels=['0', '0~500', '500~2000', '2000~5000', '5000~1万', '1万以上'],
        values=likes_num,

        hoverinfo='label+percent+value',
        textinfo='percent,label',  # textinfo = 'value',
        textfont=dict(size=15, color='white'),
        # marker=dict(
        #     line=dict(color='#000000', width=2))

    )
    mlayout = dict(title='前10万用户作品被赞总数分布',
                   )
    fig = dict(data=data, layout=mlayout)
    plot(fig, filename='./userCartHTML/likes_pie.html')


# 粉丝数饼状图
def fans_pie():
    user_fans = fh.follower.tolist()
    fans_num = [0, 0, 0, 0, 0, 0]
    for fans in user_fans:
        if 0 < fans < 10:
            fans_num[0] += 1
        elif 10 < fans < 1000:
            fans_num[1] += 1
        elif 1000 < fans < 5000:
            fans_num[2] += 1
        elif 5000 < fans < 10000:
            fans_num[3] += 1
        elif 10000 < fans < 100000:
            fans_num[4] += 1
        elif 100000 < fans:
            fans_num[5] += 1

    data = go.Pie(
        labels=['0~10', '10~1000', '1000~5000', '5000~1万', '1万~10万', '10万以上'],
        values=fans_num,

        hoverinfo='label+percent+value',
        textinfo='percent,label',  # textinfo = 'value',
        textfont=dict(size=15, color='white'),
        # marker=dict(
        #     line=dict(color='#000000', width=2))

    )
    mlayout = dict(title='前10万用户粉丝数数占比',
                   )
    fig = dict(data=data, layout=mlayout)
    plot(fig, filename='./userCartHTML/fans_pie.html')


def showWindow():
    print('>' * 10 + ' B站用户信息统计图 ' + '<' * 10 + '\n')
    print('<' * 5 + '选择要查看的统计图(输入后回车)：\n')
    print(' ' * 10 + '1:性别分布')
    print(' ' * 10 + '2:用户等级分布')
    print(' ' * 10 + '3:用户生日分布')
    print(' ' * 10 + '4:VIP类型统计')
    print(' ' * 10 + '5:播放数分布')
    print(' ' * 10 + '6:获赞数分布')
    print(' ' * 10 + '7:粉丝数分布\n')

    while True:
        choic = input('>' * 5 + '您的选择是(输入后回车)：')
        if choic == '1':
            sex_pie()
            print('对应HTML文件已存入当前目录下 userCartHTML 文件夹中\n')
            break

        elif choic == '2':
            level_pie()
            print('对应HTML文件已存入当前目录下 userCartHTML 文件夹中\n')
            break

        elif choic == '3':
            btd_hist()
            print('对应HTML文件已存入当前目录下 userCartHTML 文件夹中\n')
            break

        elif choic == '4':
            vip_pie()
            print('对应HTML文件已存入当前目录下 userCartHTML 文件夹中\n')
            break

        elif choic == '5':
            ace_pie()
            print('对应HTML文件已存入当前目录下 userCartHTML 文件夹中\n')
            break
        elif choic == '6':
            likes_pie()
            print('对应HTML文件已存入当前目录下 userCartHTML 文件夹中\n')
            break
        elif choic == '7':
            fans_pie()
            print('对应HTML文件已存入当前目录下 userCartHTML 文件夹中\n')
            break
        else:
            print('>' * 5 + ' 无此选项，请重新输入 ' + '<' * 10 + '\n')


if __name__ == '__main__':
    showWindow()
