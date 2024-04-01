from ECE16Lib.Communication import Communication
from ECE16Lib.CircularList import CircularList
from ECE16Lib.ToothBrushHelper import ToothBrushHelper
from matplotlib import pyplot as plt
import ECE16Lib.DSP as filt
import scipy.signal as sig
from time import time
from time import sleep
import numpy as np
import socket

# Setup the Socket connection to the Space Invaders game
host = "127.0.0.1"
port = 65432
mySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
mySocket.connect((host, port))
mySocket.setblocking(False)

if __name__ == "__main__":
  motion = "CM"
  fs = 50
  num_samples = 800               # 10 seconds of data @ 50Hz
  # Process data every 3 seconds
  process_time = 3
  # Each motion of brushing continues for 30 seconds
  brush_time_CM = 40
  brush_time_BM = 20
  
  TBH = ToothBrushHelper(800, fs, thresh_low_BM = 10, thresh_high_BM = 25, thresh_low_CM = 20, thresh_high_CM = 45)
  
  times = CircularList([], num_samples)
  ax = CircularList([], num_samples)
  ay = CircularList([], num_samples)
  az = CircularList([], num_samples)
  
  m1 = 0
  m2 = 0
  m3 = 0
  m4 = 0

  L1 = CircularList([], num_samples)
  
  # set up comms
  comms = Communication("COM8", 115200)
  comms.clear()                   # just in case any junk is in the pipes
  comms.send_message("wearable")  # begin sending data

  try:
    # Initialize timing variables
    previous_time_start = time()
    previous_time_DP = time()
    previous_time_Motion = time()
    
    while(True):
      message = comms.receive_message()
      
      if (message != None and '\r\n' in message):
          message = message.strip()
      
      if(message != None):
        try:
          (m1, m2, m3, m4) = message.split(',')
          
        except ValueError:        # if corrupted data, skip the sample
          pass
        
        #print(m1,m2,m3,m4)
        
        TBH.add(int(m1)/1000, int(m2), int(m3), int(m4))
        
        current_time_DP = time()
        current_time_Motion = time()
        
        if (motion == "CM" and current_time_Motion - previous_time_Motion > brush_time_CM):
          previous_time_Motion = current_time_Motion
          mySocket.send("next".encode("UTF-8"))
    
          motion = "BM"
        
        if (motion == "BM" and current_time_Motion - previous_time_Motion > brush_time_BM):
          previous_time_Motion = current_time_Motion
          mySocket.send("next".encode("UTF-8"))
          
          motion = "CM"
              
        if (time() - previous_time_start > 120):
            print("WELL DONE!")
            mySocket.send("next".encode("UTF-8"))
            break
        
        if (current_time_DP - previous_time_DP > process_time):
          previous_time_DP = current_time_DP
          
          if motion == "CM":
            mr, count, peaks, filtered = TBH.process_CM()
            freq = count/8*60
            
          elif motion == "BM":
            mr, count, peaks, filtered = TBH.process_BM()
            # freq = count/8*60
            
          print("Estimated movement rate: {:.2f} mpm".format(mr))
          #print(freq)
          
          if mr < 50:
              print("Too Slow, Check posture")
              comms.send_message("0")
          elif mr > 130:
              print("Too Fast")
              comms.send_message("1")
          else:
              print("Good Job")
              comms.send_message("2")    
          
        
  except(Exception, KeyboardInterrupt) as e:
    print(e)                     # Exiting the program due to exception
  finally:
    print("Closing connection.")
    comms.send_message("sleep")  # stop sending data
    comms.close()


