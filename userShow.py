import prettytable as pt
import csv
def showinfo():
    tb = pt.PrettyTable()
    tb.field_names = ['ID', '昵称', '性别', '用户等级', '生日', 'VIP类型'
        , '播放数', '获赞数', '关注数', '粉丝数']
    f = open('./other_file/b.csv', 'r',encoding='utf-8')  # 追加
    freader = csv.reader(f)
    count = 0
    for i in freader:
        count += 1
        if count > 500:
            break
        tb.add_row(i)
    print(tb)

if __name__ == '__main__':
    showinfo()
    pass