import numpy

from dadatype.dtype_cate import DataTypeCategory
from dadatype.dtype_track import dtype_track
from dadatype.grp_objects import grp_objects
from sensor.SensorCategory import SensorCategory
from sensor.pSensor import pSensor
from utils.importer import Importer


class ZedTrack(pSensor):
    def __init__(self, name):
        super().__init__(SensorCategory.Track, name)

    def _doWorkDataInput(self, objs):
        ros_numpy = Importer.importerLibrary('ros_numpy')
        header = objs.header
        tracks = grp_objects(dtypecate=DataTypeCategory.TRACK, timestamp=header.stamp)
        for i in range(20):
            tracks.addObject(dtype_track(i, False, posf=numpy.array([0, 0, 0])
                                         , sizef=numpy.array([1, 1, 1])))
        tid = 0  # temporary id
        for obj in objs.objects:
            label = obj.label
            lid = obj.label_id
            # print(label, lid, ':', obj.position[0], obj.position[1], obj.position[2], obj.tracking_state
            #       , obj.confidence, obj.action_state)

            #track = dtype_track(tid, False, posf=obj.position, sizef=numpy.array([1, 1, 1]))
            track = tracks.getObjects()[tid]
            track.setZedObjDetInfo(obj)
            tid += 1
        self.addRealtimeData(tracks)

"""# Standard Header
std_msgs/Header header

# Array of `object_stamped` topics
zed_interfaces/Object[] objects

================================================================================
MSG: std_msgs/Header
# Standard metadata for higher-level stamped data types.
# This is generally used to communicate timestamped data 
# in a particular coordinate frame.
# 
# sequence ID: consecutively increasing ID 
uint32 seq
#Two-integer timestamp that is expressed as:
# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
# time-handling sugar is provided by the client library
time stamp
#Frame this data is associated with
string frame_id

================================================================================
MSG: zed_interfaces/Object
# Object label
string label

# Object label ID
int16 label_id

# Object sub
string sublabel

# Object confidence level (1-99)
float32 confidence

# Object centroid position
float32[3] position

# Position covariance
float32[6] position_covariance

# Object velocity
float32[3] velocity

# Tracking available
bool tracking_available

# Tracking state
# 0 -> OFF (object not valid)
# 1 -> OK
# 2 -> SEARCHING (occlusion occurred, trajectory is estimated)
int8 tracking_state

# Action state
# 0 -> IDLE
# 2 -> MOVING
int8 action_state

# 2D Bounding box projected to Camera image
zed_interfaces/BoundingBox2Di bounding_box_2d

# 3D Bounding box in world frame
zed_interfaces/BoundingBox3D bounding_box_3d

# 3D dimensions (width, height, lenght)
float32[3] dimensions_3d

# Is skeleton available?
bool skeleton_available

# 2D Bounding box projected to Camera image of the person head
zed_interfaces/BoundingBox2Df head_bounding_box_2d

# 3D Bounding box in world frame of the person head
zed_interfaces/BoundingBox3D head_bounding_box_3d

# 3D position of the centroid of the person head
float32[3] head_position

# 2D Person skeleton projected to Camera image
zed_interfaces/Skeleton2D skeleton_2d

# 3D Person skeleton in world frame
zed_interfaces/Skeleton3D skeleton_3d

================================================================================
MSG: zed_interfaces/BoundingBox2Di
#      0 ------- 1
#      |         |
#      |         |
#      |         |
#      3 ------- 2
zed_interfaces/Keypoint2Di[4] corners

================================================================================
MSG: zed_interfaces/Keypoint2Di
uint32[2] kp

================================================================================
MSG: zed_interfaces/BoundingBox3D
#      1 ------- 2
#     /.        /|
#    0 ------- 3 |
#    | .       | |
#    | 5.......| 6
#    |.        |/
#    4 ------- 7
zed_interfaces/Keypoint3D[8] corners

================================================================================
MSG: zed_interfaces/Keypoint3D
float32[3] kp

================================================================================
MSG: zed_interfaces/BoundingBox2Df
#      0 ------- 1
#      |         |
#      |         |
#      |         |
#      3 ------- 2
zed_interfaces/Keypoint2Df[4] corners

================================================================================
MSG: zed_interfaces/Keypoint2Df
float32[2] kp

================================================================================
MSG: zed_interfaces/Skeleton2D
# Skeleton joints indices
#        16-14   15-17
#             \ /
#              0
#              |
#       2------1------5
#       |    |   |    |
#	    |    |   |    |
#       3    |   |    6
#       |    |   |    |
#       |    |   |    |
#       4    8   11   7
#            |   |
#            |   |
#            |   |
#            9   12
#            |   |
#            |   |
#            |   |
#           10   13
zed_interfaces/Keypoint2Df[18] keypoints

================================================================================
MSG: zed_interfaces/Skeleton3D
# Skeleton joints indices
#        16-14   15-17
#             \ /
#              0
#              |
#       2------1------5
#       |    |   |    |
#	    |    |   |    |
#       3    |   |    6
#       |    |   |    |
#       |    |   |    |
#       4    8   11   7
#            |   |
#            |   |
#            |   |
#            9   12
#            |   |
#            |   |
#            |   |
#           10   13
zed_interfaces/Keypoint3D[18] keypoints
"""