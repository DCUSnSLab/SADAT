class rosInstance():
    def __init__(self):
        self.isloaded = False

        try:
            self.rospy = __import__("rospy")
            self.sensor_msgs = __import__("sensor_msgs")
            self.msg = getattr(self.sensor_msgs, 'msg')
            self.LaserScan = getattr(self.msg, 'LaserScan')
            self.isloaded = True

        except ImportError as error:
            print('ros import error')
