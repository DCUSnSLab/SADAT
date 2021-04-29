import logging

class slog(object):
    mylogger = None

    @classmethod
    def init(cls):
        cls.mylogger = logging.getLogger('SADAT')
        cls.mylogger.setLevel(logging.DEBUG)
        stream_hander = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s(%(threadName)s) - %(levelname)s - %(message)s')
        stream_hander.setFormatter(formatter)
        cls.mylogger.addHandler(stream_hander)

    @classmethod
    def DEBUG(cls, message):
        cls.mylogger.debug(message)

    @classmethod
    def INFO(cls, message):
        cls.mylogger.info(message)

    @classmethod
    def ERROR(cls, message):
        cls.mylogger.error(message)

    @classmethod
    def CRITICAL(cls, message):
        cls.mylogger.critical(message)

if __name__ == '__main__':
    slog.init()
    slog.DEBUG('test')
    slog.INFO('test')
    slog.ERROR('test')
    slog.CRITICAL('test')