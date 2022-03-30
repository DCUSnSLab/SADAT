from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem


class vehicleInfoTree(QTreeWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.atree()

    def atree(self):
        self.setAlternatingRowColors(True)
        self.header().setVisible(True)
        self.setColumnWidth(0,250)
        self.headerItem().setText(0, "Display")
        self.headerItem().setText(1, " ")
        self.root = self.invisibleRootItem()

        itemTop1 = QTreeWidgetItem(self)
        itemTop1.setText(0, "Vehicle Info")

        #IMU
        itemChildIMU = QTreeWidgetItem(itemTop1)
        itemChildIMU.setText(0, "IMU")

        #IMU_angular velocity
        itemChildAngular = QTreeWidgetItem(itemChildIMU)
        itemChildAngular.setText(0, "angular velocity")
        itemChildAngularx = QTreeWidgetItem(itemChildAngular)
        itemChildAngularx.setText(0, "x")
        itemChildAngularx.setText(1, "0")
        itemChildAngulary = QTreeWidgetItem(itemChildAngular)
        itemChildAngulary.setText(0, "y")
        itemChildAngulary.setText(1, "0")
        itemChildAngularz = QTreeWidgetItem(itemChildAngular)
        itemChildAngularz.setText(0, "z")
        itemChildAngularz.setText(1, "0")

        #IMU_linear_acceleration
        itemChildLinear = QTreeWidgetItem(itemChildIMU)
        itemChildLinear.setText(0, "linear_acceleration")
        itemChildLinearx = QTreeWidgetItem(itemChildLinear)
        itemChildLinearx.setText(0, "x")
        itemChildLinearx.setText(1, "0")
        itemChildLineary = QTreeWidgetItem(itemChildLinear)
        itemChildLineary.setText(0, "y")
        itemChildLineary.setText(1, "0")
        itemChildLinearz = QTreeWidgetItem(itemChildLinear)
        itemChildLinearz.setText(0, "z")
        itemChildLinearz.setText(1, "0")

        #vesc_commands
        itemChild2 = QTreeWidgetItem(itemTop1)
        itemChild2.setText(0, "vesc")
        itemChild3 = QTreeWidgetItem(itemChild2)
        itemChild3.setText(0, "commands")

        #moter_speed
        itemChild4 = QTreeWidgetItem(itemChild3)
        itemChild4.setText(0, "motor/speed")
        itemChild4.setText(1, "0")

        #servo/position
        itemChild5 = QTreeWidgetItem(itemChild3)
        itemChild5.setText(0, "servo/position")
        itemChild5.setText(1, "0")

        #odometry
        itemChildOdom = QTreeWidgetItem(itemChild3)
        itemChildOdom.setText(0, "odom")
        itemChildPose = QTreeWidgetItem(itemChildOdom)
        itemChildPose.setText(0, "pose")
        itemChildTwist = QTreeWidgetItem(itemChildOdom)
        itemChildTwist.setText(0, "twist") # linear,angular 2개 자식 존제(2개다 x,y,z

        #Odom_position
        itemChildodomPosition = QTreeWidgetItem(itemChildPose)
        itemChildodomPosition.setText(0,"position")
        itemChildodomPositionx = QTreeWidgetItem(itemChildodomPosition)
        itemChildodomPositionx.setText(0, "x")
        itemChildodomPositionx.setText(1, "0")
        itemChildodomPositiony = QTreeWidgetItem(itemChildodomPosition)
        itemChildodomPositiony.setText(0, "y")
        itemChildodomPositiony.setText(1, "0")
        itemChildodomPositionz = QTreeWidgetItem(itemChildodomPosition)
        itemChildodomPositionz.setText(0, "z")
        itemChildodomPositionz.setText(1, "0")

        #Odom_orientation
        itemChildodomOrientation = QTreeWidgetItem(itemChildPose)
        itemChildodomOrientation.setText(0, "orientation")
        itemChildodomOrientationx = QTreeWidgetItem(itemChildodomOrientation)
        itemChildodomOrientationx.setText(0, "x")
        itemChildodomOrientationx.setText(1, "0")
        itemChildodomOrientationy = QTreeWidgetItem(itemChildodomOrientation)
        itemChildodomOrientationy.setText(0, "y")
        itemChildodomOrientationy.setText(1, "0")
        itemChildodomOrientationz = QTreeWidgetItem(itemChildodomOrientation)
        itemChildodomOrientationz.setText(0, "z")
        itemChildodomOrientationz.setText(1, "0")
        itemChildodomOrientationw = QTreeWidgetItem(itemChildodomOrientation)
        itemChildodomOrientationw.setText(0, "w")
        itemChildodomOrientationw.setText(1, "0")

        # Odom_linear
        itemChildodomLinear = QTreeWidgetItem(itemChildTwist)
        itemChildodomLinear.setText(0, "linear")
        itemChildodomLinearx = QTreeWidgetItem(itemChildodomLinear)
        itemChildodomLinearx.setText(0, "x")
        itemChildodomLinearx.setText(1, "0")
        itemChildodomLineary = QTreeWidgetItem(itemChildodomLinear)
        itemChildodomLineary.setText(0, "y")
        itemChildodomLineary.setText(1, "0")
        itemChildodomLinearz = QTreeWidgetItem(itemChildodomLinear)
        itemChildodomLinearz.setText(0, "z")
        itemChildodomLinearz.setText(1, "0")

        # Odom_angular
        itemChildodomAngular = QTreeWidgetItem(itemChildTwist)
        itemChildodomAngular.setText(0, "angular")
        itemChildodomAngularx = QTreeWidgetItem(itemChildodomAngular)
        itemChildodomAngularx.setText(0, "x")
        itemChildodomAngularx.setText(1, "0")
        itemChildodomAngulary = QTreeWidgetItem(itemChildodomAngular)
        itemChildodomAngulary.setText(0, "y")
        itemChildodomAngulary.setText(1, "0")
        itemChildodomAngularz = QTreeWidgetItem(itemChildodomAngular)
        itemChildodomAngularz.setText(0, "z")
        itemChildodomAngularz.setText(1, "0")

