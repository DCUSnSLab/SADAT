import sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import SnSimulator
from dadatype.dtype_cate import DataTypeCategory
from externalmodules.default.dataset_enum import senarioBasicDataset
from gui.EventHandler import MouseEventHandler
from gui.menuExit import menuExit
from gui.menuFiles import menuLoadSim, menuLogPlay
from gui.menuSim import menuSim

from multiprocessing import Manager

from gui.toolbarOption import toolbarPlay, toolbarEditor
from gui.toolbarSlider import toolbarSlider
from views.planview_manager import planviewManager, guiInfo

'''GUI 그룹'''
class GUI_GROUP:
    ALL = 0
    LOGGING_MODE = 1
    LOGPLAY_MODE = 2

'''GUI 컨트롤을 위한 클래스'''
class GUI_CONTROLLER:
    STOPMODE = 0
    PLAYMODE = 1
    RESUMEMODE = 2

    def __init__(self):
        self.toolbar = {}
        self.menubar = {}
        self.slider = None
        self.cmode = self.STOPMODE

    def addToolbar(self, item, name):
        self.toolbar[name] = item

    def addMenubar(self, item, name):
        self.menubar[name] = item

    def addSlider(self, item):
        self.slider = item

    def getSlider(self):
        return self.slider

    def getCurrentMode(self):
        return self.cmode

    #라이다 데이터를 플레이, 재생, 멈춤 버튼을 동작 시키는 함수
    def setPlayMode(self, mode):
        self.cmode = mode
        if mode is self.STOPMODE:
            self.toolbar['Play'].setVisible(True)
            self.toolbar['Pause'].setVisible(False)
            self.toolbar['Resume'].setVisible(False)
        elif mode is self.PLAYMODE:
            self.toolbar['Play'].setVisible(False)
            self.toolbar['Pause'].setVisible(True)
            self.toolbar['Resume'].setVisible(False)
        else:
            self.toolbar['Play'].setVisible(False)
            self.toolbar['Pause'].setVisible(False)
            self.toolbar['Resume'].setVisible(True)

class MyAppEventManager():
    def __init__(self):
        pass

'''현재 진행중인 드래그 앤 드롭 이벤트'''
# class DragAndDrop(QPushButton):
#     def __init__(self,parent):
#         QPushButton.__init__(self, parent)
#         self.offset = 0
#
#     def mouseMoveEvent(self, e):
#         if e.pr.paintEvent(self) != Qt.RightButton:
#             return
#
#         #마우스 데이터 전송을 위해 MIME 객체를 선언
#         #데이터 타입, 보낼 데이터를 byte형으로 저장한다.
#         mime_data = QMimeData()
#         mime_data.setData("application/hotspot", b"%d %d" % (e.x(), e.y()))
#
#         drag = QDrag(self)
#         # MIME 타입데이터를 Drag에 설정
#         drag.setMimeData(mime_data)
#         # 드래그시 위젯의 모양 유지를 위해 QPixmap에 모양을 렌더링
#         pixmap = QPixmap(self.size())
#         self.render(pixmap)
#         drag.setPixmap(pixmap)
#
#         drag.setHotSpot(e.pos() - self.rect().topLeft())
#         drag.exec_(Qt.MoveAction)

