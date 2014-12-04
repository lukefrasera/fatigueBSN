import sys
import struct

ANDROID_IMU_DATA_FORMAT_STRING = 'ddddddddd'

def main():
	input_file_name = sys.argv[1]
	output_file_name = sys.argv[2]

	with open(output_file_name, "wb") as out_file:
		with open(input_file_name, "r") as in_file:
			line = in_file.readline()
			while line is not '': # ????????????????????????????????????????????
				clean_data = line_to_clean_data(line)
				if clean_data is not None:
					out_file.write(
						struct.pack(ANDROID_IMU_DATA_FORMAT_STRING, *clean_data)
					)
					line = in_file.readline()
			in_file.close()
		out_file.close()


def line_to_clean_data(line):
	items_as_text = line.split(",")
	data_items = [float(x) for x in items_as_text]



if __name__ == '__main__':
	main()