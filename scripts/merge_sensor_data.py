#!/usr/bin/env python

""" Merges data into a format ready for data processing.

    Final Data Format (?):
    Time, label, Low-Alpha, High-Alpha, Heart Rate, IMU angle
"""

import sys
import struct

import reaction_test_visualizer as rtv


LUKE_FILE = '/home/t/Desktop/fatigueBSN/fatigue_test_data/Luke/12_03_2240_reaction.dat'
TERENCE_FILE = '/home/t/Desktop/fatigueBSN/fatigue_test_data/Terence/12_03_2002_reaction.dat'


def main():
    # load files
    # load IMU
    imu_file = sys.argv[1]
    imu_data = []
    # Mindwave
    mindwave_file = sys.argv[2]

    # Heartrate depending on the length of sys.argc
    heart_file = None
    heart_data = []
    if len(sys.argv) >= 4:
      heart_file = sys.argv[3]

    # Read data from IMU file
    imu_data, fmt_imu = unpack_binary_data_into_list(imu_file)
    mindwave_data, fmt_mind = unpack_binary_data_into_list(mindwave_file)
    heart_data, fmt_heart = unpack_binary_data_into_list(heart_file)

    # interpolate the data
    merged_data = interpolate_data(imu_data, heart_data)

    # Save data
    f = open(sys.argv[1], 'wb')
    fmt_merge = fmt_imu + fmt_mind + fmt_heart if fmt_heart else ''
    f.write(fmt_merge.ljust(25, ' '))
    for row in merged_data:
        f.write(struct.pack(fmt_merge, *row))
    f.close()


def unpack_binary_data_into_list(file_name):
    data_points = []
    file_ = open(file_name, 'rb')
    fmt = file_.read(25).rstrip()
    struct_size = struct.calcsize(fmt)

    for packed_struct in packed_structs_from_file(file_, struct_size):
        if packed_struct is not None:
            data_tuple = struct.unpack(fmt, packed_struct)
            data_points.append(list(data_tuple))
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


def interpolate_data(leader_data, *data_lists):
    # maps from list (0 for leader_data or varargs_index + 1) to indices of
    # first and last data points to be used
    merge_list = []
    for i, row in enumerate(leader_data):
        current_time = row[0]
        merge_list.append(row)
        for arg in data_lists:
            # Find local indices around data
            low, high = local_indicies(current_time, arg)
            merge_list[i] += interpolate(current_time, arg[low], arg[high])
    return merge_list


def local_indicies(lead_step, child_steps):
    """
    Returns a tuple of indices surrounding the lead_step
    """
    imin = 0
    imax = len(child_steps) - 1
    mid = 0
    while imin < imax:
        mid = (imax + imin)/2
        if(child_steps[mid][0] < lead_step):
            imin = mid + 1
        else:
            imax = mid
    if child_steps[mid][0] < lead_step:
        return (mid, mid+1)
    return mid-1,mid


def interpolate(time, low_val_list, high_val_list):
    """
    Returns a list of interpolated values from the low and high list
    """
    d_t = high_val_list[0] - low_val_list[0]
    x1 = low_val_list[0]
    result = []
    for y1,y2 in map(lambda a,b: (a,b),low_val_list[1:], high_val_list[1:]):
        d_y = y2 - y1
        m = d_y/d_t
        b = y1 - m*x1
        result.append(m * time + b)
    return result


def tag_data(reaction_data_file_name, data):
    reaction_data = rtv.generate_labels_with_times(
        rtv.read_reaction_data_into_list(reaction_data_file_name),
        1.1
    )
    tagged_data = []
    j = 0
    for item in data:
        if reaction_data[j + 1] < item[0]:
            j += 1
        tagged_data.append((reaction_data[j], item[2:]))

    return tagged_data


if __name__ == '__main__':
    main()
    # x = [[1.2,1.1,2.1], [1.5,3.2,4.1], [1.8, 4.2,6.5], [2.1,7.0,1.2], [2.5,9.1,1.6], [2.7,10,11.1]]
    # y = [[.1,1,2,3],[.2,1,2,3],[.3,1,2,3],[.4,1,2,3],[.5,1,2,3],[.6,1,2,3],[.7,1,2,3],[.8,1,2,3],[.9,1,2,3],[1.0,1,2,3],[1.1,1,2,3],[1.2,1,2,3],[1.3,1,2,3]]
    # print interpolate_data(y,x,x)
    # low, high = local_indicies(y,x)
    # print low, high
    # print interpolate(y, x[low], x[high])