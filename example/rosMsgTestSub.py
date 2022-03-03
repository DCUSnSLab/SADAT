import rospy
from geometry_msgs.msg import Pose, PoseArray
from zed_interfaces.msg import ObjectsStamped

def callback(data):
    for obj in data.objects:
        label = obj.label
        lid = obj.label_id
        print(label, lid, ':', obj.position[0], obj.position[1], obj.position[2], obj.tracking_state
              , obj.confidence, obj.action_state)

    print('-------------------')


def listener():
    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("/zed2/zed_node/obj_det/objects", ObjectsStamped, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


if __name__ == '__main__':
    listener()