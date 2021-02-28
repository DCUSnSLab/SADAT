'''
외부 모듈은 총 2가지 방법으로 제어될 수 있음
1. taskPostPlan 에서 realtime으로 외부 모듈 동작
2. LogSimDispatcher에서 시뮬레이션 데이터를 load할 때 외부 모듈 동작

외부모듈의 목적
1. 현재 진행되고 있는 센서데이터를 활용하여 각각의 알고리즘들을 수행
2. 알고리즘들의 상태 분석 및 기능 기선
3. 시나리오 설정 및 시나리오 별 모듈을 동작시켜 상태 분석 및 각 기능 개선
4.
'''
from externalmodules.default.senario import senarioBasic
from externalmodules.ext_scheduler import extScheduler
from externalmodules.default.dataset_enum import senarioBasicDataset


class extModuleManager():
    def __init__(self):
        self.__selectedScheduler = None
        self.modAdapter = None
        #temperary
        self.setSenario(senario=senarioBasic())

    def doTask(self, rawdata):
        self.__selectedScheduler.resetData()
        self.__selectedScheduler.insertRawData(rawdata)
        self.__selectedScheduler.doTask()

    def setSenario(self, senario:extScheduler):
        self.__selectedScheduler = senario
        self.__selectedScheduler.initextScheduler()
        self.__selectedScheduler.enableModule(0)

    def Disable(self):
        a=senarioBasicDataset.TRACK
        b=senarioBasicDataset.DELAYEDPOINTS
        c=senarioBasicDataset.CAMTRACK
        self.__selectedScheduler.disableModule(0)
        print('disable')

    def Enable(self):
        self.__selectedScheduler.enableModule(0)
        print('enable')


    # def Ensable(self,senario:extScheduler):
    #     print('disable')
    #     self.__selectedScheduler = senario
    #     self.__selectedScheduler.disableModule(0)
    #     print(123)

    def getDataset(self):
        return self.__selectedScheduler.getAllDataset()

    def getRawData(self):
        return self.__selectedScheduler.getAllRawDataset()
