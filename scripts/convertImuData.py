#!/usr/bin/env python

import struct, sys, re

def main():
  imu_file = open(sys.argv[1], 'r')
  for i in xrange(7):
    imu_file.readline()

  imu_data = []
  for line in imu_file:
    img_data.append(re.split('\t',line[:-1]))

if __name__ == '__main__':
  main()
