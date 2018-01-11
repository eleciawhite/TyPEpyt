import time
import math
from threading import Timer

# Import the ADS1x15 module.
import Adafruit_ADS1x15

# wiring to ADC channels:
TYADC_CLAW = 0
TYADC_ELBOW = 1
TYADC_SHOULDER = 2
TYADC_BASE = 3

class TyAdc():
  def __init__(self, i2c_busnum=1, gain=1, data_rate=860, channels=4, read_time = 0.1):
    # Create an ADS1115 ADC (16-bit) instance.
    self.adc = Adafruit_ADS1x15.ADS1115(busnum=i2c_busnum)
    self.GAIN = gain
    self.DATA_RATE = data_rate
    self.ADC_CHANNELS = channels
    self.READ_TIME = read_time

    self.running = True

    # ADC readings
    self.idx = -1
    self.val = [0]*channels
    self.timer = Timer(self.READ_TIME, self.update,())
    self.timer.start()

  
  def stop(self):
    self.running = False

  def start(self):
    self.running = True
    self.idx == -1
    self.update()

  # Timer function is called frequently to sample the adc data one channel at a time
  def update(self):
    if (self.idx == -1):
      self.idx = 0 # first pass
    else:
     self.val[self.idx] =  self.adc.get_last_result()
     self.idx += 1
     if (self.idx >= self.ADC_CHANNELS): self.idx = 0
    if self.running == True:
      self.adc.start_adc(self.idx, gain=self.GAIN, data_rate=self.DATA_RATE)
      self.timer = Timer(self.READ_TIME, self.update,())
      self.timer.start()

  def output(self):
    print time.time(), self.val

  def outputloop(self):
    while True:
      self.output()
      time.sleep(self.READ_TIME * self.ADC_CHANNELS)

  def is_claw_ok(self):
    return self.val[TYADC_CLAW] < 100
  def is_elbow_ok(self):
    return self.val[TYADC_ELBOW] < 100
  def is_shoulder_ok(self):
    return self.val[TYADC_SHOULDER] < 100
  def is_base_ok(self):
    return self.val[TYADC_BASE] < 100

  def magnitude(self):
    total = 0.0
    for v in self.val:
        total += v*v
    return math.sqrt(total)
    