'''MyWG클래스는 레이아웃을 나누기 위해 생성한 클래스'''
class MyWG(QWidget):

    def __init__(self, parent):
        super(MyWG, self).__init__(parent)      #MyApp클래스를 상속 하면서 MyApp클래스의 함수에 접근 가능하게 됨
        self.pr = parent
        #self.btn=DragAndDrop(self.pr.initplanview())
        self.initUI()
        #self.btn.show()

    '''현재 진행중인 작업'''
    # def dragEnterEvent(self, e:QDragEnterEvent):
    #     e.accept()
    #
    # def dropEvent(self, e:QDropEvent):
    #     position = e.pos()
    #
    #     # 보내온 데이터를 받기
    #     # 그랩 당시의 마우스 위치값을 함께 계산하여 위젯 위치 보정
    #     offset = e.mimeData().data("application/hotspot")
    #     x, y = offset.data().decode('utf-8').split()
    #     self.btn.move(position - QPoint(int(x), int(y)))
    #
    #     e.setDropAction(Qt.MoveAction)
    #     e.accept()

    '''initUI 함수에는 왼쪽 레이아웃의 코드가 작성되어 있음'''
    def initUI(self):
        self.group=QGroupBox("Evaluation")          #레이아웃의 그룹 이름
        self.group.setStyleSheet("color:black;"
                                 "background-color:white;")
        fInnerLayOut=QVBoxLayout()
        self.buttonGroup=QGroupBox("Vehicle Button")
        self.buttonGroup.setStyleSheet("color:black;"
                                       "background-color: white;")
        #레이아웃에 있는 제어 버튼
        self.pushButton1 = QPushButton("전진")
        self.pushButton2 = QPushButton("후진")
        self.pushButton3 = QPushButton("좌회전")
        self.pushButton4 = QPushButton("우회전")
        self.pushButton5 = QPushButton("멈춤")

        eInnerLayOut=QVBoxLayout()
        eInnerLayOut.addWidget(self.pushButton1)
        eInnerLayOut.addWidget(self.pushButton2)
        eInnerLayOut.addWidget(self.pushButton3)
        eInnerLayOut.addWidget(self.pushButton4)
        eInnerLayOut.addWidget(self.pushButton5)
        self.buttonGroup.setLayout(eInnerLayOut)
        self.ExGroup=QGroupBox("None")
        self.ExGroup.setStyleSheet("color:black;"
                                   "background-color: white")
        fInnerLayOut.addWidget(self.buttonGroup)
        fInnerLayOut.addWidget(self.ExGroup,1)
        self.group.setLayout(fInnerLayOut)
        layout=QVBoxLayout()
        layout.addWidget(self.group)
        self.setLayout(layout)
        self.setFixedSize(300, 730)         #이 부분의 y의 값은 맥에서 개발 할 때는 730으로 리눅스 환경에서 개발할 때는 930으로 설정, 창 기본 크기 문제

        self.pr.guiGroup[GUI_GROUP.LOGGING_MODE] = []
        self.pr.guiGroup[GUI_GROUP.LOGPLAY_MODE] = []


        self.pr.statusBar()
        self.pr.statusBar().setStyleSheet("background-color : white")
        self.pr.initMenubar()
        self.pr.initToolbar()
        self.pr.initplanview()
        self.pr.setStyleSheet("""QMenuBar {
                 background-color: Gray;
                 color: white;
                }

             QMenuBar::item {
                 background: Gray;
                 color: white;
             }""")

        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        self.pr.setPalette(p)
        #self.setPalette(p)
        self.pr.modeChanger(GUI_GROUP.ALL, False)

        self.setWindowTitle('QGridLayout')
        self.setGeometry(300, 300, 300, 200)
        self.show()

