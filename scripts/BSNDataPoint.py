from ghmm import Alphabet, LabelDomain

__author__ = 't'

""" Defines a class that retains only essential data for HMM emissions.

    This class is used to contain the raw data only, but can generate the
    string used as an emission label (member of an 'alphabet') for GHMM since
    GHMM backs us into the corner of using strings to represent vectors.
"""

# Fatigue state labels
FATIGUE_LABEL = 'fatigue'
NON_FATIGUE_LABEL = 'non-fatigue'
STATE_ALPHABET = LabelDomain([NON_FATIGUE_LABEL, FATIGUE_LABEL])

# Emission labels
EMISSION_ALPHABET =  Alphabet(['aaa', 'aab', 'aba', 'abb',
                      'baa', 'bab', 'bba', 'bbb',])

# Discretization thresholds
ALPHA_FATIQUE_FREQUENCY = 100     #TODO
ATTENTION_FATIGUE_LEVEL = 50      #TODO
TORSO_FATIGUE_ANGLE = 30          #TODO

class BSNDataPoint(object):
    def __init__(self, alpha_frequency, attention_level, torso_position,
                 label = None):
        self.alpha = alpha_frequency
        self.attention = attention_level
        self.torso = torso_position
        self.label = label

    def get_alpha_category(self):
        if self.alpha <= ALPHA_FATIQUE_FREQUENCY:
            return "a"
        else:
            return "b"

    def get_attention_category(self):
        if self.attention <= ATTENTION_FATIGUE_LEVEL:
            return "a"
        else:
            return "b"

    def get_torso_category(self):
        if self.torso <= TORSO_FATIGUE_ANGLE:
            return "a"
        else:
            return "b"

    def to_discrete_emission_string(self):
        return "{}{}{}".format(
            self.get_alpha_category(),
            self.get_attention_category(),
            self.get_torso_category()
        )

    def __str__(self):
        return (
            'Alpha Frequency: {} -> {}'
            'Attention Level: {} -> {}'
            'Torso Position:  {} -> {}'
            'Emitted From:    {}'
        ).format(
            self.alpha, self.get_alpha_category(),
            self.attention, self.get_attention_category(),
            self.torso, self.get_torso_category(),
            self.label
        )