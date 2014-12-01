#!/usr/bin/python

__author__ = 't'

import collections
import struct
from ghmm import *
from fatigueBSN_model.BSNDataPoint import *

DATA_FORMAT_STRING = 'ddddddddd'


def main():
    # TODO: get a list of data points
    data_points = unpack_binary_data_into_list("training.dat")

    print 'number of time stamps: ', len(data_points)
    print 'duration of experiment: ',\
        data_points[len(data_points) - 1].timestamp - data_points[0].timestamp

    training_emissions = \
        [point.to_discrete_emission_string() for point in data_points]
    training_labels = [point.label for point in data_points]

    print training_emissions
    print training_labels

    # aka sigma
    emission_aplphabet = EMISSION_ALPHABET

    # aka pi
    initial_state_model = [0.9,  # non-fatigue
                           0.1]  # fatigue
    # aka A
    state_transition_matrix = [[0.7, 0.3],    # non-fatigue
                               [0.1, 0.9]]    # fatigue

    non_fatigue_emission_probabilities = [
        0.3,   # 'aaa'
        0.15,  # 'aab'
        0.1,   # 'aba'
        0.1,   # 'abb'
        0.1,   # 'baa'
        0.1,   # 'bab'
        0.1,   # 'bba'
        0.05   # 'bbb'
    ]

    fatigue_emission_probabilities = [
        0.1,  # 'aaa'
        0.1,  # 'aab'
        0.1,  # 'aba'
        0.1,  # 'abb'
        0.1,  # 'baa'
        0.1,  # 'bab'
        0.1,  # 'bba'
        0.3   # 'bbb'
    ]

    # aka B
    emission_likelihood_matrix = [non_fatigue_emission_probabilities,
                                  fatigue_emission_probabilities]

    # simply initialize the model
    bsn_hmm_model = HMMFromMatrices(
        emission_aplphabet,         # sigma: the alphabet
        DiscreteDistribution(       # ???
            emission_aplphabet
        ),
        state_transition_matrix,     # A: state transitions model matrix
        emission_likelihood_matrix,  # B: emission likelihoods matrix
        initial_state_model          # PI: initial state model
    )

    test_list = ['aaa', 'baa', 'bba', 'bbb', 'bbb', 'bbb', 'bbb', 'bbb', 'bbb']
    test_emission = EmissionSequence(EMISSION_ALPHABET, test_list)
    print "State estimation on test_list before training:"
    print bsn_hmm_model.viterbi(test_emission)

    # retrain the probablilties of the model
    print "Re-training model..."
    bsn_hmm_model.baumWelch(
        EmissionSequence(EMISSION_ALPHABET, training_emissions)
    )
    # print bsn_hmm_model

    # when we are ready, we can try to use our model to predict the state
    # of the BSN wearer TODO: there may be a problem with the viterbi
    # print "State estimation on test_list after retraining:"
    # test_labels = bsn_hmm_model.viterbi(test_emission)
    # print test_labels
    # print determine_most_likely_state(test_labels[0])


def determine_most_likely_state(state_labels):
    label_counts = collections.defaultdict(lambda: 0)

    most_frequent_label = label_counts[0]
    high_frequency = 0
    for label in state_labels:
        if label_counts[label] > high_frequency:
            most_frequent_label = label
            high_frequency = label_counts[label]

    return most_frequent_label


def unpack_binary_data_into_list(file_name):
    data_points = []
    struct_size = struct.calcsize(DATA_FORMAT_STRING)

    for packed_struct in packed_structs_from_file(file_name, struct_size):
        if packed_struct is not None:
            data_tuple = struct.unpack(DATA_FORMAT_STRING, packed_struct)
            print "data: {}".format(data_tuple)
            data_points.append(BSNDataPoint(
                data_tuple[0],  # timestamp
                data_tuple[4],  # alpha frequency
                data_tuple[1],  # attention level
                data_tuple[3]   # torso position TODO: testing using arbitrary
            ))

    return data_points


def packed_structs_from_file(filename, struct_size):
    with open(filename, "rb") as data_file:
        while True:
            struct_data = data_file.read(struct_size)
            if struct_data:
                yield struct_data
            else:
                break
    yield None

if __name__ == "__main__":
    main()