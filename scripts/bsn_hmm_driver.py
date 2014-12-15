#!/usr/bin/python

__author__ = 't'

import collections

from ghmm import *

import pylab as pl

from bsn_data_point import BSN_EMISSION_ALPHABET, BSNDataPoint
import merge_sensor_data as msd


def main():
    # TODO: get a list of data points
    data_points = msd.unpack_binary_data_into_list("training.dat")

    print 'number of time stamps: ', len(data_points)
    print 'duration of experiment: ',\
        data_points[len(data_points) - 1].timestamp - data_points[0].timestamp

    sampled_data = [
        BSNDataPoint(
            timestamp=x[0],
            label=x[1],
            heart_rate=x[2],
            low_alpha_frequency=x[3],
            high_alpha_frequency=x[4],
            torso_position=x[5]
        ) for x in data_points
    ]

    training_emissions = \
        [point.to_discrete_emission_string() for point in data_points]
    training_labels = [point.label for point in data_points]

    print training_emissions
    print training_labels

    # aka sigma
    emission_aplphabet = BSN_EMISSION_ALPHABET

    # aka pi
    initial_state_model = [0.9,  # non-fatigue
                           0.1]  # fatigue
    # aka A
    state_transition_matrix = [[0.7, 0.3],    # non-fatigue
                               [0.1, 0.9]]    # fatigue

    non_fatigue_emission_probabilities = \
        [
            0.25,  # aaaa
            0.10,  # aaab
            0.10,  # aaba
            0.05,  # aabb
            0.10,  # abaa
            0.05,  # abab
            0.05,  # abba
            0.01,  # abbb
            0.10,  # baaa
            0.05,  # baab
            0.05,  # baba
            0.01,  # babb
            0.05,  # bbaa
            0.01,  # bbab
            0.01,  # bbba
            0.01   # bbbb
        ]

    fatigue_emission_probabilities = \
        [
            0.01,  # aaaa
            0.01,  # aaab
            0.01,  # aaba
            0.05,  # aabb
            0.01,  # abaa
            0.05,  # abab
            0.05,  # abba
            0.10,  # abbb
            0.01,  # baaa
            0.05,  # baab
            0.05,  # baba
            0.10,  # babb
            0.05,  # bbaa
            0.10,  # bbab
            0.10,  # bbba
            0.25   # bbbb
        ]

    if not probabilities_sum_to_one(non_fatigue_emission_probabilities):
        raise Exception('FIX THE NON-FATIGUE PROBS!!!!')
    if not probabilities_sum_to_one(fatigue_emission_probabilities):
        raise Exception('FIX THE FATIGUE PROBS!!!!')

    # aka B
    emission_likelihood_matrix = [non_fatigue_emission_probabilities,
                                  fatigue_emission_probabilities]

    # simply initialize the model
    bsn_hmm_model = HMMFromMatrices(
        emission_aplphabet,         # sigma: the alphabet
        DiscreteDistribution(       # the DiscreteDistribution is for ghmm's
            emission_aplphabet      # internals
        ),
        state_transition_matrix,     # A: state transitions model matrix
        emission_likelihood_matrix,  # B: emission likelihoods matrix
        initial_state_model          # PI: initial state model
    )

    test_list = ['aaa', 'baa', 'bba', 'bbb', 'bbb', 'bbb', 'bbb', 'bbb', 'bbb']
    test_emission = EmissionSequence(BSN_EMISSION_ALPHABET, test_list)
    print "State estimation on test_list before training:"
    print bsn_hmm_model.viterbi(test_emission)

    # retrain the probablilties of the model
    print "Re-training model..."
    bsn_hmm_model.baumWelch(
        EmissionSequence(BSN_EMISSION_ALPHABET, training_emissions)
    )
    # print bsn_hmm_model

    # when we are ready, we can try to use our model to predict the state
    # of the BSN wearer
    # print "State estimation on test_list after retraining:
    sample_emissions = EmissionSequence(
        BSN_EMISSION_ALPHABET,
        [x.to_discrete_emission_string() for x in sampled_data]
    )
    predicted_labels = bsn_hmm_model.viterbi(sample_emissions)
    print determine_percent_correct(
        [x.label for x in sampled_data],
        predicted_labels
    )
    # print test_labels

    pl.plot(range(len([1])), [1], label='Actual')
    pl.plot(range(len([1])), [1], label='Predicted')
    pl.xlabel("Time Step")
    pl.ylabel("BSN Wearer State (Non-Fatigued or Fatigued)")
    pl.title("BSN Fatigue State Prediction")
    legend = pl.legend(loc='best', ncol=2, shadow=None)
    legend.get_frame().set_facecolor('#00FFCC')
    pl.show()


def probabilities_sum_to_one(probability_vector):
    return sum(probability_vector) == 1.0


def determine_percent_correct(input_list, output_list):
    num_correct = 0
    for i in range(0, len(input_list)):
        if input_list[i] == output_list[i]:
            num_correct += 1

    return float(num_correct) / float(len(input_list))


def determine_most_likely_state(state_labels):
    label_counts = collections.defaultdict(lambda: 0)

    most_frequent_label = label_counts[0]
    high_frequency = 0
    for label in state_labels:
        if label_counts[label] > high_frequency:
            most_frequent_label = label
            high_frequency = label_counts[label]

    return most_frequent_label

if __name__ == "__main__":
    main()
