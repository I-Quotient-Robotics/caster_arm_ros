#!/usr/bin/env python

import sys
import math

import PyKDL

import rospy
import moveit_commander
from tf_conversions import posemath

from geometry_msgs.msg import Pose, PoseArray
from control_msgs.msg import GripperCommandActionGoal

from rail_manipulation_msgs.srv import SegmentObjects
from rail_manipulation_msgs.msg import SegmentedObject, SegmentedObjectList


standby_angles = [4.798158746451781, 2.906056295196569, 0.6865793074631316, 6.274263184895603, 3.8105518214906877, 3.232796599861192]
place_angles = [4.6941633711486235, 2.2671501012488915, 1.4487019755655053, -0.0011303618198529944, 3.9173395211967943, 3.042449025160541]


class PickPlace:
    def __init__(self):
        self.__robot = moveit_commander.RobotCommander("robot_description")
        self.__scene = moveit_commander.PlanningSceneInterface(ns=rospy.get_namespace())

        self.__arm_group = moveit_commander.MoveGroupCommander('arm', ns=rospy.get_namespace())
        # self.__arm_group.set_max_velocity_scaling_factor(0.4)

        self.__gripper_group = moveit_commander.MoveGroupCommander('gripper', ns=rospy.get_namespace())

        self.__object_pose_array_pub = rospy.Publisher('object_pose_array', PoseArray, queue_size=10)
        self.__rail_segmentation_proxy = rospy.ServiceProxy('/rail_segmentation_node/segment_objects', SegmentObjects)

    def __set_gripper(self, state):
        if state:
            self.__gripper_group.set_named_target('open')
        else:
            self.__gripper_group.set_named_target('close')

        self.__gripper_group.go(wait=True)

    def __move_by_pose(self, target_pose):
        self.__arm_group.set_pose_target(target_pose)
        return self.__arm_group.go(wait=True)

    def __move_by_name(self, target_name):
        self.__arm_group.set_named_target(target_name)
        return self.__arm_group.go(wait=True)

    def __move_by_joint_angle(self, target_angle):
        self.__arm_group.set_joint_value_target(target_angle)
        return self.__arm_group.go(wait=True)

    def run(self):
        try:
            rospy.loginfo("get objects")
            seg_response = self.__rail_segmentation_proxy()
            rospy.loginfo("get %d object", len(seg_response.segmented_objects.objects))

            if len(seg_response.segmented_objects.objects) is 0:
                rospy.loginfo('no object found')
                return

            # publish object axis
            pose_array = PoseArray()
            pose_array.header.stamp = rospy.Time.now()
            pose_array.header.frame_id = "base_footprint"
            for obj in seg_response.segmented_objects.objects:
                pose_array.poses.append(obj.bounding_volume.pose.pose)
            self.__object_pose_array_pub.publish(pose_array)

            # use first object as target object
            p = posemath.fromMsg(seg_response.segmented_objects.objects[0].bounding_volume.pose.pose)

            rospy.loginfo("open gripper")
            self.__set_gripper(True)
            rospy.sleep(1.0)

            rospy.loginfo("pre touch")
            f = PyKDL.Frame(PyKDL.Rotation.RPY(-math.pi/2.0, 0, math.pi/2.0), PyKDL.Vector(0.05, 0, 0))
            self.__move_by_pose(posemath.toMsg(p*f))

            rospy.loginfo("touch")
            f = PyKDL.Frame(PyKDL.Rotation.RPY(-math.pi/2.0, 0, math.pi/2.0), PyKDL.Vector(0.02, 0, 0))
            self.__move_by_pose(posemath.toMsg(p*f))

            rospy.loginfo("close gripper")
            self.__set_gripper(False)

            rospy.loginfo("leave up")
            f = PyKDL.Frame(PyKDL.Rotation.RPY(-math.pi/2.0, 0, math.pi/2.0), PyKDL.Vector(0.05, 0, 0))
            self.__move_by_pose(posemath.toMsg(p*f))

            rospy.loginfo('standby')
            self.__move_by_joint_angle(standby_angles)

            rospy.loginfo('place')
            self.__move_by_joint_angle(place_angles)

            rospy.loginfo("open gripper")
            self.__set_gripper(True)
            rospy.sleep(1.0)

            rospy.loginfo('standby')
            self.__move_by_joint_angle(standby_angles)

        except rospy.ServiceException as exc:
            rospy.logwarn("rail segmentation service did not process request: " + str(exc))

    def initialize(self):
        rospy.loginfo('standby')
        self.__move_by_joint_angle(standby_angles)


def main():
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('pick_place_demo_node')

    pick_place = PickPlace()
    pick_place.initialize()

    rate = rospy.Rate(0.4)
    while not rospy.is_shutdown():
        pick_place.run()
        rate.sleep()


if __name__ == '__main__':
    main()
