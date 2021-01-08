# -*-coding:utf8-*-
import requests
import json
import random
import time
import datetime
from concurrent.futures import ThreadPoolExecutor
import csv
import codecs
from requests import exceptions as rerr

thread_result = []

# urls = []
# 设置mid进行循环访问
mid_init = 1
# 无数据mid数量
bad_mid_num = 0
# 每个线程爬取最大用户数
# max_ok_num = 200
# poolSize = 1
# group_num = 1

ips = []


# 失败mid写入文件
def save_wrong_mid(thread_num, max_ok_num, mid, info_or_fans):
    info_url = 'http://api.bilibili.com/x/space/acc/info?mid=&jsonp=jsonp'
    fans_url = 'http://api.bilibili.com/x/relation/stat?vmid=&jsonp=jsonp'
    try:

        for i in mid:
            if i in info_url or fans_url:
                mid = mid.replace(i, "")
        data = {}
        data['thread_num'] = thread_num
        data['max_ok_num'] = max_ok_num
        data['start_mid'] = (thread_num - 1) * max_ok_num
        data['end_mid'] = mid
        if info_or_fans == 1:
            data['info_or_fans'] = 'info'
        elif info_or_fans == 2:
            data['info_or_fans'] = 'fans'
        else:
            mid += 1
            data['info_or_fans'] = 'thread_error'

        f = codecs.open('./poj_file/wrong_mid.csv', 'a', 'utf-8')  # 追加
        # 写入excel文件
        writer = csv.writer(f, delimiter=',', quotechar=' ', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(data.values())
        f.close()
        print('>>>>>>>>存入失败名录成功<<<<<<<<<')
    except Exception as err:
        print(err)


# 载入用户代理文件，将用户代理放入列表中

def LoadUserAgents(uafile):
    # print('----------->>初始化用户代理池。。。')
    uals = open(uafile, 'r')
    allus = uals.read()
    allus = allus.splitlines()
    return allus


uals = LoadUserAgents(r'./poj_file/user_agents.txt')


# 存入csv文件
def save_info_csv(info_data, fans_data):
    info_data['following'] = fans_data['following']
    info_data['follower'] = fans_data['follower']
    f = codecs.open('./poj_file/info.csv', 'a', 'utf-8')  # 追加
    try:
        # 写入excel文件
        writer = csv.writer(f, delimiter=',', quotechar=' ', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(info_data.values())
        f.close()
    except Exception as err:
        print(err)


def save_time_csv(alltime):
    f = codecs.open('./poj_file/runtime.csv', 'a', 'utf-8')
    try:
        writer = csv.writer(f, delimiter=',', quotechar=' ', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(alltime.values())
        f.close()
        print('>' * 10 + '本次操作载入成功' + '<' * 10)
    except Exception as err:
        print(err)


# 创建mid对应的urls,每500个为一组
def create_mid(mid_init, max_ok_num):
    info_urls = []
    fans_urls = []
    urls = {'info_urls': [], 'fans_urls': []}
    # print('初始化URL。。。')
    for m in range(mid_init, mid_init + max_ok_num):
        # 将对应用户信息url放入列表
        info_url = 'http://api.bilibili.com/x/space/acc/info?mid=%d&jsonp=jsonp' % m
        fans_url = 'http://api.bilibili.com/x/relation/stat?vmid=%d&jsonp=jsonp' % m
        info_urls.append(info_url)
        fans_urls.append(fans_url)
    urls['info_urls'] = info_urls
    urls['fans_urls'] = fans_urls
    return urls


def LoadIPs(ipfile, ips_num):
    ipf = open(ipfile, 'r')
    if ips_num < 0:  # 此时把文件Ip全部分配
        # print('----------->>初始化IP代理池。。。')
        allips = ipf.read()
        allips = allips.splitlines()
    else:
        allips = []
        for i in range(0, ips_num):
            allips.append(ipf.readline().strip('\n'))
    ipf.close()
    return allips


# 通过API，随机分配Ua和IP
def AlocIPUa_API(ip_num, file_name):
    time.sleep(1)
    # 正常API
    ip_api = 'http://120.79.85.144/index.php/api/entry?' \
             'method=proxyServer.tiqu_api_url&packid=0&' \
             'fa=0&dt=0&groupid=0&fetch_key=&qty=' + str(ip_num) + \
             '&time=100&port=1&format=txt&ss=3&css=&dt=0&ipport=1&pro=&city=&usertype=6'
    # 每日免费
    # ip_api = 'http://120.79.85.144/index.php/api/entry?' \
    #          'method=proxyServer.tiqu_api_url&packid=1&' \
    #          'fa=0&dt=0&groupid=0&fetch_key=&qty=' + str(ip_num) + \
    #          '&time=100&port=1&format=txt&ss=3&css=&dt=0&ipport=1&pro=&city=&usertype=6'

    ip = (requests.get(ip_api)).text
    fh = open(file_name, 'w')
    fh.write(ip + '\n')
    fh.close()


# 通过文件调用IP和UAL
def AlocIPUa_File(ips, uas, file_name, poolSize):
    # 随机选取一个用户代理，ip
    # 伪装进入网站
    ua = random.choice(uas)

    # 文件调用ip
    if len(ips) > 0:
        print('----->>ip池还有存货')
        rand_i = random.choice(range(0, len(ips)))
        ip = str(ips[rand_i])
        ips.pop(rand_i)
    else:
        print('----->>ip池空，即将重新分配ip')
        AlocIPUa_API(5, file_name)
        ips_t = LoadIPs(file_name, 5)
        for item in ips_t:
            ips.append(item)
        rand_i = random.choice(range(0, len(ips)))
        ip = str(ips[rand_i])
        ips.pop(rand_i)
    # print('----->>用户代理选用：' + str(ua))
    print('----->>IP代理选用：' + str(ip))
    work_maybe = {'headers': {'User-Agent': ua},
                  'proxies': {'http': 'http://' + ip},
                  'Connection': 'close'}
    return work_maybe


# 获取用户基本信息
def get_info(thisurl, work_maybe, thread_num, wrong_time, poolSize):
    proxy = work_maybe['proxies']
    header = work_maybe['headers']
    if wrong_time < 2:
        try:
            info_url = requests.get(thisurl, headers=header, proxies=proxy, timeout=(5, 15))
            info_data = info_url.text
            jsDict = json.loads(info_data)
            statusJson = jsDict['data'] if 'data' in jsDict.keys() else False
            if statusJson:
                info_dic = {}
                jsData = jsDict['data']
                mid = jsData['mid']
                name = jsData['name']
                sex = jsData['sex']
                face = jsData['face']
                birthday = jsData['birthday'] if 'birthday' in jsData.keys() else 'nobirthday'
                sign = jsData['sign']
                level = jsData['level']
                OfficialVerifyType = jsData['official']['type']
                OfficialVerifyDesc = jsData['official']['desc']
                officialTitle = jsData['official']['title'] if 'title' in jsData['official'].keys() else 'notitles'
                vipType = jsData['vip']['type']
                vipStatus = jsData['vip']['status']
                coins = jsData['coins']

                info_dic.update({'mid': mid, 'name': name, 'sex': sex, 'face': face,
                                 'birthday': birthday, 'sign': sign, 'level': level,
                                 'OfficialVerifyType': OfficialVerifyType,
                                 'OfficialVerifyDesc': OfficialVerifyDesc,
                                 'officialTitle': officialTitle,
                                 'vipType': vipType, 'vipStatus': vipStatus,
                                 'coins': coins})

                print('线程号:' + str(thread_num) + '->' + str(jsData['mid']) + ' : ' + jsData['name'])

                return info_dic
            else:
                print('no data now')
        except (rerr.HTTPError, rerr.ProxyError, rerr.ConnectTimeout, rerr.ConnectionError) as e:
            print(str(e) + '线程' + str(thread_num) + '获取第一类异常' + str(thisurl) + '基本信息异常')
            # 存入信息获取失败mid
            wrong_time += 1
            time.sleep(2)
            print('线程' + str(thread_num) + '第' + str(wrong_time + 1) + '次重连')
            work_maybe.clear()
            work_maybe.update(AlocIPUa_File(ips, uals, './poj_file/info_catch_ips.txt', poolSize))
            get_info(thisurl, work_maybe, thread_num, wrong_time, poolSize)

    else:
        print('重连失败,存入失败名录')
        save_wrong_mid(thread_num, max_ok_num, thisurl, 1)


# 获取粉丝和关注
def get_fans(thisurl, work_maybe, thread_num, wrong_time, poolSize):
    proxy = work_maybe['proxies']
    header = work_maybe['headers']
    result = {}
    if wrong_time < 2:
        try:
            fans_url = requests.get(thisurl, headers=header, proxies=proxy, timeout=(15, 15))
            fans_data = fans_url.text
            # if fans_url.status_code == 200:
            jsDict = json.loads(fans_data)
            statusJson = jsDict['data'] if 'data' in jsDict.keys() else False
            if statusJson:
                jsData = jsDict['data']
                result.update({'following': jsData['following'], 'follower': jsData['follower']})
                return result
        except (rerr.HTTPError, rerr.ProxyError, rerr.ConnectTimeout, rerr.ConnectionError) as e:
            print(str(e) + '线程' + str(thread_num) + '获取第一类异常' + str(thisurl) + '粉丝数异常')
            wrong_time += 1
            time.sleep(2)
            print('线程' + str(thread_num) + '第' + str(wrong_time) + '次重连')
            work_maybe.clear()
            work_maybe.update(AlocIPUa_File(ips, uals, './poj_file/fans_catch_ips.txt', poolSize))
            get_fans(thisurl, work_maybe, thread_num, wrong_time, poolSize)
    else:
        print('重连失败,存入失败名录')
        save_wrong_mid(thread_num, max_ok_num, thisurl, 2)


# 每个线程处理一组数据
def thread_one(t, ips, max_ok_num, poolSize):
    print('-------->>线程号:' + str(t) + '  爬取数据量为：' + str(max_ok_num))
    wrong_time = 0
    # print('选用ip代理')
    # time1 = time.time()
    user_count = 0

    # 每个线程的消息盒子，存放开始时间、结束时间、预计完成用户数，实际完成数、错误用户数，爬取准确率
    thread_info = {
        '线程号': t,
        '开始时间': '',
        '结束时间': '',
        '共耗时': '',
        '预计爬取用户数': '',
        '实际完成数': '',
        '准确率': '',

    }
    thread_info['预计爬取用户数'] = max_ok_num
    time11 = datetime.datetime.now().strftime('%H:%M:%S')
    time1 = time.time()
    thread_info['开始时间'] = time11

    try:
        work_maybe = AlocIPUa_File(ips, uals, './poj_file/ips.txt', poolSize)
        urls = create_mid((t - 1) * max_ok_num, max_ok_num)
        for i in range(0, len(urls['info_urls'])):
            try:
                info_data = get_info(urls['info_urls'][i], work_maybe, t, wrong_time, poolSize)
                fans_data = get_fans(urls['fans_urls'][i], work_maybe, t, wrong_time, poolSize)
                if info_data and fans_data:
                    save_info_csv(info_data, fans_data)
                    user_count += 1
                else:
                    continue
            except (Exception) as e:
                print('>>>>>>>>>>>>>>>>>>>>>>ip已失效，即将重新分配<<<<<<<<<<<<<<<<<<<')
                work_maybe.clear()
                work_maybe.update(AlocIPUa_File(ips, uals, './poj_file/ips_catch.txt', poolSize))
                continue

    except (Exception) as e:
        print('在thread_one中外层分配mid或headers出现异常：')
        print(e)

    time22 = datetime.datetime.now().strftime('%H:%M:%S')
    time2 = time.time()
    thread_info['实际完成数'] = user_count
    thread_info['结束时间'] = time22
    thread_info['准确率'] = str((user_count / max_ok_num) * 100) + '%'

    one_thread_time = time2 - time1
    thread_info['共耗时'] = round(one_thread_time, 5)
    print('-------->>线程号:' + str(t) + ' |总计用时：' + str(round(one_thread_time, 5)) + '秒')

    # 返回线程信息
    global thread_result
    thread_result.insert(thread_info['线程号'] - 1, thread_info)


def StartCraw(user_option):
    print('>' * 10 + '测试时间：' + str(datetime.datetime.now()) + '<' * 10 + '\n')
    poolSize = user_option['poolSize'] + 1
    group_num = user_option['group_num']
    max_ok_num = user_option['max_ok_num']
    other_thread = user_option['other_thread']
    alltime = {}
    thread_task = []
    try:
        pool_thread = ThreadPoolExecutor(poolSize)
        AlocIPUa_API(poolSize, './poj_file/ips_api.txt')
        ips = LoadIPs("./poj_file/ips_api.txt", poolSize)
        time_start = time.time()
        test_time = datetime.datetime.now()

        # 若2000可整除线程数
        if other_thread == 0:
            for i in range(1, group_num + 1):
                print('创建线程')
                thread_task.append(pool_thread.submit(thread_one, i, ips, max_ok_num, poolSize))
        # 不能整除则多余的数据平分给前几个线程处理
        else:
            for i in range(1, group_num+1):
                if i<=other_thread:
                    print('创建线程')
                    thread_task.append(pool_thread.submit(thread_one, i, ips, max_ok_num+1, poolSize))
                else:
                    thread_task.append(pool_thread.submit(thread_one, i, ips, max_ok_num, poolSize))

        pool_thread.shutdown(wait=True)
        time_end = time.time()
        alltime['test_time'] = test_time
        alltime['time_start'] = time_start
        alltime['time_end'] = time_end
        alltime['sub_time'] = time_end - time_start
        alltime['threads_num'] = poolSize
        alltime['users_num'] = group_num * max_ok_num + other_thread
        alltime['max_ok_num'] = max_ok_num
        alltime['group_num'] = group_num
        print('耗费时间：' + str(alltime['sub_time']))

        last_str = ''
        user_count = 0
        for tinfo in thread_result:
            t_string = '\n' + '-' * 50 + '\n' + \
                       '线程号:' + str(tinfo['线程号']) + \
                       ' | 耗时:' + str(tinfo['共耗时']) + '秒' +\
                       '\n预计爬取用户数:' + str(tinfo['预计爬取用户数']) + \
                       ' | 实际完成数:' + str(tinfo['实际完成数']) + \
                       ' | 准确率:' + str(tinfo['准确率'])
        # '\n开始时间:' + str(tinfo['开始时间']) + \
        # ' | 结束时间:' + str(tinfo['结束时间']) + \
            user_count += tinfo['实际完成数']
            last_str += t_string

        last_str += '\n' + '-' * 50 + '\n' + \
                    '总线程数：' + str(alltime['group_num']) + \
                    '，  总计预爬取用户数：' + str(alltime['users_num']) + \
                    '，  实际爬取总数：' + str(user_count + other_thread) + \
                    '，  准确率：' + str((user_count / alltime['users_num']) * 100) + '%' + \
                    '，  总耗时：' + str(round(alltime['sub_time'], 5)) + '秒' + \
                    '\n' + '-' * 45 + '\n'

        print(last_str)
        
        # 存入时间日志
        alltime['finfis']=user_count / alltime['users_num']
        user_count = 0
        save_time_csv(alltime)



    except Exception as e:
        print(e)


def overSound():
    import winsound
    for i in range(0, 3):
        duration = 300  # millisecond
        freq = 440  # Hz
        winsound.Beep(freq, duration)
        time.sleep(0.2)


if __name__ == "__main__":
    # 主函数
    user_option = {}
    user_option['poolSize'] = 1
    user_option['group_num'] = 1
    user_option['max_ok_num'] = 1
    user_option['other_thread'] = 0
    StartCraw(user_option)
    # import os

    # os.startfile(r'info.csv')
    # os.startfile(r'./poj_file/runtime.csv')
    print('------>>结束<<------')
    overSound()
