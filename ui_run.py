from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from PyQt5.QtGui import *
import sys
from userCraw import StartCraw
from crawWindow import con_ok_num
import mainWindow
import time
import os
import csv

# import icons_rc

# UI--Logic分离
ui, _ = loadUiType('bilibili_ui.ui')


class EmittingStr(QObject):
    textWritten = pyqtSignal(str)  # 定义一个发送str的信号

    def write(self, text):
        self.textWritten.emit(str(text))


# noinspection PyArgumentList
class MainApp(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        self.crawResult = ''
        self.viewModel = QStandardItemModel(0, 10)
        self.viewModel.setHorizontalHeaderLabels(['id', '姓名', '性别', '等级', '生日',
                                                  'VIP类型', '播放量', '点赞数', '关注数', '粉丝数'])
        self.showTable(0, 10000)

        self.tableView.setModel(self.viewModel)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # 提示小窗口
        op = QGraphicsOpacityEffect()
        op.setOpacity(0.8)
        self.rightBox.setGraphicsEffect(op)
        self.rightBox.setAutoFillBackground(True)
        self.rightBox.setVisible(False)

        # 将输出重定向到textBrowser中
        self.temp = sys.stdout
        sys.stdout = EmittingStr(textWritten=self.outputWritten)
        # sys.stderr = EmittingStr(textWritten=self.outputWritten)
        self.someTips()
        self.btnConnect()

    # 表格显示和用户数据
    def showTable(self, startpos, endpos):
        count = 0
        item = []
        f = open('./other_file/b.csv', 'r', encoding='utf-8')  # 追加
        freader = csv.reader(f)
        for i in freader:
            count += 1
            if count >= startpos:
                for r in range(0, 10):
                    item.append(QStandardItem(i[r]))
                self.viewModel.appendRow(item)
                item.clear()

            if count >= endpos:
                break

    # 显示用户预展示范围内的数据
    def showTable_user(self):
        self.viewModel.clear()
        self.viewModel.setHorizontalHeaderLabels(['id', '姓名', '性别', '等级', '生日',
                                                  'VIP类型', '播放量', '点赞数', '关注数', '粉丝数'])
        startpos = 0
        endpos = 10000
        if self.start_edit.text() and self.end_edit.text():
            startpos = int(self.start_edit.text())
            endpos = int(self.end_edit.text())
        self.showTable(startpos, endpos)
        self.tableView.setModel(self.viewModel)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    # 输出重定向到textbrowser
    def outputWritten(self, text):
        cursor = self.print_browser.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.print_browser.setTextCursor(cursor)
        self.print_browser.ensureCursorVisible()

    # 获取用户输入
    def getInput(self):
        user_input = {}
        if self.poolSize_edit.text() and self.threadSum_edit.text() and self.soloWork_edit.text():
            user_input['poolSize'] = int(self.poolSize_edit.text())
            user_input['group_num'] = int(self.threadSum_edit.text())
            user_input['max_ok_num'] = int(self.soloWork_edit.text())
            user_input['other_thread'] = 0
            QMessageBox.about(self, '开始运行', '总线程数：' + str(user_input['group_num']) +
                              '\n线程池大小：' + str(user_input['poolSize']) +
                              '\n单线程爬取数据量：' + str(user_input['max_ok_num']))
            return user_input
        else:
            print('用户输入不完整')
        pass

    # 传递输入到爬虫程序中
    # 开始按钮槽函数
    def startCraw(self):
        user_input = self.getInput()

        self.start_btn.setEnabled(False)
        self.poolSize_edit.setEnabled(False)
        self.threadSum_edit.setEnabled(False)
        self.soloWork_edit.setEnabled(False)
        self.dosRun_btn.setEnabled(False)
        self.start_btn.setText('运行中,请稍等。。')
        qssStyle = '''
                    QPushButton{background-color: rgb(200, 195, 235);
                        color:white;
                        border-radius:7px;}
    
            '''
        self.start_btn.setStyleSheet(qssStyle)

        self.straw_thread = strawThread(user_input=user_input)
        self.straw_thread.resSignal.connect(self.ResSlotPrint)
        self.straw_thread.start()

    # 结束爬取输出
    def ResSlotPrint(self):
        QMessageBox.about(self, '结束任务', '爬虫结束！')
        self.start_btn.setEnabled(True)
        self.poolSize_edit.setEnabled(True)
        self.threadSum_edit.setEnabled(True)
        self.soloWork_edit.setEnabled(True)
        self.dosRun_btn.setEnabled(True)
        self.start_btn.setText('开始爬取')
        qssStyle = '''
                QPushButton{background-color: rgb(137, 195, 235);
                            color:rgb(25, 68, 142);
                            border-radius:7px;}
                QPushButton:hover{
                            color:rgb(243, 152, 0);
                            background-color:  qlineargradient(spread:pad, x1:0.517, y1:0, x2:0.517, y2:1, stop:0 rgba(155, 168, 141,255), stop:0.505682 rgba(34, 58, 112,255), stop:1 rgba(29, 29, 29, 255));
                            border-color:#2d89ef;
                            border-width:2px;}
    
            '''
        self.start_btn.setStyleSheet(qssStyle)

    # def timerPrint(self):
    #     loop = QEventLoop()
    #     QTimer.singleShot(1000, loop.quit)
    #     loop.exec_()

    # 信号与槽通信
    def btnConnect(self):
        self.start_btn.clicked.connect(self.startCraw)
        self.thread_btn.clicked.connect(self.showCrawCartClk)
        # self.start_btn.clicked.connect(self.timerPrint)
        self.dosRun_btn.clicked.connect(self.runDos)
        self.userCart_btn.clicked.connect(self.showUserInfoSelc)
        self.selecCls_btn.clicked.connect(self.clsUserinfoSelc)
        self.sex_rdo.toggled.connect(lambda: self.rdoSlcImg(self.sex_rdo))
        self.level_rdo.toggled.connect(lambda: self.rdoSlcImg(self.level_rdo))
        self.bth_rdo.toggled.connect(lambda: self.rdoSlcImg(self.bth_rdo))
        self.vip_rdo.toggled.connect(lambda: self.rdoSlcImg(self.vip_rdo))
        self.play_rdo.toggled.connect(lambda: self.rdoSlcImg(self.play_rdo))
        self.good_rdo.toggled.connect(lambda: self.rdoSlcImg(self.good_rdo))
        self.fans_rdo.toggled.connect(lambda: self.rdoSlcImg(self.fans_rdo))
        self.clear_btn.clicked.connect(self.clcBrowser)
        self.save_btn.clicked.connect(self.saveBrowser)
        self.showData_btn.clicked.connect(self.showTable_user)

    # 清空输出页内容
    def clcBrowser(self):
        self.print_browser.clear()
        QMessageBox.about(self, '清空信息板', '已清空！')

    # 导出输出页内容
    def saveBrowser(self):
        try:
            StrText = self.print_browser.toPlainText()
            qS = str(StrText)
            f = open('./poj_file/note.txt', 'w')
            f.write('{}'.format(qS))
            f.close()
            QMessageBox.about(self, '存储成功', '请到当前目录 ./poj_ile/note.txt 中查看')
        except Exception as e:
            print(e)

    def showImgAndWeb(self, img_path, web_path):
        img_path = img_path
        # 加载图片,并自定义图片展示尺寸
        image = QPixmap(img_path).scaled(511, 391)
        # 显示图片
        self.imgLabel.setPixmap(image)

        # 加载外部页面，调用

        # os.system("gnome-terminal -e 'ls'")
        os.system(web_path)

    # 显示爬虫效率预览图
    def showCrawCartClk(self):
        self.showImgAndWeb('./img/threadCart.png', "threadCart.html")

    # 显示用户信息预览选择框
    def showUserInfoSelc(self):
        # self.imgLabel.setVisible(False)
        qssStly = '''
                color:rgb(255, 255, 255);
                background-color: rgb(90, 121, 186);
                border-radius:20px;
                '''
        self.rightBox.setStyleSheet(qssStly)

        self.rightBox.setVisible(True)
        OrigX = 0
        ChangeX = 121
        # 动画弹出效果
        startWidth = OrigX
        endWidth = ChangeX
        animation = QPropertyAnimation(self.rightBox, b'geometry', self)
        animation.setDuration(500)
        animation.setStartValue(QRect(330, 160, startWidth, 211))
        animation.setEndValue(QRect(330, 160, endWidth, 211))

        animation.start()

    # 关闭选择框
    def clsUserinfoSelc(self):
        self.rightBox.setVisible(False)

    # 根据单选打开图片
    def rdoSlcImg(self, btn):
        if btn.text() == '性别分布':
            if btn.isChecked() == True:
                self.showImgAndWeb('./img/sex_pie.png', 'sex_pie.html')

        if btn.text() == '用户等级':
            if btn.isChecked() == True:
                self.showImgAndWeb('./img/level_pie.png', 'level_pie.html')

        if btn.text() == '用户生日':
            if btn.isChecked() == True:
                self.showImgAndWeb('./img/btd_bar.png', 'btd_bar.html')

        if btn.text() == 'VIP类型':
            if btn.isChecked() == True:
                self.showImgAndWeb('./img/vip_pie.png', 'vip_pie.html')

        if btn.text() == '播放数':
            if btn.isChecked() == True:
                self.showImgAndWeb('./img/ace_pie.png', 'ace_pie.html')

        if btn.text() == '获赞数':
            if btn.isChecked() == True:
                self.showImgAndWeb('./img/likes_pie.png', 'likes_pie.html')

        if btn.text() == '粉丝数':
            if btn.isChecked() == True:
                self.showImgAndWeb('./img/fans_pie.png', 'fans_pie.html')

    # DOS端使用体验
    def runDos(self):
        sys.stdout = self.temp
        QMessageBox.about(self, 'DOS端体验', '请关注程序后侧终端界面！')
        import os
        # os.system("gnome-terminal -e 'ls'")
        os.system("mainWindow.py")

    # 一些提示信息
    def someTips(self):
        self.threadSum_edit.setToolTip('请填入小于200的正整数')
        self.soloWork_edit.setToolTip('请填入小于2000的正整数')
        self.poolSize_edit.setToolTip('请填入正整数，尽量大于等于总线程数')
        self.thread_btn.setToolTip('点击打开对应web页面，右侧为预览图')
        self.userCart_btn.setToolTip('点击打开对应web页面，右侧为预览图')
        self.dosRun_btn.setToolTip('若爬虫任务进行中则无法点击')
        self.clear_btn.setToolTip('清空信息板')
        self.save_btn.setToolTip('储存日志')
        self.showData_btn.setToolTip('默认显示一万条用户数据')


# 自定义线程，防止爬取时程序死
class strawThread(QThread):
    resSignal = pyqtSignal(str)

    def __init__(self, user_input=None):
        super(strawThread, self).__init__()
        self.is_on = True
        self.user_input = user_input

    def run(self):
        self.crawResult = StartCraw(self.user_input)
        self.resSignal.emit('爬取结束')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainApp()
    main.show()
    sys.exit(app.exec_())
