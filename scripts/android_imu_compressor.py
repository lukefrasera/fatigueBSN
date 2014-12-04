import sys
import struct

""" Takes data from the Android IMU app and turns it into binary data.

Data comes in as csv, data points will be turned into the format:

	Time Stamp    Accelerometer     Gyroscope
					x  y  z          x  y  z
	=========================================
        0           1  2  3          4  5  6
"""

ANDROID_IMU_DATA_FORMAT_STRING = 'ddddddd'
HEADER_SIZE = 25


def main():
	input_file_name = sys.argv[1]
	output_file_name = sys.argv[2]

	with open(output_file_name, "wb") as out_file:
		# write the format header
		out_file.write(
			ANDROID_IMU_DATA_FORMAT_STRING.ljust(HEADER_SIZE, ' ')
		)

		with open(input_file_name, "r") as in_file:
			line = in_file.readline()
			while line is not None: # ??????????????? Is Ok? ??????????????????
				clean_data = line_to_clean_data(line)
				if clean_data is not None:
					out_file.write(
						struct.pack(ANDROID_IMU_DATA_FORMAT_STRING, *clean_data)
					)
				line = in_file.readline()
			in_file.close()
		out_file.close()


def line_to_clean_data(line):
	if '4,' is not in line:
		return None
	else:
		items_as_text = line.split(",")

		if len(items_as_text) <= 13: # expected number of items in line
			return None

		item_values = [float(x) for x in items_as_text]

		data_items = []

		data_items.append(item_values[0]) # time stamp
		data_items.append(item_values[2]) # accelerometer x
		data_items.append(item_values[3]) # accelerometer y
		data_items.append(item_values[4]) # accelerometer z
		data_items.append(item_values[6]) # gyroscope x
		data_items.append(item_values[7]) # gyroscope y
		data_items.append(item_values[8]) # gyroscope z

		print data_items

		return data_items


if __name__ == '__main__':
	main()