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

class MyAppEventManager():          #아직 해당 클래의 기능은 없는거 같음
    def __init__(self):
        pass

'''MyWG클래스는 레이아웃을 나누기 위해 생성한 클래스'''
class MyWG(QWidget):

    def __init__(self, parent):
        super(MyWG, self).__init__(parent)      #MyApp클래스를 상속 하면서 MyApp클래스의 함수에 접근 가능하게 됨
        self.pr = parent
        self.initUI()

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
        self.setFixedSize(300, 730)         #이 부분의 y의 값은 맥에서 개발 할 때는 730으로 리눅스 환경에서 개발할 때는 930으로 설정

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
        self.setMouseTracking(True)
        self.setAcceptDrops(True)
        print(self.hasMouseTracking())

        #for Planview Size and Position
        self.panviewSize = 20       #화면에 출력되는 라이다 데이터
        self.relx = 0               #라이다 데이터의 x축 좌표를 조정
        self.rely = 0               #라이다 데이터의 y축 좌표를 조정
        self.pressX=0
        self.pressY=0
        self.xp=0
        self.yp=0

        #frame rate
        self.velocity = 15          #초기 라이다 데이터 값(비율)

        #init gui group
        self.guiGroup = {}

        self.gcontrol = GUI_CONTROLLER()
        self.mouseEventHndl = MouseEventHandler()

        self.prevx = list()
        self.prevy = list()

        # init Simulator Manager
        self.simulator = SnSimulator.SnSimulator(Manager(), self)   #simulator변수는 SnSimylator 파일을 import
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
        #create MenuBar
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        self.statusBar()

        #File Menu
        filemenu = menubar.addMenu('&File')
        #filemenu.addAction(self.OnOpenDocument('Load log files..', self))
        filemenu.addAction(menuLoadSim('Load log files..', self))
        #self.Open_Button.clicked.connect(self.OnOpenDocument3)
        filemenu.addAction(menuLogPlay('Log Play',self))
        filemenu.addAction(menuExit('exit', self))

        #Simulation Menu
        simmenu = menubar.addMenu('&Simulation')
        simmenu.addAction(menuSim('Play',self))
        self.guiGroup[GUI_GROUP.LOGPLAY_MODE].append(simmenu)

    def initToolbar(self):
        self.toolbar = self.addToolBar('Navigator')
        toolplay = toolbarPlay('Play', self, self.simulator.playMode, 'Ctrl+P')     #플레이
        toolpause = toolbarPlay('Pause', self, self.simulator.PauseMode)            #중지
        toolresume = toolbarPlay('Resume', self, self.simulator.ResumeMode)         #재생
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


    def initplanview(self):         #현재 이 함수의 기능은 못 찾겠음,, tool을 보아하니 아직 레이아웃 버튼이 안보임
        grid_layout = QGridLayout()
        self.setLayout(grid_layout)

        for x in range(3):
            for y in range(3):
                button = QPushButton(str(str(3 * x + y)))
                grid_layout.addWidget(button, x, y)

    def paintEvent(self, e):        #라이다 데이터를 출력해주는 함수
        qp = QPainter()
        qp.begin(self)
        self.draw_point(qp)
        qp.end()

    #event
    def wheelEvent(self, e):            #whellEvent 함수, 마우스 휠을 조정해 panview 사이즈 조정 가능
        wvalue = e.angleDelta().y()     #wvalue는 delta의 값을 이용해서 마우스 휠의 y축 즉, 위 아래 값을 알 수 있음
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
        if e.buttons()==Qt.LeftButton:
            self.relx = e.globalX() - self.pressX
            self.rely = e.globalY() - self.pressY
            self.updatePosition()

    def mousePressEvent(self, e):
        self.updatePosition()
        self.pressX = e.globalX()-self.relx
        self.pressY = e.globalY()-self.rely
        self.updatePosition()
        #print('press')

    def mouseReleaseEvent(self, e):
        self.relx = e.globalX()-self.pressX
        self.rely = e.globalY()-self.pressY
        self.updatePosition()
        #print('release')

    def draw_point(self, qp):
        #draw paint
        self.xp= self.relx
        self.yp=self.rely
        qp.setPen(QPen(Qt.white, 1))
        rx = 150
        ry = 100

        for ikey, values in self.planviewmanager.getObjects():
            for idata in values:
                for tdata in idata.pos_xy:
                    xp = int(tdata[0]) + rx
                    yp = int(tdata[1]) + ry
                    if ikey is senarioBasicDataset.TRACK:
                        qp.drawText(xp, yp, "Test label")
                        qp.drawRect(xp, yp, 20, 20)
                    else:
                        qp.drawEllipse(xp, yp, 6, 6)

    def modeChanger(self, mode, isTrue):
        for modedata in self.guiGroup:
            if mode is GUI_GROUP.ALL or modedata is mode:
                for actions in self.guiGroup[modedata]:
                    actions.setEnabled(isTrue)

    def setStatus(self, str):               #setStatus함수는 tool창에 제일 하단에 있는 상태바 메세지를 출력함
        self.statusBar().showMessage(str)

    #Callback Event

    def sliderMoved(self):                  #sliderMoved 함수는 tool의 슬라이드 바를 움직임
        self.simulator.lpthread.setPlayPoint(self.gcontrol.getSlider().value())
        self.simulator.PauseMode()

    def changePosition(self, data):
        self.planviewmanager.updateposinfo(guiinfo=guiInfo(self.panviewSize, self.width(), self.height(), self.relx, self.rely))
        self.planviewmanager.updateview(data)
        self.updatePosition()

    def updatePosition(self):       #포지션 업데이트 (점 좌표 값)
        self.planviewmanager.updateAllpos(guiinfo=guiInfo(self.panviewSize, self.width(), self.height(), self.relx, self.rely))
        self.update()

    def playbackstatus(self, pbinfo):       #플레이 상태를 다시 되돌리는 함수?, 여기서 pbinfo에 대해서 잘 모르겠음..
        if pbinfo.mode == self.simulator.lpthread.PLAYMODE_LOAD:        #lpthread가 Qt 라이브러리를 성공적으로 호출하기 위해서 필요한 스레드옵션
            self.gcontrol.getSlider().setSliderRange(pbinfo.maxLength)
            self.velocity = pbinfo.setfps
            self.simulator.setVelocity(self.velocity)
            self.toolvel.setText(str(self.simulator.getVelocity()))
            self.modeChanger(GUI_GROUP.LOGPLAY_MODE, True)

        elif pbinfo.mode == self.simulator.lpthread.PLAYMODE_PLAY:
            self.gcontrol.getSlider().setValue(pbinfo.currentIdx)
        elif pbinfo.mode == self.simulator.lpthread.PLAYMODE_SETVALUE:
            pass
        stxt = 'current idx - %d'%pbinfo.currentIdx     #stxt는 tool 하단부에 나타나는 현재 index
        self.statusBar().showMessage(stxt)
        self.update()
        #print("pbInfo : ", pbinfo.mode, pbinfo.maxLength, pbinfo.currentIdx)

    def closeEvent(self, event):
        sys.exit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())