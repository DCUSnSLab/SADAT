import math
from datetime import datetime

import rospy
import time

# imu 메시지 사용준비
from sensor_msgs.msg import Imu
from tf.transformations import euler_from_quaternion

# euler_from_quaternion 함수 사용준비
Imu_msg = None


# IMU데이터가 들어오면 실행되는 콜백함수 정의
def imu_callback(data):
    global Imu_msg
    global Imu_lacc
    Imu_msg = [data.orientation.x, data.orientation.y, data.orientation.z, data.orientation.w]
    Imu_lacc = [data.linear_acceleration.x, data.linear_acceleration.y, data.linear_acceleration.z]
rospy.init_node("Imu_print")
rospy.Subscriber("imu", Imu, imu_callback)

Velocity_old_x = 0
prevtime = datetime.now()
while not rospy.is_shutdown():
    if Imu_msg == None:
        continue

    # 쿼터니언 값을 roll, pitch, yaw 값으로 변환
    (roll, pitch, yaw) = euler_from_quaternion(Imu_msg)
    (accx, accy, accz) = Imu_lacc
    acceleration_x = (accx + 9.81 * math.sin(pitch)) *math.cos(pitch);
    acceleration_y = (accy - 9.81 * math.sin(roll))  *math.cos(roll);
    #print('Roll:%.4f, pitch:%.4f, Yaw:%.4f' % (roll, pitch, yaw))
    #print('Acc X:%.4f, Acc Y:%.4f, Acc Z:%.4f' % (acceleration_x, acceleration_y, 0))

    ctime = datetime.now()
    dt = (ctime - prevtime).microseconds / 1000000
    #velocity
    Velocity_x = Velocity_old_x + acceleration_x * dt;
    print('vel - ',(Velocity_x*3.6), dt)
    # 화면에 roll, pitch, yaw 값 출력
    Velocity_old_x = Velocity_x
    prevtime = ctime
    time.sleep(0.1)