class MyApp(QMainWindow):

    def __init__(self, parent=None):
        super(MyApp, self).__init__(parent)
        self.statusbar=self.statusBar()
        print(self.hasMouseTracking())
        self.setMouseTracking(True)
        print(self.hasMouseTracking())
        #for Planview Size and Position
        self.panviewSize = 20       #화면에 출력되는 라이다 데이터
        self.relx = 0               #라이다 데이터의 x축 좌표를 조정
        self.rely = 0               #라이다 데이터의 y축 좌표를 조정

        self.pressX=0
        self.pressY=0

        #frame rate
        self.velocity = 15          #초기 라이다 데이터 값(비율)

        #init gui group
        self.guiGroup = {}

        self.gcontrol = GUI_CONTROLLER()
        self.mouseEventHndl = MouseEventHandler()

        self.xpos = []
        self.ypos = []

        self.prevx = list()
        self.prevy = list()

        # init Simulator Manager
        self.simulator = SnSimulator.SnSimulator(Manager(), self)
        self.simulator.setVelocity(self.velocity)

        #planview manager
        self.planviewmanager = planviewManager()

        self.form_widget = MyWG(self)
        self.setCentralWidget(self.form_widget)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('SADAT')
        #self.setStyleSheet("background-color: dimgray;")
        self.setGeometry(300, 300, 1500, 1000)
        self.show()

    def initMenubar(self):
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        self.statusBar()

        #File Menu
        filemenu = menubar.addMenu('&File')
        filemenu.addAction(menuLoadSim('Load log files..', self))
        filemenu.addAction(menuLogPlay('Log Play',self))
        filemenu.addAction(menuExit('exit', self))

        #Simulation Menu
        simmenu = menubar.addMenu('&Simulation')
        simmenu.addAction(menuSim('Play',self))
        self.guiGroup[GUI_GROUP.LOGPLAY_MODE].append(simmenu)

    def initToolbar(self):
        self.toolbar = self.addToolBar('Navigator')
        toolplay = toolbarPlay('Play', self, self.simulator.playMode, 'Ctrl+P')
        toolpause = toolbarPlay('Pause', self, self.simulator.PauseMode)
        toolresume = toolbarPlay('Resume', self, self.simulator.ResumeMode)
        self.toolvel = toolbarEditor('10', self, self.simulator.setVelocity)
        self.toolvel.setText(str(self.simulator.getVelocity()))

        self.toolbar.addAction(toolplay)
        self.toolbar.addAction(toolpause)
        self.toolbar.addAction(toolresume)
        self.toolbar.addWidget(self.toolvel)
        self.toolbar.setStyleSheet("color: black")

        #slider
        slider = toolbarSlider(Qt.Horizontal, self)
        slider.sliderMoved.connect(self.sliderMoved)
        slider.sliderReleased.connect(self.sliderMoved)
        self.toolbar.addWidget(slider)

        self.gcontrol.addToolbar(toolplay, toolplay.text())
        self.gcontrol.addToolbar(toolpause, toolpause.text())
        self.gcontrol.addToolbar(toolresume, toolresume.text())
        self.gcontrol.addToolbar(slider, 'logslider')
        self.gcontrol.addSlider(slider)
        self.gcontrol.setPlayMode(GUI_CONTROLLER.STOPMODE)

        self.guiGroup[GUI_GROUP.LOGPLAY_MODE].append(self.toolbar)


    def initplanview(self):
        grid_layout = QGridLayout()
        self.setLayout(grid_layout)

        for x in range(3):
            for y in range(3):
                button = QPushButton(str(str(3 * x + y)))
                grid_layout.addWidget(button, x, y)

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.draw_point(qp)
        qp.end()

    #event
    def wheelEvent(self, e):
        wvalue = e.angleDelta().y()
        div = 0.025
        max = 0.6
        min = 0.05
        dv = wvalue * div
        if dv != 0:
            sign = abs(dv) / dv
        else:
            sign = 0

        if abs(dv) > max:
            dv = max * sign
        elif abs(dv) < min:
            dv = min * sign

        temp = self.panviewSize + dv

        if 0.1 < temp <= 126:
            self.panviewSize += dv

        if self.gcontrol.getCurrentMode() is not GUI_CONTROLLER.PLAYMODE:
            self.updatePosition()

    def mouseMoveEvent(self, e):
        pass
        # mevent = self.mouseEventHndl.moveEvent
        #
        # if e.buttons() == Qt.LeftButton:
        #     if mevent.eventMouse(e.globalX(), e.globalY()):

    '''내가 수정 진행부분'''
    def mouseMoveEvent(self, e):
        txt="Mouse 위치 x = {0}, y = {1}".format(e.x(),e.y())
        self.statusbar.showMessage(txt)
        #print(e.globalX(), e.globalY())
        # if e.buttons()==Qt.LeftButton:
        #     return
        # mime_data=QMimeData()
        # drag=QDrag(self)
        # drag.setMimeData(mime_data)

    def mousePressEvent(self, e):
        self.pressX=e.globalX()
        self.pressY=e.globalY()

    def mouseReleaseEvent(self, e):
        self.relx = e.globalX()-self.pressX
        self.rely=e.globalY()-self.pressY

    def dragEnterEvent(self,e:QDragEnterEvent):
        e.accept

    def dropEvent(self,e:QDropEvent):


        e.setDropAction()
        e.accept()

    def draw_point(self, qp):
        #draw paint
        qp.setPen(QPen(Qt.white, 1))

        rx = 150
        ry = 100
        for idx,item in enumerate(self.xpos):
            #qp.drawPoint(int(self.xpos[idx]), int(self.ypos[idx]))
            xp = int(self.xpos[idx])+rx    #
            yp = int(self.ypos[idx])+ry
            qp.drawEllipse(xp, yp, 1, 1)

        for ikey, values in self.planviewmanager.getObjects():
            for idata in values:
                xp = int(idata.posx) + rx
                yp = int(idata.posy) + ry
                if ikey is senarioBasicDataset.TRACK:
                    qp.drawRect(xp,yp,10,10)
                else:
                    qp.drawEllipse(xp, yp, 6, 6)

    def modeChanger(self, mode, isTrue):
        for modedata in self.guiGroup:
            if mode is GUI_GROUP.ALL or modedata is mode:
                for actions in self.guiGroup[modedata]:
                    actions.setEnabled(isTrue)

    def setStatus(self, str):
        self.statusBar().showMessage(str)

    #Callback Event

    def sliderMoved(self):
        self.simulator.lpthread.setPlayPoint(self.gcontrol.getSlider().value())
        self.simulator.PauseMode()

    def changePosition(self, data):
        self.planviewmanager.updateposinfo(guiinfo=guiInfo(self.panviewSize, self.width(), self.height(), self.relx, self.rely))
        self.planviewmanager.updateview(data)
        self.prevx = data['rawdata'][0]
        self.prevy = data['rawdata'][1]

        # key = list(data.keys())
        # if(len(data[key[1]]) > 0):
        #     print('raw: ',data['rawdata'][0][0],end=" ")
        #     key3 = data[key[1]]
        #     print('dataset: ',type(key3[0]), key3[0].posx)
        self.updatePosition()

    def updatePosition(self):       #포지션 업데이트 (점 좌표 값)
        # print(len(x))
        self.xpos.clear()
        self.ypos.clear()
        self.planviewmanager.updateAllpos(guiinfo=guiInfo(self.panviewSize, self.width(), self.height(), self.relx, self.rely))

        for idx, item in enumerate(self.prevx):
            self.xpos.append((self.prevx[idx] / self.panviewSize) + (self.width() / 2) + self.relx)
            self.ypos.append((self.prevy[idx] / self.panviewSize) + (self.height() / 2) + self.rely)

        self.update()

    def playbackstatus(self, pbinfo):
        if pbinfo.mode == self.simulator.lpthread.PLAYMODE_LOAD:
            self.gcontrol.getSlider().setSliderRange(pbinfo.maxLength)
            self.velocity = pbinfo.setfps
            self.simulator.setVelocity(self.velocity)
            self.toolvel.setText(str(self.simulator.getVelocity()))

            self.modeChanger(GUI_GROUP.LOGPLAY_MODE, True)
        elif pbinfo.mode == self.simulator.lpthread.PLAYMODE_PLAY:
            self.gcontrol.getSlider().setValue(pbinfo.currentIdx)
        elif pbinfo.mode == self.simulator.lpthread.PLAYMODE_SETVALUE:
            pass
        stxt = 'current idx - %d'%pbinfo.currentIdx
        self.statusBar().showMessage(stxt)
        self.update()
        #print("pbInfo : ", pbinfo.mode, pbinfo.maxLength, pbinfo.currentIdx)

    def closeEvent(self, event):
        sys.exit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())