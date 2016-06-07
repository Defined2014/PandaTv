#!/usr/bin/env python
#coding=utf8

import PandaTv
import httplib2
import urllib.request
import json
import sys
import os
from PyQt5.QtCore import *
from PyQt5 import QtWidgets,QtGui



class Window(QtWidgets.QMainWindow):
    def __init__(self, parent = None):
        QtWidgets.QWidget.__init__(self, parent)

        main_ground = QtWidgets.QWidget()
        self.setCentralWidget(main_ground)
        self.setWindowTitle("PandaTv弹幕助手")
        self.setWindowIcon(QtGui.QIcon(r'icon.jpeg'))

        self.QroomId=QtWidgets.QLineEdit()
        self.QRoomButton=QtWidgets.QPushButton("确认输入",self)
        self.QRoomButton.clicked.connect(self.OnButtonClicked)
        self.Qbarrage=QtWidgets.QTextEdit()
        self.Qbarrage.setReadOnly(True)

        roomid=PandaTv.getfollow()
        l=len(roomid)
        if(l>4):
            l=4
            roomid=roomid[0:4]

        grid = QtWidgets.QGridLayout()
        grid2 = QtWidgets.QGridLayout()
        grid2.setSpacing(20)
        grid.setSpacing(20)
        grid.addWidget(QtWidgets.QLabel("在关注的主播，已开播的有："),1,0,1,3)
        grid.addLayout(grid2,2,0,2,3)
        j=0
        for i in roomid:
            url=i['pic']
            name=i['name']+'.jpg'
            if(os.path.isfile(name)==False):
                conn = urllib.request.urlopen(url)
                f = open(name,'wb')
                f.write(conn.read())  
                f.close()  
            self.testlable = QtWidgets.QLabel()
            self.testlable.setPixmap(QtGui.QPixmap(name))
            grid2.addWidget(self.testlable,l//2+2+j//2*2,j%2)
            grid2.addWidget(QtWidgets.QLabel(i['name']+" <font color=\"red\">房间号</font>： "+i['roomid']),l//2+3+j//2*2,j%2)
            j=j+1
        grid.addWidget(QtWidgets.QLabel("请输入房间号:"),l//2+3,0)
        grid.addWidget(self.QroomId,l//2+3,1)
        grid.addWidget(self.QRoomButton,l//2+3,2)
        grid.addWidget(QtWidgets.QLabel("弹幕:"),l//2+4,0)
        grid.addWidget(self.Qbarrage,l//2+4,1,8,2)

        main_ground.setLayout(grid)
        self.resize(500,300)

    def OnButtonClicked(self):
        self.Qbarrage.clear()
        if self.QroomId.text().strip().isdigit() == True:
            status=PandaTv.getroomstatus(self.QroomId.text().strip(),self.Qbarrage)
            if(int(status)==2):
                if(type(self.thread)==MyThread):
                    self.thread.flag=0
                    self.thread.wait()
                    self.thread.quit()
                self.thread=MyThread()
                self.thread.start()
                self.thread.trigger.connect(self.updateProgress,Qt.QueuedConnection)
            elif(int(status)==3):
                self.Qbarrage.append("主播尚未开播")
        else:
        	self.Qbarrage.setText("请输入数字")

    @pyqtSlot(str) 
    def updateProgress(self, value): 
        self.Qbarrage.append(value) 

class MyThread(QThread):
    trigger = pyqtSignal(str)
    flag=1

    def __init__(self):
        super(MyThread,self).__init__()

    def run(self):
        w.Qbarrage.append("正在连接房间...")
        self.flag=1
        PandaTv.getdm(w.QroomId.text().strip(),self)


app = QtWidgets.QApplication(sys.argv)
w = Window()
w.show()
sys.exit(app.exec_())

