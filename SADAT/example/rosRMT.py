from time import sleep

import rospy
import random
from std_msgs.msg import String
from geometry_msgs.msg import PoseArray, Pose


class rmTracker():

    def __init__(self, id):
        self.tid = id
        self.movingstep = 0.05
        self.xmin = -20
        self.xmax = 20
        self.ymin = -5
        self.ymax = 5
        self.points = [random.randint(self.xmin,self.xmax), random.randint(self.ymin,self.ymax), 0]
        self.size = [3, 1.5, 1.5]
        self.dirMap = {0: -1, 1: 1}
        self.direction = [0, 0, 0]
        self.dirRange = [0, 0, 0]
        self.maxdirRange = [0, 0, 0]

        for i in range(3):
            self.validate(i)

    def movingXY(self):
        for pnt in range(2): #only x,y
            self.increaseDirRange(pnt)
            tmpoint = self.points[pnt] + self.direction[pnt] * self.movingstep
            if (pnt == 0 and (tmpoint <= self.xmax and tmpoint >= self.xmin))\
                    or (pnt == 1 and (tmpoint <= self.ymax and tmpoint >= self.ymin)):
                self.points[pnt] = tmpoint
            else:
                self.direction[pnt] *= -1


    def validate(self, pnt):
        self.direction[pnt] = self.dirMap[random.randint(0, 1)]
        self.maxdirRange[pnt] = random.randint(30, 100)
        self.dirRange[pnt] = 0

    def increaseDirRange(self, pnt):
        self.dirRange[pnt] += 1
        if self.dirRange[pnt] == self.maxdirRange[pnt]:
            self.validate(pnt)
            return True
        else:
            return False

    def printPos(self):
        print('tid - ',self.tid, self.points, self.dirRange, self.maxdirRange)

    def toPose(self):
        position = Pose()
        position.position.x = self.points[0]
        position.position.y = self.points[1]
        position.position.z = self.points[2]
        position.orientation.x = 0
        position.orientation.y = 0
        position.orientation.z = 0
        position.orientation.w = 0

        size = Pose()
        size.position.x = self.size[0]
        size.position.y = self.size[1]
        size.position.z = self.size[2]

        data = list()
        data.append(position)
        data.append(size)
        return data

def talker():
    pub = rospy.Publisher('lidar_tracker_geometry', PoseArray, queue_size=10)
    rospy.init_node('LidarTracker', anonymous=True)
    rate = rospy.Rate(10)  # 10hz
    trackers = list()
    for i in range(10):
        trackers.append(rmTracker(i))

    while not rospy.is_shutdown():
        parray = PoseArray()
        for tr in trackers:
            tr.movingXY()
            #tr.printPos()
            for pdata in tr.toPose():
                parray.poses.append(pdata)
        #rospy.loginfo(msg)
        pub.publish(parray)
        rate.sleep()


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
