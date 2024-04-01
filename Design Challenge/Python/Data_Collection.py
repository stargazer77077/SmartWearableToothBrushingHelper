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


# Collect num_samples from the MCU
def collect_samples():

  num_samples = 800 # 10 seconds of data @ 50Hz
  times = CircularList([], num_samples)
  ax = CircularList([], num_samples)
  ay = CircularList([], num_samples)
  az = CircularList([], num_samples)
  data = None

  comms = Communication("COM8", 115200)
  try:
    comms.clear() # just in case any junk is in the pipes
    # wait for user to start walking before starting to collect data
    input("Ready to collect data? Press [ENTER] to begin.\n")
    sleep(3)
    comms.send_message("wearable") # begin sending data

    sample = 0
    while(sample < num_samples):
      message = comms.receive_message()
      if(message != None):
        try:
          (m1, m2, m3, m4) = message.split(',')
        except ValueError: # if corrupted data, skip the sample
          continue

        # add the new values to the circular lists
        times.add(int(m1))
        ax.add(int(m2))
        ay.add(int(m3))
        az.add(int(m4))
        sample += 1
        print("Collected {:d} samples".format(sample))

    # a single ndarray for all samples for easy file I/O
    data = np.column_stack([times, ax, ay, az])

  except(Exception, KeyboardInterrupt) as e:
    print(e) # exiting the program due to exception
    print("USER EXITED PROGRAM WITH CLTR+C INPUT")
  finally:
    comms.send_message("sleep") # stop sending data
    comms.close()

  return data


if __name__ == "__main__":


  # Make sure not to overwrite a file after saving!
  filename = "./data/TEST.csv"

  # Get data from the MCU and save to file
  data = collect_samples()
  save_data(filename, data)

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
  
  # Low-pass Filter Design
  bl, al = sig.butter(3, 1, btype="lowpass", fs=50)

  # Low-pass Filter the Signal
  l1 = sig.lfilter(bl, al, l1)
  
  # Count the peaks
  thresh_low = 10
  thresh_high = 20
  # CM
  #thresh_low = 25
  #thresh_high = 45
  count, peaks = filt.count_peaks(l1, thresh_low, thresh_high)
  
  # Compute the rate of toothbursh moving
  #avg_movement_time = np.mean(np.diff(t[peaks]))
  #freq = 60/avg_movement_time
  freq = count/8*60
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