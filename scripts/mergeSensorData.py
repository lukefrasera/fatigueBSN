#!/usr/bin/env python

import sys, struct

def unpack_binary_data_into_list(file_name):
  data_points = []
  file_ = open(filename)
  fmt = file_.read(25).rstrip()
  struct_size = struct.calcsize(fmt)

  for packed_struct in packed_structs_from_file(file_, struct_size):
    if packed_struct is not None:
      data_tuple = struct.unpack(fmt, packed_struct)
      data_points.append(data_tuple)
  file_.close()
  return data_points


def packed_structs_from_file(file_, struct_size):
  while True:
    struct_data = file_.read(struct_size)
    if struct_data:
      yield struct_data
    else:
      break
  yield None

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
    imu_data      = unpack_binary_data_into_list(imu_file)
    mindwave_data = unpack_binary_data_into_list(mindwave_file)
    heart_data    = unpack_binary_data_into_list(heart_file)


if __name__ == '__main__':
  main()