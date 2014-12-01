#!/usr/bin/env python

import sys, struct

def main():
  # load files
    # load IMU
    imu_file = open(sys.argv[1], 'rb')
    imu_data = []
    # Mindwave
    mindwave_file = open(sys.argv[2],'rb')

    # Heartrate depending on the laength of sys.argc
    heart_file = None
    heart_data = []
    if sys.argc >= 4:
      heart_file = open(sys.argv[3], 'rb')

    # Read data from IMU file
    while imu_file.peek() is not EOF:
      imu_data.append(imu_file.read())

if __name__ == '__main__':
  main()