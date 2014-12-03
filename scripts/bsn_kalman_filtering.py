#!/usr/bin/env python

from __future__ import print_function
from mergeSensorData import unpack_binary_data_into_list
import numpy as np
from pykalman import KalmanFilter
import struct
import string


BSN_DATA_FILE_NAME =\
	"/home/t/Desktop/fatigueBSN/fatigue_test_data/LukeFraser_Nov_30_IMU.dat"
FILTERED_BSN_DATA_FILE_NAME = "filtered_bsn_data.dat"

def main():
	# get the data
	readings, data_format = unpack_binary_data_into_list(BSN_DATA_FILE_NAME)
	# just the data/readings, no timestamps
	bsn_data = np.array([x[1:] for x in readings])

	print("list length: {}".format(len(bsn_data)))
	print("item length: {}".format(len(bsn_data[0])))
			
	# initialize filter
	# (all constructor parameters have defaults, and pykalman supposedly does a
	# good job of estimating them, so we will be lazy until there is a need to
	# define the initial parameters)
	print("Number of items to smooth: {}".format(len(bsn_data)))
	bsn_kfilter = KalmanFilter(
		n_dim_state = len(bsn_data[0]),
		n_dim_obs = len(bsn_data),
		em_vars = 'all'
		#[
		#	'transition_matrices', 'observation_matrices',
		#	'transition_covariance', 'observation_covariance',
		#	'observation_offsets', 'initial_state_mean',
		#	'initial_state_covariance'
    	#]
    )
	
	# perform parameter estimation and do predictions
	print("Estimating parameters...")
	bsn_kfilter.em(X = bsn_data)
	print("Creating smoothed estimates...")
	filtered_bsn_data = bsn_kfilter.smooth(bsn_data)[0]
	print(type(filtered_bsn_data))
	print(filtered_bsn_data)
	print(type(filtered_bsn_data[0]))
	print(filtered_bsn_data[0])

	# write the data to a new file
	with open(FILTERED_BSN_DATA_FILE_NAME, "wb") as filtered_file:
		filtered_file.write(string.ljust(data_format, 25))
		for filtered_item in filtered_bsn_data:
			print(filtered_item)
			filtered_file.write(struct.pack(data_format, *filtered_item))
		filtered_file.close()

if __name__ == "__main__":
	main()
