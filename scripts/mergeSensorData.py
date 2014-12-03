#!/usr/bin/env python

import sys, struct

def unpack_binary_data_into_list(file_name):
  data_points = []
  file_ = open(file_name)
  fmt = file_.read(25).rstrip()
  struct_size = struct.calcsize(fmt)

  for packed_struct in packed_structs_from_file(file_, struct_size):
    if packed_struct is not None:
      data_tuple = struct.unpack(fmt, packed_struct)
      data_points.append(data_tuple)
  file_.close()
  return data_points, fmt


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


	# interpolate the data
	merged_data = interpolate_data(imu_data, mindwave_data, heart_data)


def interpolate_data(leader_data, *other_data_lists):
	# maps from list (0 for leader_data or varargs_index + 1) to indices of
	# first and last data points to be used
	bounding_indices = {}

	

if __name__ == '__main__':
  main()
