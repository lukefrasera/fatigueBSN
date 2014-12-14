#!/usr/bin/env python

from __future__ import print_function
import pylab as pl
import struct
import merge_sensor_data as msd

import merge_sensor_data as msd

def main():
	data = msd.unpack_binary_data_into_list (
		'/home/t/Desktop/fatigueBSN/fatigue_test_data/Terence/12_03_2002_heart.dat'
	)

	print(data[0][0])

	# data format:
	# timestamp, mean reflex time, reflex time variance, accuracy mean, accuracy variance
	timestamp = [x[0] for x in data[0]]
	heart_rate = [float(x[1]) for x in data[0]]

	pl.plot(range(len(heart_rate)), heart_rate, label='Heart Rate')
	pl.xlabel("Time Step")
	pl.ylabel("BPM")
	legend = pl.legend(loc='best', ncol=2, shadow=None)
	legend.get_frame().set_facecolor('#00FFCC')
	pl.show()


if __name__ == '__main__':
	main()