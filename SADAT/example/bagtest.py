import rosbag
bag = rosbag.Bag('/home/soobin/development/dataset/2021_07_22_outdoor_centerpark.bag')

rmsg = bag.read_messages()
for topic, msg, t in rmsg:
    print(topic, t, msg)
    break
bag.close()