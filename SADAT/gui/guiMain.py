import sys

import vispy.scene
import cv2
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import SystemManager
from externalmodules.default.dataset_enum import senarioBasicDataset
from gui.guiCameraDock import cameraDock
from gui.guiMainBottomToolbar import toolbarPlanviewVisible
from gui.guiMainDocks import SideDock
from gui.planview2D import planView2D
from gui.planview3D import planView3D
from sensor.SenAdptMgr import AttachedSensorName
from gui.comboCheck import CheckableComboBox
from gui.EventHandler import MouseEventHandler
from gui.menuExit import menuExit
from gui.menuFiles import menuLoadSim, menuLoadSim_pcd, menuLogPlay, menuLogPlayROS
from gui.menuSim import menuSim

from multiprocessing import Manager

from gui.toolbarOption import toolbarPlay, toolbarEditor
from gui.toolbarSlider import toolbarSlider
from utils.importer import Importer
from utils.sadatlogger import slog
from views.planview_manager import planviewManager, guiInfo
from dadatype.dtype_cate import DataTypeCategory

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

    def setSlider(self, index):
        self.slider.setValue(index)

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

class MyApp(QMainWindow):

    def __init__(self, parent=None):
        super(MyApp, self).__init__(parent)
        self.statusbar=self.statusBar()
        self.setMouseTracking(True)
        self.setAcceptDrops(True)

        #frame rate
        self.velocity = 15          #초기 라이다 데이터 값(비율)

        #init gui group
        self.guiGroup = {}

        self.gcontrol = GUI_CONTROLLER()
        self.mouseEventHndl = MouseEventHandler()

        # camera Dock init
        self.cameraDock = cameraDock()
        self.bottomToolbar = toolbarPlanviewVisible(self)

        # init Simulator Manager
        self.simulator = SystemManager.SystemManager(Manager(), self)   #simulator변수는 SnSimylator 파일을 import
        self.simulator.setVelocity(self.velocity)
        self.planviewmanager = planviewManager()
        self.planviewmanager.visibleChanged.hfunc = self.bottomToolbar.refreshList

        #init planview widget
        self.stkWidget = QStackedWidget(self)
        self.planviewUI()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Autonomous Driving Analysis Tool')
        #self.setStyleSheet("background-color: dimgray;")
        self.guiGroup[GUI_GROUP.LOGGING_MODE] = []
        self.guiGroup[GUI_GROUP.LOGPLAY_MODE] = []
        self.statusBar()
        self.statusBar().setStyleSheet("background-color : white")
        self.initMenubar()
        self.initToolbar()
        #self.ComboToolbar()
        self.addToolBar(Qt.BottomToolBarArea, self.bottomToolbar)
        # init side Widget
        self.addDockWidget(Qt.LeftDockWidgetArea, self.cameraDock)
        self.addDockWidget(Qt.LeftDockWidgetArea, SideDock(self))
        #set planview in main
        self.setCentralWidget(self.stkWidget)
        #self.setCentralWidget(self.pvWidget)
        self.setStyleSheet("""QMenuBar {        self.draw()

                         background-color: Gray;
                         color: white;
                        }

                     QMenuBar::item {
                         background: Gray;
                         color: white;
                     }""")

        p = self.palette()
        #p.setColor(self.backgroundRole(), Qt.lightGray)
        self.setPalette(p)
        self.modeChanger(GUI_GROUP.ALL, False)
        display_monitor = 0
        monitor = QDesktopWidget().screenGeometry(display_monitor)
        self.setGeometry(0, 0, 1500, 1000)
        self.move(monitor.left()+300, monitor.top()+300)
        self.show()

    def initMenubar(self):
        #create MenuBar
        self.menubar = self.menuBar()
        self.menubar.setNativeMenuBar(False)
        self.statusBar()

        #File Menu
        filemenu = self.menubar.addMenu('&File')
        filemenu.addAction(menuLoadSim('Load log files..', self))
        filemenu.addAction(menuLoadSim_pcd('Load pcd files.', self))

        # Add LogPlay
        logplaymenu = filemenu.addMenu('&Log Play')
        logplaymenu.addAction(menuLogPlay('Log Play with Device',self))
        logplaymenu.addAction(menuLogPlayROS('Log Play with ROS', self))
        filemenu.addAction(menuExit('exit', self))

        #Simulation Menu
        simmenu = self.menubar.addMenu('&Simulation')
        simmenu.addAction(menuSim('Play',self))
        self.guiGroup[GUI_GROUP.LOGPLAY_MODE].append(simmenu)

    def initToolbar(self):
        self.toolbar = self.addToolBar('Navigator')
        toolplay = toolbarPlay('Play', self, self.simulator.playMode, 'Ctrl+P')     #플레이
        toolpause = toolbarPlay('Pause', self, self.simulator.PauseMode)            #중지
        toolresume = toolbarPlay('Resume', self, self.simulator.ResumeMode)         #재생
        self.toolvel = toolbarEditor('10', self, self.simulator.setVelocity)
        self.toolvel.setText(str(self.simulator.getVelocity()))
        self.toolvel.setFixedWidth(50)

        self.toolbar.addAction(toolplay)
        self.toolbar.addAction(toolpause)
        self.toolbar.addAction(toolresume)
        self.toolbar.addWidget(self.toolvel)
        #self.toolbar.setStyleSheet("color: white")

        #step by step
        fbutton=QPushButton('Decrease button')
        fbutton.setFixedWidth(50)
        fbutton.setText("⬅")
        fbutton.clicked.connect(self.DecreaseButton)
        self.toolbar.addWidget(fbutton)

        sbutton=QPushButton('Increase button')
        sbutton.setFixedWidth(50)
        sbutton.setText("➡")
        sbutton.clicked.connect(self.IncreaseButton)
        self.toolbar.addWidget(sbutton)

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


    def planviewUI(self):
        if Importer.checkVispy() is True:
            self.stkWidget.addWidget(planView3D(self.planviewmanager))

        self.stkWidget.addWidget(planView2D(self.planviewmanager))
        self.setPlanviewWidget(0)


    def setPlanviewWidget(self, idx):
        self.stkWidget.setCurrentIndex(idx)
        self.pvWidget = self.stkWidget.currentWidget()


    def keyPressEvent(self, e):
        if e.key()==Qt.Key_Left:
            self.DecreaseButton()
        if e.key()==Qt.Key_Right:
            self.IncreaseButton()

    def DecreaseButton(self):
        self.gcontrol.setSlider(self.gcontrol.getSlider().value() - 1)
        self.simulator.lpthread.setPlayPoint(self.gcontrol.getSlider().value())

    def IncreaseButton(self):
        self.gcontrol.setSlider(self.gcontrol.getSlider().value() + 1)
        self.simulator.lpthread.setPlayPoint(self.gcontrol.getSlider().value())

    def ComboToolbar(self):
        self.toolbar=self.addToolBar('ComboToolbar')
        self.addToolBar(Qt.BottomToolBarArea,self.toolbar)
        self.comboText=QLabel('Object View')

        self.combo = CheckableComboBox()
        self.combo.setFixedHeight(25)

        for name, member in DataTypeCategory.__members__.items():
            self.combo.addItem(name)
            item = self.combo.model().item(name.index(name), 0)
            item.setCheckState(Qt.Checked)

        self.toolbar.addWidget(self.comboText)
        self.toolbar.addWidget(self.combo)


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
        print()
        print("changePosition called.")
        print()
        self.planviewmanager.updateview(data)
        self.updatePosition()

    def updatePosition(self):       #포지션 업데이트 (점 좌표 값)
        self.planviewmanager.updateAllpos()
        #play with opengl
        self.pvWidget.draw()

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

        if pbinfo.mode != self.simulator.lpthread.PLAYMODE_ETC:
            stxt = 'current idx - %d'%pbinfo.currentIdx     #stxt는 tool 하단부에 나타나는 현재 index
            self.statusBar().showMessage(stxt)
        self.update()


    def updateCameraImage(self, data):
        for rkey, rval in data.items():
            cv_image = rval.imagedata
            h, w, ch = cv_image.shape
            bytesPerLine = ch * w
            convertToQtFormat = QImage(cv_image.data, w, h, cv_image.strides[0], QImage.Format_RGB888)
            #p = convertToQtFormat.scaledToWidth(self.vwidth)
            #self.label.setPixmap(QPixmap.fromImage(p))
            self.cameraDock.setPixmap(convertToQtFormat)

    def closeEvent(self, event):
        self.simulator.cleanProcess()
        sys.exit()

if __name__ == '__main__':
    slog.init()
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())