#!/usr/bin/python3

import rospkg
import rosbag

import os
import time
import yaml

import cv2
from cv_bridge import CvBridge, CvBridgeError


class DataGPS:

    def __init__(self, path_directory):
        self.path_directory = path_directory
        self.stamp_nsec = []
        self.latitude = []
        self.longitude = []
        self.altitude = []

    def callback_gps(self, gps_ros):
        self.stamp_nsec.append(gps_ros.header.stamp.to_nsec())
        self.latitude.append(gps_ros.latitude)
        self.longitude.append(gps_ros.longitude)
        self.altitude.append(gps_ros.altitude)

    def save(self):
        file = self.path_directory+"Data_GPS.txt"
        N = len(self.stamp_nsec)
        with open(file, "w+") as f:
            f.write("stamp_nsec latitude longitude altitude\n")
            for idx in range(0, N):
                f.write(str(self.stamp_nsec[idx]) + " ")
                f.write(str(self.latitude[idx]) + " ")
                f.write(str(self.longitude[idx]) + " ")
                f.write(str(self.altitude[idx]) + "\n")


class DataIMU:

    def __init__(self, path_directory):
        self.path_directory = path_directory
        self.stamp_nsec = []
        self.qx = []
        self.qy = []
        self.qz = []
        self.qw = []

    def callback_imu(self, imu_ros):
        self.stamp_nsec.append(imu_ros.header.stamp.to_nsec())
        self.qx.append(imu_ros.orientation.x)
        self.qy.append(imu_ros.orientation.y)
        self.qz.append(imu_ros.orientation.z)
        self.qw.append(imu_ros.orientation.w)

    def save(self):
        file = self.path_directory+"Data_IMU.txt"
        N = len(self.stamp_nsec)
        with open(file, "w+") as f:
            f.write("stamp_nsec qx qy qz qw\n")
            for idx in range(0, N):
                f.write(str(self.stamp_nsec[idx]) + " ")
                f.write(str(self.qx[idx]) + " ")
                f.write(str(self.qy[idx]) + " ")
                f.write(str(self.qz[idx]) + " ")
                f.write(str(self.qw[idx]) + "\n")


class DataImg:

    def __init__(self, path_directory, path_directory_img):
        self.path_directory = path_directory
        self.path_directory_img = path_directory_img
        self.cv_bridge = CvBridge()
        self.stamp_nsec = []

    def callback_img(self, img_ros):
        stamp_nsec = img_ros.header.stamp.to_nsec()
        self.stamp_nsec.append(stamp_nsec)

        path_img = ""
        path_img += self.path_directory_img
        path_img += str(stamp_nsec)
        path_img += ".jpg"

        try:
            img = self.cv_bridge.imgmsg_to_cv2(img_ros, "passthrough")
            cv2.imwrite(path_img, img)
        except CvBridgeError:
            pass

    def save(self):
        file = self.path_directory+"Data_Img.txt"
        N = len(self.stamp_nsec)
        with open(file, "w+") as f:
            f.write("stamp_nsec\n")
            for idx in range(0, N):
                f.write(str(self.stamp_nsec[idx]) + "\n")


print("\033[1;32----------\033[0m")
ros_Pack = rospkg.RosPack()
path_ros2pix4d = ros_Pack.get_path('ros2pix4d')

path_file_params = path_ros2pix4d+"/config/params.yaml"
with open(path_file_params, 'r') as f:
    params = yaml.load(f, Loader=yaml.FullLoader)["ros2pix4d"]

path_directory = path_ros2pix4d+"_"+params["rosbag"]["name"]+"/"
path_directory_img = path_directory + "img/"
try:
    os.mkdir(path_directory)
except:
    pass
try:
    os.mkdir(path_directory_img)
except:
    pass
print("\033[1;32m-> Rosbag2data.\033[0m")
time_tic = time.time()

print("\033[1;31m-> Open rosbag.\033[0m")
path_file_rosbag = (params["rosbag"]["path"] + "/" +
                    params["rosbag"]["name"]+".bag")
data_rosbag = rosbag.Bag(path_file_rosbag)
print("\033[1;32m-> Ok.\033[0m")

print("\033[1;31m-> Read data.\033[0m")
topic_gps = params["topics"]["gps"]
topic_imu = params["topics"]["imu"]
topic_cam = params["topics"]["cam"]

data_topics = []
data_topics.append(topic_gps)
data_topics.append(topic_imu)
data_topics.append(topic_cam)

data_gps = DataGPS(path_directory)
data_imu = DataIMU(path_directory)
data_img = DataImg(path_directory, path_directory_img)

for topic_msg, msg, _ in data_rosbag.read_messages(topics=data_topics):
    if topic_msg == topic_gps:
        data_gps.callback_gps(msg)
    elif topic_msg == topic_imu:
        data_imu.callback_imu(msg)
    elif topic_msg == topic_cam:
        data_img.callback_img(msg)

data_rosbag.close()
print("\033[1;32m-> Ok.\033[0m")

print("\033[1;31m-> save_data.\033[0m")
data_gps.save()
data_imu.save()
data_img.save()
print("\033[1;32m-> Ok.\033[0m")

time_final = time.time()-time_tic
print("\033[1;32m-> time =\033[0m", time_final)

print("\033[1;33----------\033[0m")
