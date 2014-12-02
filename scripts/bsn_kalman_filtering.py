from mergeSensorData import *
from pykalman import KalmanFilter


BSN_DATA_FILE_NAME = "bsn_data.dat"
FILTERED_BSN_DATA_FILE_NAME = "filtered_bsn_data.dat"
MODEL_DIMENSIONALITY = 3 +  # IMU
					   3 +  # Mindwave
				       0    # PH7

if __name__ == "__main__":
	main()

def main():
	# get the data
	bsn_data, data_format = unpack_binary_data_into_list(BSN_DATA_FILE_NAME)

	# initialize filter
	# (all constructor parameters have defaults, and pykalman supposedly does a
	# good job of estimating them, so we will be lazy until there is a need to
	# define the initial parameters)
	bsn_kfilter = KalmanFilter(n_dim_obs = len(data_format))
	
	# perform parameter estimation and do predictions
	filtered_bsn_data = bsn_kfilter.em(bsn_data, 'all').smooth(bsn_data)[0]

	# write the data to a new file
	with open(FILTERED_BSN_DATA_FILE_NAME, "wb") as filtered_file:
		filtered_file.write(ljust(25, data_format))
		for filtered_item in filtered_bsn_data:
			filtered_file.write(struct.pack(data_format, filtered_item))
		filtered_file.close()

