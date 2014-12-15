#!/usr/bin/env python

from __future__ import print_function
import pylab as pl
import merge_sensor_data as msd

LUKE_FILE = '/home/t/Desktop/fatigueBSN/fatigue_test_data/Luke/12_03_2202_heart.dat'
TERENCE_FILE = '/home/t/Desktop/fatigueBSN/fatigue_test_data/Terence/12_03_2002_cleaned_imu.dat'

def main():
	data = msd.unpack_binary_data_into_list(TERENCE_FILE)

	# data format:
	# timestamp, mean reflex time, reflex time variance, accuracy mean, accuracy variance


	pl.plot(range(len(heart_rate)), heart_rate, label='Heart Rate')
	pl.xlabel("Time (s)")
	pl.ylabel("Heart Rate (BPM)")
	pl.title("Reaction Test Results")
	legend = pl.legend(loc='best', ncol=2, shadow=None)
	legend.get_frame().set_facecolor('#00FFCC')
	pl.show()


if __name__ == '__main__':
	main()