import logging

class staticClass(object):
    mylogger = None

    @classmethod
    def init(cls):
        cls.mylogger = logging.getLogger('SADAT')
        cls.mylogger.setLevel(logging.INFO)
        stream_hander = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s(%(threadName)s) - %(levelname)s - %(message)s')
        stream_hander.setFormatter(formatter)
        cls.mylogger.addHandler(stream_hander)

    @classmethod
    def plogger(cls, message):
        cls.mylogger.info(message)

if __name__ == '__main__':
    staticClass.init()
    staticClass.plogger('test')