#!/usr/bin/python3

import rospkg

import os
import yaml
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


print("\033[1;32----------\033[0m")
ros_Pack = rospkg.RosPack()
path_ros2pix4d = ros_Pack.get_path('ros2pix4d')

path_file_params = path_ros2pix4d+"/config/params.yaml"
with open(path_file_params, 'r') as f:
    params = yaml.load(f, Loader=yaml.FullLoader)["ros2pix4d"]

path_directory = path_ros2pix4d+"_"+params["rosbag"]["name"]+"/"
try:
    os.mkdir(path_directory)
except:
    pass
print("\033[1;32m-> Data2Plot.\033[0m")

print("\033[1;31m-> Read data.\033[0m")
path_file_gps = path_directory + "Data_GPS.txt"
path_file_imu = path_directory + "Data_IMU.txt"
path_file_img = path_directory + "Data_Img.txt"

data_gps = pd.read_csv(path_file_gps, sep=" ", header=0)
gps_stamp = np.array(data_gps["stamp_nsec"])
gps_stamp = gps_stamp.astype(np.int64)

data_imu = pd.read_csv(path_file_imu, sep=" ", header=0)
imu_stamp = np.array(data_imu["stamp_nsec"])
imu_stamp = imu_stamp.astype(np.int64)

data_img = pd.read_csv(path_file_img, sep=" ", header=0)
img_stamp = np.array(data_img["stamp_nsec"])
img_stamp = img_stamp.astype(np.int64)
print("\033[1;32m-> Ok.\033[0m")

print("\033[1;31m-> Plot.\033[0m")
gps_stamp = gps_stamp - gps_stamp[0]
imu_stamp = imu_stamp - imu_stamp[0]
img_stamp = img_stamp - img_stamp[0]

gps_ones = np.ones(gps_stamp.shape[0])
imu_ones = np.ones(imu_stamp.shape[0])
img_ones = np.ones(img_stamp.shape[0])

# plt.plot(gps_stamp[:1000], gps_ones[:1000], ".")
# plt.plot(imu_stamp[:1000], imu_ones[:1000], ".")
# plt.plot(img_stamp[:1000], img_ones[:1000], ".")
# plt.show()

plt.plot(gps_stamp, gps_ones, ".")
plt.plot(imu_stamp, imu_ones, ".")
plt.plot(img_stamp, img_ones, ".")
plt.show()

print("\033[1;33----------\033[0m")
