from externalmodules.extModule import extModule


class trackerBasic(extModule):
    def __init__(self,):
        super().__init__('trackerBasic')

    def do(self):
        print('do ExtModules -->', self.getName())