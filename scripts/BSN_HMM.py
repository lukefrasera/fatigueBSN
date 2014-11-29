#!/usr/bin/python
import collections

from ghmm import *
from fatigueBSN_model import *
from fatigueBSN_model.BSNDataPoint import *

__author__ = 't'

def main():
    # TODO: get a list of data points
    data_points = []

    training_emissions = \
        [point.to_discrete_emission_string() for point in data_points]
    training_labels = [point.label for point in data_points]

    # aka sigma
    emission_aplphabet = EMISSION_ALPHABET


    # aka pi
    initial_state_model = [0.99, # non-fatigue
                           0.01] # fatigue
    # aka A
    state_transition_model = [[0.9, 0.1],    # non-fatigue
                              [0.99, 0.01]]  # fatigue

    non_fatigue_emission_probabilities = [
        0.3, # 'aaa'
        0.1, # 'aab'
        0.1, # 'aba'
        0.1, # 'abb'
        0.1, # 'baa'
        0.1, # 'bab'
        0.1, # 'bba'
        0.1  # 'bbb'
    ]
    fatigue_emission_probabilities = [
        0.1, # 'aaa'
        0.1, # 'aab'
        0.1, # 'aba'
        0.1, # 'abb'
        0.1, # 'baa'
        0.1, # 'bab'
        0.1, # 'bba'
        0.3  # 'bbb'
    ]

    #aka B
    emission_likelihood_matrix = [non_fatigue_emission_probabilities,
                                  fatigue_emission_probabilities]

    # simply initialize the model
    bsn_hmm_model = HMMFromMatrices(
        emission_aplphabet,         # sigma: the alphabet
        DiscreteDistribution(       #
            emission_aplphabet
        ),
        state_transition_model,     # A: state transitions model matrix
        emission_likelihood_matrix, # B: emission likelihoods matrix
        initial_state_model         # PI: initial state model
    )

    # retrain the probablilties of the model
    bsn_hmm_model.baumWelch(
        emission_aplphabet,
        training_emissions,
        STATE_ALPHABET,
        training_labels
    )

    # when we are ready, we can try to use our model to predict the state
    # of the BSN wearer TODO
    test_emissions = []
    test_labels = bsn_hmm_model.viterbi(test_emissions)
    print determine_most_likely_state(STATE_ALPHABET, test_labels)


def determine_most_likely_state(state_alphabet, state_labels):
    label_counts = collections.defaultdict(lambda: 0)
    for label in state_alphabet:
        label_counts[label] += 1

    most_frequent_label = state_alphabet[0]
    frequency = 0
    for label in label_counts:
        if label_counts[label] > frequency:
            most_frequent_label = label
            frequency = label_counts[label]

    return label

if __name__ == "__main__":
    main()