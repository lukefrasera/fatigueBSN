#!/usr/bin/env python

from __future__ import print_function
from mergeSensorData import unpack_binary_data_into_list
from pykalman import KalmanFilter
import struct
import string


BSN_DATA_FILE_NAME =\
	"/home/t/Desktop/fatigueBSN/fatigue_test_data/LukeFraser_Nov_30_IMU.dat"
FILTERED_BSN_DATA_FILE_NAME = "filtered_bsn_data.dat"

def main():
	# get the data
	bsn_data, data_format = unpack_binary_data_into_list(BSN_DATA_FILE_NAME)
	print("format string: {}".format(data_format))
	for datum in bsn_data:
		print(datum)

	# initialize filter
	# (all constructor parameters have defaults, and pykalman supposedly does a
	# good job of estimating them, so we will be lazy until there is a need to
	# define the initial parameters)
	bsn_kfilter = KalmanFilter(n_dim_obs = len(data_format))
	
	# perform parameter estimation and do predictions
	filtered_bsn_data = bsn_kfilter.em(bsn_data, 'all').smooth(bsn_data)[0]

	# write the data to a new file
	with open(FILTERED_BSN_DATA_FILE_NAME, "wb") as filtered_file:
		filtered_file.write(string.ljust(data_format, 25))
		for filtered_item in filtered_bsn_data:
			print(filtered_item)
			filtered_file.write(struct.pack(data_format, *filtered_item))
		filtered_file.close()

if __name__ == "__main__":
	main()
