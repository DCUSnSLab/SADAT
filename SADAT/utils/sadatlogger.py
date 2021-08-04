import logging

class slog(object):
    mylogger = None

    @classmethod
    def init(cls):
        cls.mylogger = logging.getLogger('SADAT')
        cls.mylogger.setLevel(logging.DEBUG)
        stream_hander = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s(%(processName)s-%(process)d) - %(levelname)s - %(message)s')
        stream_hander.setFormatter(formatter)
        cls.mylogger.addHandler(stream_hander)

    @classmethod
    def DEBUG(cls, message):
        if cls.mylogger is None:
            cls.init()
            print('init mylogger')
        msg = cls.mylogger.debug(message)
        return msg

    @classmethod
    def INFO(cls, message):
        cls.mylogger.info(message)

    @classmethod
    def ERROR(cls, message):
        cls.mylogger.error(message)

    @classmethod
    def WARNING(cls, message):
        cls.mylogger.warning(message)

    @classmethod
    def CRITICAL(cls, message):
        cls.mylogger.critical(message)

    @classmethod
    def addHandler(cls, handler):
        cls.mylogger.addHandler(handler)
    @classmethod
    def removeHandler(cls, handler):
        cls.mylogger.removeHandler(handler)


if __name__ == '__main__':
    slog.init()
    slog.DEBUG('test')
    slog.INFO('test')
    slog.ERROR('test')
    slog.CRITICAL('test')