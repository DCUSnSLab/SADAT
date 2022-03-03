from externalmodules.default.dataset_enum import senarioBasicDataset
from externalmodules.default.delayed_points import delayedPoints
from externalmodules.default.tracker import trackerBasic
from externalmodules.extModule import extModule
from externalmodules.ext_scheduler import extScheduler
from enum import Enum

from utils.sadatlogger import slog


class senarioBasic(extScheduler):
    def __init__(self):
        super().__init__('senario basic')
        slog.DEBUG('-----init senario basic-----')

    def dataConstruction(self):
        self._initDataset(senarioBasicDataset.TRACK, list())
        self._initDataset(senarioBasicDataset.CAMTRACK, list()) #temporary
        self._initDataset(senarioBasicDataset.DELAYEDPOINTS, list())

        slog.DEBUG('-data Construction loaded')
        for key in self._dataset.keys():
            slog.DEBUG(key)

    def modConstruction(self):
        #self._addModules([delayedPoints(), trackerBasic()])
        self._addModules([trackerBasic()])
        slog.DEBUG('-load Modules')
        for mod in self._modules:
            slog.DEBUG(self.name+mod.getName())