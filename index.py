import sys, os
from PIL import Image
import imagehash
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog,QWidget
from PyQt5.QtWidgets import QTableWidgetItem as item
import mainwin
import sim4, unsim3

files, sims, compare_hash = [], [], 0
os.chdir('pics')

class MainWindow():
    def __init__(self):
        app = QApplication(sys.argv)
        win = QMainWindow()
        self.ui = mainwin.Ui_MainWindow()
        self.ui.setupUi(win)

        self.clicked_open()
        self.clicked_index()
        self.click_display()

        self.sim_win4 = QWidget()
        self.unsim_win3 = QWidget()
        self.sim4_win = sim4.Ui_Form()
        self.sim4_win.setupUi(self.sim_win4)
        self.unsim3_win = unsim3.Ui_Form()
        self.unsim3_win.setupUi(self.unsim_win3)

        win.show()
        sys.exit(app.exec())

    def open(self):
        global files, compare_hash, sims
        files, sims = [], []
        file, type = QFileDialog.getOpenFileName(QWidget(), '打开文件','./pics',("Images (*.png *.jpg *.bmp);;All File(*)"))
        compare_hash = imagehash.phash(Image.open(file), hash_size=8)
        pixmap = QtGui.QPixmap(file)
        self.ui.label.setPixmap(pixmap)
        num = file[-7]
        for i in os.listdir():
            if num == i[-7]:
                files.append(i)

    def clicked_open(self):
        self.ui.open_btn.clicked.connect(self.open)

    def index(self):
        global files, sims
        for name in files:
            cur_hash = imagehash.phash(Image.open(name), hash_size=8)
            sim = 1 - (compare_hash - cur_hash)/len(cur_hash.hash)**2
            if (name, sim) not in sims:
                sims.append((name, sim))
        sims = sorted(sims, key=lambda i:i[1], reverse=True)

        for i in range(7):
            for j in range(2):
                self.ui.tableWidget.setItem(i , j, item(str(sims[i][j])))

        # 缩小图像尺寸以显示
        ims = []
        for i in range(7):
            im = Image.open(sims[i][0])
            pixmap = QtGui.QPixmap(sims[i][0]).scaled(int(im.size[0]*0.65), int(im.size[1]*0.65))
            ims.append(pixmap)


        # 4 幅相似的窗口
        self.sim4_win.label.setPixmap(QtGui.QPixmap(ims[0]))
        self.sim4_win.label_2.setPixmap(QtGui.QPixmap(ims[1]))
        self.sim4_win.label_3.setPixmap(QtGui.QPixmap(ims[2]))
        self.sim4_win.label_4.setPixmap(QtGui.QPixmap(ims[3]))
        self.sim4_win.label_a.setText(sims[0][0] + '  相似度：' + str(sims[0][1]))
        self.sim4_win.label_b.setText(sims[1][0] + '  相似度：' + str(sims[1][1]))
        self.sim4_win.label_c.setText(sims[2][0] + '  相似度：' + str(sims[2][1]))
        self.sim4_win.label_d.setText(sims[3][0] + '  相似度：' + str(sims[3][1]))

        # 3 幅不太相似的窗口
        self.unsim3_win.label.setPixmap(QtGui.QPixmap(ims[4]))
        self.unsim3_win.label_2.setPixmap(QtGui.QPixmap(ims[5]))
        self.unsim3_win.label_3.setPixmap(QtGui.QPixmap(ims[6]))
        self.unsim3_win.label_a.setText(sims[4][0] + '  相似度：' + str(sims[4][1]))
        self.unsim3_win.label_b.setText(sims[5][0] + '  相似度：' + str(sims[5][1]))
        self.unsim3_win.label_c.setText(sims[6][0] + '  相似度：' + str(sims[6][1]))

    def clicked_index(self):
        self.ui.index_btn.clicked.connect(self.index)

    def display_pics(self):
        self.unsim_win3.show()
        self.sim_win4.show()

    def click_display(self):
        self.ui.display_btn.clicked.connect(self.display_pics)


if __name__ == '__main__':
    MainWindow()