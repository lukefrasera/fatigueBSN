#!/usr/bin/env python

import time, struct,sys, random
import termios, fcntl, sys, os
from include.typodistance import euclideanKeyboardDistance
from math import sqrt, pow


qwertyKeyboardArrayMissing = [
    ['1','2','3','4','5','6','7','8','9','0'],
    ['q','w','e','r','t','y','u','i','o','p','[',']'],
    ['a','s','d','f','g','h','j','k','l'],
    ['z','x','c','v','b','n','m']
    ]

def read_single_keypress():
  """Waits for a single keypress on stdin.

  This is a silly function to call if you need to do it a lot because it has
  to store stdin's current setup, setup stdin for reading single keystrokes
  then read the single keystroke then revert stdin back after reading the
  keystroke.

  Returns the character of the key that was pressed (zero on
  KeyboardInterrupt which can happen when a signal gets handled)

  """
  fd = sys.stdin.fileno()
  # save old state
  flags_save = fcntl.fcntl(fd, fcntl.F_GETFL)
  attrs_save = termios.tcgetattr(fd)
  # make raw - the way to do this comes from the termios(3) man page.
  attrs = list(attrs_save) # copy the stored version to update
  # iflag
  attrs[0] &= ~(termios.IGNBRK | termios.BRKINT | termios.PARMRK 
                | termios.ISTRIP | termios.INLCR | termios. IGNCR 
                | termios.ICRNL | termios.IXON )
  # oflag
  attrs[1] &= ~termios.OPOST
  # cflag
  attrs[2] &= ~(termios.CSIZE | termios. PARENB)
  attrs[2] |= termios.CS8
  # lflag
  attrs[3] &= ~(termios.ECHONL | termios.ECHO | termios.ICANON
                | termios.ISIG | termios.IEXTEN)
  termios.tcsetattr(fd, termios.TCSANOW, attrs)
  # turn off non-blocking
  fcntl.fcntl(fd, fcntl.F_SETFL, flags_save & ~os.O_NONBLOCK)
  # read a single keystroke
  try:
      ret = sys.stdin.read(1) # returns a single character
  except KeyboardInterrupt: 
      ret = 0
  finally:
      # restore old state
      termios.tcsetattr(fd, termios.TCSAFLUSH, attrs_save)
      fcntl.fcntl(fd, fcntl.F_SETFL, flags_save)
  return ret

def main():
  random.seed()
  data = []
  try:
    while True:
      print "Ready?"
      reflexTimeList = []
      accuracyList = []
      for i in xrange(5):
        # choose Random Key
        row = random.randrange(0,len(qwertyKeyboardArrayMissing))
        col = random.randrange(0,len(qwertyKeyboardArrayMissing[row]))
        randKey = qwertyKeyboardArrayMissing[row][col]
        #choose Random Delay
        time.sleep(random.uniform(.5,2))
        print "Press: {0}".format(randKey)
        x = time.time()
        s = read_single_keypress()
        y = time.time()
        z = euclideanKeyboardDistance(s, randKey)

        reflexTimeList.append(y-x)
        accuracyList.append(z)

      # computer mean
      meanReflex = sum(reflexTimeList)/len(reflexTimeList)
      meanAccuracy = sum(accuracyList)/len(accuracyList)

      varReflex = sum([pow(i - meanReflex,2) for i in reflexTimeList])
      varAccuracy = sum([pow(i - meanAccuracy,2) for i in accuracyList])
      print (meanReflex, varReflex)
      print (meanAccuracy, varAccuracy)
      data.append([time.time(), meanReflex, varReflex, meanAccuracy, varAccuracy])
      print ("Press Space To run again or another key to stop and store:")
      if read_single_keypress() != ' ':
        raise KeyboardInterrupt
  except KeyboardInterrupt:
    pass

  file_ = open(sys.argv[1], 'wb')

  for line in data:
    s = struct.pack('ddddd', *line)
    file_.write(s)
  file_.close()


if __name__ == '__main__':
  main()