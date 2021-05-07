# import message_filters
# import rospy
# from sensor_msgs.msg import Image, CameraInfo, CompressedImage, LaserScan
#
# cdata = 1
#
# def callback(image, info):
#     gap = image.header.stamp.to_sec() - info.header.stamp.to_sec()
#     print("%.3f - %.3f, gap = %.4f"%(image.header.stamp.to_sec(), info.header.stamp.to_sec(), gap))
#
#   # Solve all of perception here...
#
# def scallback(data):
#     print(data)
#
#
# rospy.init_node('syncgrabber', anonymous=True)
# image_sub = message_filters.Subscriber('/usb_cam/image_raw/compressed', CompressedImage)
# info_sub = message_filters.Subscriber('/scan', LaserScan)
#
# ts = message_filters.ApproximateTimeSynchronizer([image_sub, info_sub], 10, 0.1, allow_headerless=True)
# ts.registerCallback(callback)
# #sub = rospy.Subscriber('/usb_cam/image_raw/compressed', CompressedImage, scallback)
# rospy.spin()