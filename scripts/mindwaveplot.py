#!/usr/bin/env python

import time
import bluetooth
from mindwavemobile.MindwaveDataPoints import AttentionDataPoint, EEGPowersDataPoint
from mindwavemobile.MindwaveDataPointReader import MindwaveDataPointReader

import numpy as np
import pylab as pl

def main():
  mdpr = MindwaveDataPointReader()
  mdpr.start()
  eeg_datapoints = []
  attention_datapoints = []

  try:
    while(True):
      data = mdpr.readNextDataPoint()
      if (data.__class__ is AttentionDataPoint):
        attention_datapoints.append(data)
      if (data.__class__ is EEGPowersDataPoint):
        eeg_datapoints.append(data)
  except KeyboardInterrupt:
    pass

  # plot data
  print len(eeg_datapoints)
  print len(attention_datapoints)

  attention_datapoint_vals = [point.attentionValue for point in attention_datapoints]

  delta_points = []
  theta_points = []
  lowAlpha_points = []
  highAlpha_points = []
  lowBeta_points = []
  highBeta_points = []
  lowGamma_points = []
  midGamma_points = []

  for datapoint in eeg_datapoints:
    # print(datapoint)
    delta_points.append(datapoint.delta)
    theta_points.append(datapoint.theta)
    lowAlpha_points.append(datapoint.lowAlpha)
    highAlpha_points.append(datapoint.highAlpha)
    lowBeta_points.append(datapoint.lowBeta)
    highBeta_points.append(datapoint.highBeta)
    lowGamma_points.append(datapoint.lowGamma)
    midGamma_points.append(datapoint.midGamma)


  # two plots will make the data look more presentable since the scales
  # of the data vary widely (maybe even more, like a plot per greek letter
  # or something)

  # plot the EEG components (scale: 0 - large)
  pl.plot(range(len(eeg_datapoints)), delta_points, label="Delta")
  pl.plot(range(len(eeg_datapoints)), theta_points, label="Theta")
  pl.plot(range(len(eeg_datapoints)), lowAlpha_points, label="Low-Alpha")
  pl.plot(range(len(eeg_datapoints)), highAlpha_points, label="High-Alpha")
  pl.plot(range(len(eeg_datapoints)), lowBeta_points, label="Low-Beta")
  pl.plot(range(len(eeg_datapoints)), highBeta_points, label="High-Beta")
  pl.plot(range(len(eeg_datapoints)), lowGamma_points, label="Low-Gamma")
  pl.plot(range(len(eeg_datapoints)), midGamma_points, label="Mid-Gamma")

  pl.xlabel("Time Step")
  pl.ylabel("Reading Value")

  legend = pl.legend(loc='best', ncol=2, shadow=None)
  legend.get_frame().set_facecolor('#00FFCC')

  # pl.yscale('log')

  pl.show()


  # plot the attention reading (scale: 1- 1001)
  pl.plot(range(len(attention_datapoints)), attention_datapoint_vals, label="Attention")
  pl.xlabel("Time Step")
  pl.ylabel("Reading Value")

  legend = pl.legend(loc='best', ncol=2, shadow=None)
  legend.get_frame().set_facecolor('#00FFCC')
  pl.show()




if __name__ == '__main__':
  main()