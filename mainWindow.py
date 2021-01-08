import time
from userCraw import StartCraw
from userShow import showinfo
from userCart import showWindow
from threadCart import drawThreadCart
import crawWindow


def craw_chose_show():
    print(' ' * 30 + '=' * 20 + '请按照提示输入' + '=' * 20 + '\n')
    user_option = crawWindow.go()

    StartCraw(user_option)


# 不同线程数爬取效率对比图
def thread_cart_chose_show():
    print(' ' * 30 + '>' * 10 + ' 不同线程数爬取效率对比图 ' + '<' * 10 + '\n')
    drawThreadCart()


# B站用户信息统计图
def userinfo_cart_chose_show():
    print(' ' * 30 + '>' * 10 + ' B站用户信息统计图 ' + '<' * 10 + '\n')
    showWindow()


# B站用户信息概览
def userinfo_chose_show():
    print(' ' * 30 + '>' * 10 + ' B站用户信息概览(500名) ' + '<' * 10 + '\n')
    showinfo()


# 退出程序
def exit_chose_show():
    print(' ' * 30 + '>' * 10 + ' 返回客户端 ' + '<' * 10 + '\n')
    time.sleep(1)
    exit(0)


def menu_show():
    print(' ' * 30 + '*' * 23 + '  多线程爬虫系统  ' + '*' * 23)
    print(' ' * 30 + '| ' + '     |' + ' ' * 55 + '|')
    print(' ' * 30 + '| ' + ' 请  |' + ' ' * 13 + '1:多线程爬虫体验' + ' ' * 26 + '|')
    print(' ' * 30 + '| ' + ' 选  |' + ' ' * 13 + '2:不同线程数爬取效率对比统计图' + ' ' * 12 + '|')
    print(' ' * 30 + '| ' + ' 择  |' + ' ' * 13 + '3:B站用户信息统计图  ' + ' ' * 21 + '|')
    print(' ' * 30 + '| ' + ' 功  |' + ' ' * 13 + '4:B站用户信息概览(500名)  ' + ' ' * 16 + '|')
    print(' ' * 30 + '| ' + ' 能  |' + ' ' * 13 + '5:退出程序' + ' ' * 32 + '|')
    print(' ' * 30 + '| ' + '     |' + ' ' * 55 + '|')
    print(' ' * 30 + '*' * 64 + '\n')
    while True:
        choic = input('>' * 10 + '您的选择是(输入后回车)：')
        if choic == '1':
            craw_chose_show()
            break

        elif choic == '2':
            thread_cart_chose_show()
            break

        elif choic == '3':
            userinfo_cart_chose_show()
            break

        elif choic == '4':
            userinfo_chose_show()
            break

        elif choic == '5':
            exit_chose_show()
            break

        else:
            print('>' * 10 + ' 无此选项，请重新输入 ' + '<' * 10 + '\n')

def work():
    while True:
        menu_show()

if __name__ == "__main__":
    work()
