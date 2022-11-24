from PyQt5.QtWidgets import QAction, QDialog, QPlainTextEdit, QGridLayout, QLabel, QPushButton, QFileDialog, QComboBox, \
    QSlider, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, Qt, QThread, QTimer

import time
import rosbag
import pyqtgraph
import ros_numpy
import numpy as np
import sensor_msgs
import csv
import json

from sklearn.neighbors import KDTree
from sklearn.cluster import DBSCAN

from msgs.Inputpointcloud import Inputpoints
from msgs.Algorithmoutput import Algorithmoutput

from threading import Thread

class reSimulation(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.simulator = self.parent.simulator
        # Bounding box list via algorithm result
        self.detectionBbox = None

        self.filename = None

        self.setWindowTitle('ReSimulation')
        self.setGeometry(600, 600, 600, 800)
        self.show()
        self.initUI()

        # ros thread for play loaded rosbag data
        self.bagthread = Thread(target=self.getbagfile)

        # List for create Resimulation replay output file
        self.algorithmOutput = list()

        # List for Replay via replay output file
        self.outputdata = None

        # Flag for initial load output file check
        self.isloadoutput = False

        # playback control flags

        self.ispaused = True


        self.logplayindex = 0

    def initUI(self):

        self.gridlayout = QGridLayout()
        self.setLayout(self.gridlayout)
        # rosbag file open UI
        self.fileloadlayout = QHBoxLayout()

        self.openbagfile = QPushButton('Load rosbag File', self)
        self.openbagfile.setFixedWidth(170)
        self.openbagfile.clicked.connect(self.loadbagfile)

        self.selectedfile = QLabel()

        self.fileloadlayout.addWidget(self.openbagfile)
        self.fileloadlayout.addWidget(self.selectedfile)
        self.gridlayout.addLayout(self.fileloadlayout, 0, 0)

        # Algorithm Category UI

        self.algocate = QComboBox(self)
        self.algocatelayout = QHBoxLayout()

        self.algocate.addItem("Algo Category 1")
        self.algocate.addItem("Algo Category 2")
        self.algocate.addItem("Algo Category 3")
        self.algocate.addItem("Algo Category 4")

        self.algocate.setFixedWidth(170)
        self.algocatelayout.addWidget(self.algocate)
        self.algocatelayout.addWidget(QLabel('Algorithm Category : '))

        self.gridlayout.addLayout(self.algocatelayout, 3, 0)

        # Implemented Algorithm UI

        self.algolist = QComboBox(self)
        self.algolistlayout = QHBoxLayout()

        self.algolist.addItem("Algo 1")
        self.algolist.addItem("Algo 2")
        self.algolist.addItem("Algo 3")
        self.algolist.addItem("Algo 4")

        self.algolist.setFixedWidth(170)
        self.algolistlayout.addWidget(self.algolist)
        self.algolistlayout.addWidget(QLabel('Test Algorithm : '))
        self.gridlayout.addLayout(self.algolistlayout, 5, 0)

        # Resimulation execute

        self.resimulate = QPushButton('Algorithm Test', self)
        self.resimulate.clicked.connect(self.resimulation)
        self.gridlayout.addWidget(self.resimulate, 6, 0)

        # Load replay output file

        self.loadreplay = QPushButton('Load output file', self)
        self.loadreplay.clicked.connect(self.loadreplayoutput)
        self.gridlayout.addWidget(self.loadreplay, 7, 0)

        # Resim Visualization UI

        # Playback control UI
        self.replaybtn = QPushButton('Replay / Pause', self)
        self.stepoverbtn = QPushButton('Step over', self)
        self.stepdownbtn = QPushButton('Step down', self)

        self.playbacklayout = QHBoxLayout()
        self.playbacklayout.addWidget(self.replaybtn)
        self.playbacklayout.addWidget(self.stepoverbtn)
        self.playbacklayout.addWidget(self.stepdownbtn)

        self.replaybtn.clicked.connect(self.replay)
        # self.gridlayout.addWidget(self.replaybtn, 8, 0)
        self.gridlayout.addLayout(self.playbacklayout, 8, 0)

        # Slider UI
        self.slidebar = QSlider(Qt.Horizontal, self)

        self.slidebar.setMinimum(0)

        self.slidebar.valueChanged.connect(self.slidercallback)
        self.gridlayout.addWidget(self.slidebar, 9, 0)

        # point cloud 출력용
        self.canvas = pyqtgraph.GraphicsLayoutWidget()
        self.gridlayout.addWidget(self.canvas, 10, 0)
        self.view = self.canvas.addViewBox()
        self.view.setAspectLocked(True)
        self.view.disableAutoRange()
        self.view.scaleBy(s=(20, 20))
        grid = pyqtgraph.GridItem()
        self.view.addItem(grid)

        self.spt = pyqtgraph.ScatterPlotItem(pen=pyqtgraph.mkPen(width=1, color='r'), symbol='o', size=2)
        self.view.addItem(self.spt)

        # global position to display graph
        self.pos = None

        # object 출력용
        self.objs = list()  # for display to graph

        # object 출력용 position과 size
        self.objsPos = list()
        self.objsSize = list()

        # 출력용 Object 사전 생성
        # 스레드 풀과 비슷한 역할을 수행하기 위한?
        numofobjs = 500
        for i in range(numofobjs):
            obj = pyqtgraph.QtGui.QGraphicsRectItem(-0.5, -0.5, 0.5, 0.5)  # obj 크기는 1m로 고정시킴
            obj.setPen(pyqtgraph.mkPen('w'))
            self.view.addItem(obj)
            self.objs.append(obj)

            pos = [0, 0, 0]  # x, y, z
            size = [0, 0, 0]  # w, h, depth
            self.objsPos.append(pos)
            self.objsSize.append(size)

    @pyqtSlot()
    def get_data(self):
        if self.pos is not None:
            self.spt.setData(pos=self.pos)  # line chart 그리기

        # object 출력
        # 50개 object중 position 값이 0,0이 아닌것만 출력
        for i, obj in enumerate(self.objs):
            objpos = self.objsPos[i]
            objsize = self.objsSize[i]
            if objpos[0] == 0 and objpos[1] == 0:
                obj.setVisible(False)
            else:
                obj.setVisible(True)
                obj.setRect((objpos[0]) - (objsize[0] / 2), (objpos[1]) - (objsize[1] / 2), objsize[0], objsize[1])

    def customAlgorithm(self, output_idx, data, points):
        """
        알고리즘 적용을 위한 추상 클래스 구현 후 해당 클래스를 통한 Interface만 정의하면 될 것 같습니다.
        입력, 출력 데이터를 위한 클래스 정의 필요

        알고리즘 적용을 위한 인터페이스 역할을 수행할 수 있어야 함.
        Detection
        input
            - points
        return
            - Object(s)
                - x
                - y
                - x_size
                - y_size
        """

        idx = np.random.randint(len(points), size=2500)
        points = points[idx, :]

        print("points 타입")
        print(type(points))

        box_cnt = list()

        # 선택한 알고리즘에 따라 points를 전달하고
        # self.clusterLabel 에 결과 데이터 저장
        """
        알고리즘 별 다른 함수 호출 필요
        """
        self.tempdbscan(points)

        print("self.clusterLabel")
        print(type(self.clusterLabel))
        print(self.clusterLabel)

        # 그래프의 좌표 출력을 위해 pos 데이터에 최종 points 저장
        self.pos = points

        # self.algorithmOutput[str(output_idx)]['data'] = dict(enumerate(points.flatten(), 1))

        # 만약 self.tempdbscan(points) 결과가 없으면, 아래에서 append 하지 않도록 코드 작성
        self.algorithmOutput.append({
            'time': {
                'secs': data.timestamp.secs,
                'nsecs': data.timestamp.nsecs
            },
            'det': {},
            'data': {}
        })

        self.algorithmOutput[output_idx]['data'] = {
            'min': np.min(points),
            'max': np.max(points),
            'size': np.size(points),
            'points': points.tolist()
        }

        # Bounding Box
        for i in range(1, max(self.clusterLabel) + 1):
            tempobjPos = self.objsPos[i]
            tempobjSize = self.objsSize[i]

            index = np.asarray(np.where(self.clusterLabel == i))
            # print(i, 'cluster 개수 : ', len(index[0]))
            x = np.min(points[index, 0])
            y = np.min(points[index, 1])
            x_size = np.max(points[index, 0]) - np.min(points[index, 0])  # x_max 3
            y_size = np.max(points[index, 1]) - np.min(points[index, 1])  # y_max 1.3

            # car size bounding box
            box_cnt.append(i)
            tempobjPos[0] = x
            tempobjPos[1] = y
            tempobjSize[0] = x_size
            tempobjSize[1] = y_size

            self.algorithmOutput[output_idx]['det'][str(i)] = {
                'x': x,
                'y': y,
                'x_size': x_size,
                'y_size': y_size
            }

    def tempdbscan(self, points):
        dbscan = DBSCAN(eps=5, min_samples=10, algorithm='ball_tree').fit(points)
        self.clusterLabel = dbscan.labels_

    def resetObjPos(self):
        for i, pos in enumerate(self.objsPos):
            # reset pos, size
            pos[0] = 0
            pos[1] = 0
            os = self.objsSize[i]
            os[0] = 0
            os[1] = 0

    def loadbagfile(self):
        # print("loadbagfile")
        self.filename = QFileDialog.getOpenFileName(self, 'Open rosbag file', '/home/ros/rosbag')[0]
        print("Selected filename is : ", self.filename)
        self.selectedfile.setText(self.filename)

    def resimulation(self):
        if self.filename == None:
            print("No any file selected!")
            pass
        elif self.ispaused == False:
            self.bagthreadFlag = False
            # self.bagthread
        elif self.ispaused == True:
            print("resimulation")
            # load bagfile
            self.bag_file = rosbag.Bag(self.filename)

            # ros thread
            self.bagthreadFlag = True

            self.bagthread.start()
            self.ispaused = False

            # Graph Timer 시작
            self.mytimer = QTimer()
            self.mytimer.start(10)  # 차트 갱신 주기
            self.mytimer.timeout.connect(self.get_data)

            # ros 파일에서 velodyne_points 메시지만 불러오는 부분

    def getbagfile(self):
        read_topic = '/velodyne_points'  # 메시지 타입

        for idx, data in enumerate(self.bag_file.read_messages(read_topic)): # topic, msg, t
            if self.bagthreadFlag is False:
                break
            # ros_numpy 데이터 타입 문제로 class를 강제로 변경
            data.message.__class__ = sensor_msgs.msg._PointCloud2.PointCloud2

            # get point cloud
            pc = ros_numpy.numpify(data.message)
            points = np.zeros((pc.shape[0], 4))  # point배열 초기화 1번 컬럼부터 x, y, z, intensity 저장 예정

            # for ROS and vehicle, x axis is long direction, y axis is lat direction
            # ros 데이터는 x축이 정북 방향, y축이 서쪽 방향임, 좌표계 오른손 법칙을 따름
            points[:, 0] = pc['x']
            points[:, 1] = pc['y']
            points[:, 2] = pc['z']
            points[:, 3] = pc['intensity']

            # self.algorithmOutput.append({
            #     'time': {
            #         'secs': data.timestamp.secs,
            #         'nsecs': data.timestamp.nsecs
            #     },
            #     'det': {},
            #     'data': {}
            # })

            self.resetObjPos()
            self.customAlgorithm(idx, data, points)

            time.sleep(0.1) # 재생 주기 설정

        print("Algorithm test end.")

        jsonoutput = json.dumps(self.algorithmOutput, sort_keys=True, indent=4)

        with open("output_2.json", "w") as outfile:
            outfile.write(jsonoutput)

        print("output file generated.")

    def loadreplayoutput(self):
        # Load json output file
        selectedoutput = QFileDialog.getOpenFileName(self, 'Open replay output file')[0]

        with open(selectedoutput, "r") as f:
            json_object = json.load(f)

        self.outputdata = json_object
        self.slidebar.setMaximum(len(self.outputdata))

        # QSlider의 최대값을

    def slidercallback(self):
        print("Slidebar current val")
        print(self.slidebar.value())
        self.logplayindex = self.slidebar.value()

    def replay(self):
        # TODO: Replay data through Thread and update planview

        self.logthread = Thread(target=self.getoutputdata)
        self.logthread.daemon = True
        self.logthread.start()

        self.mytimer = QTimer()
        self.mytimer.start(10)  # 차트 갱신 주기
        self.mytimer.timeout.connect(self.get_data)

    def getoutputdata(self):
        # print("Replay called.")

        box_cnt = list()

        if self.isloadoutput == False:
            self.slidebar.setValue(0)
            self.isloadoutput = True

        print("Total Len")
        print(len(self.outputdata))
        for idx, val in enumerate(self.outputdata):
            print("idx", idx)
            # idx = self.logplayindex
            # self.logplayindex = idx

            self.slidebar.setValue(idx)

            self.resetObjPos()

            self.pos = val['data']['points']

            for det_idx, (key, value) in enumerate(val['det'].items()):
                # 두번째 for에 맞춰서 idx 추가 필요
                tempobjPos = self.objsPos[det_idx + 1]
                tempobjSize = self.objsSize[det_idx + 1]

                x = value['x']
                y = value['y']
                x_size = value['x_size']
                y_size = value['y_size']

                # car size bounding box
                box_cnt.append(idx + 1)
                tempobjPos[0] = x
                tempobjPos[1] = y
                tempobjSize[0] = x_size
                tempobjSize[1] = y_size

            time.sleep(0.1)