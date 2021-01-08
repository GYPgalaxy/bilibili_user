from userCraw import StartCraw
import time

user_option = {}


def show():
    while True:
        try:
            user_option['poolSize'] = eval(input(' ' * 39 + '输入线程池大小(即同时运行线程数，1~50)：'))
            user_option['group_num'] = eval(input(' ' * 47 + '输入总线程数(1~100)：'))
            # user_option['group_num'] = user_option['poolSize']

            if isinstance(user_option['poolSize'], int) and isinstance(user_option['group_num'], int):
                break
        except:
            print('>' * 20 + ' 请正确输入! ' + '<' * 20)
            pass
        finally:
            return user_option


# 确定单线程爬取数据量
def con_ok_num(user_option):
    group_num = int(user_option['group_num'])
    poolSize = int(user_option['poolSize'])
    # 如果能被2000整除
    if 2000 % group_num == 0:
        max_ok_num = int(2000 / group_num)
        other_thread = 0
    else:
        max_ok_num = int(2000 / group_num)
        other_thread = 2000 % group_num

    user_option['max_ok_num'] = max_ok_num
    user_option['other_thread'] = other_thread
    user_option['group_num'] = group_num
    user_option['poolSize'] = poolSize
    return user_option


def go():
    return con_ok_num(show())


if __name__ == "__main__":
    endnow = '1'
    while endnow == '1':
        StartCraw((go()))
        endnow = input('继续？')
