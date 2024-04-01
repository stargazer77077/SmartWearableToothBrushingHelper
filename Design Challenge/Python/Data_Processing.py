# Imports
from ECE16Lib.Communication import Communication
from ECE16Lib.CircularList import CircularList
import ECE16Lib.DSP as filt
import scipy.signal as sig
from matplotlib import pyplot as plt
from time import sleep
import numpy as np

# Save data to file
def save_data(filename, data):
  np.savetxt(filename, data, delimiter=",")

# Load data from file
def load_data(filename):
  return np.genfromtxt(filename, delimiter=",")

# Compute the L1 norm for vectors ax, ay, az (L1=|ax|+|ay|+|az|)
def l1_norm(ax, ay, az):
  return abs(ax) + abs(ay) + abs(az)


if __name__ == "__main__":

  # Make sure not to overwrite a file after saving!
  filename = "./data/CM1.csv"
  # Load the data from file
  data = load_data(filename)


  # Data is 500x4 containing the time, ax, ay, az samples
  t = data[:,0]
  t = (t - t[0])/1e3 # make time range from 0-10 in seconds
  ax = data[:,1]
  ay = data[:,2]
  az = data[:,3]

  # Compute the Sample L1 Norm 
  l1 = l1_norm(ax, ay, az)
  l1 = filt.detrend(l1, 25)
  l1 = filt.moving_average(l1, 5)
  # Normalize the signal
  # l1 = filt.normalize(l1)
  
  # Low-pass Filter Design
  bl, al = sig.butter(3, 1, btype="lowpass", fs=50)

  # Low-pass Filter the Signal
  l1 = sig.lfilter(bl, al, l1)
  
  # Count the peaks
  #thresh_low = 10
  #thresh_high = 25
  thresh_low = 25
  thresh_high = 50
  count, peaks = filt.count_peaks(l1, thresh_low, thresh_high)
  
  print(count)
  
  # Compute the rate of toothbursh moving
  avg_movement_time = np.mean(np.diff(t[peaks]))
  freq = 60/avg_movement_time
  print("Estimated movement rate: {:.2f} mpm".format(freq))
  

  
  # Plot the data
  plt.figure()
  plt.plot(t, l1)
  plt.title("L1-Norm of Acceleration")
  plt.xlabel("seconds")
  plt.ylabel("|ax|+|ay|+|az|")
  
  plt.plot(t[peaks], l1[peaks], 'rx')
  plt.plot(t, [thresh_low]*len(l1), "b--")
  plt.show()
  
  
  
  '''
  
  # Plot the data
  plt.figure()
  ax = filt.detrend(ax, 25)
  plt.plot(t, ax)
  plt.title("ax Acceleration")
  plt.xlabel("seconds")
  plt.ylabel("ax")
  plt.show()
  
  # Plot the data
  plt.figure()
  ay = filt.detrend(ay, 25)
  plt.plot(t, ay)
  plt.title("ay Acceleration")
  plt.xlabel("seconds")
  plt.ylabel("ay")
  plt.show()
  
  # Plot the data
  plt.figure()
  az = filt.detrend(az, 25)
  plt.plot(t, az)
  plt.title("az Acceleration")
  plt.xlabel("seconds")
  plt.ylabel("az")
  plt.show()
  '''