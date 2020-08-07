# GrovePi Project for a Weather Station project.

#   *   Sensor Connections on the GrovePi:
#           -> Grove light sensor                       - Port A2
#           -> Grove Temperature and Humidity sensor    - Port D4

#################################################################
import time
import grovepi
import subprocess
import math
from ISStreamer.Streamer import Streamer
from grove_i2c_barometic_sensor_BMP180 import BMP085

#################################################################

#InitialState Streamer Key - KAD
streamer = Streamer(bucket_name="Shed Weather Test", bucket_key="Python", access_key="ist_1qMvI4et1jay3o3ZooCcqhOlUG1YAWy_DLT")


###################################################################
light_sensor            = 2     #Light Sensor Port Number
temp_humidity_sensor    = 4     #Temperature sensor Port Number

# Temp humidity sensor type.  You can use the blue or the white version.
# Note the GrovePi Starter Kit comes with the blue sensor
blue=0
white=1
therm_version = blue            # If you change the thermometer, this is where you redefine.

#################################################################
# Timings

time_to_sleep       = 60        # The main loop runs every 60 seconds. Change to 1 for testing

#Read the data from the sensors.
def read_sensor():
    try:
        light=grovepi.analogRead(light_sensor)
        [temp,humidity] = grovepi.dht(temp_humidity_sensor,therm_version)   # Here we're using the thermometer version.
        #Return -1 in case of bad temp/humidity sensor reading
        if math.isnan(temp) or math.isnan(humidity):        #temp/humidity sensor sometimes gives nan
            return [-1,-1,-1,-1]
            #return [-1,-1,-1]
        return [light,temp,humidity]
        #return [light,temp,humidity]
    
    #Return -1 in case of sensor error
    except (IOError,TypeError) as e:
            # return [-1,-1,-1]
            return [-1,-1,-1,-1]

# Main Loop
while True:
    curr_time_sec=int(time.time())
    
    [light,temp,humidity]=read_sensor()
    # If any reading is a bad reading, skip the loop and try again
    if light==-1:
        print("Bad reading")
        time.sleep(1)
        continue
    
    print(("Light: %d\nTemp: %.2fC\nHumidity:%.2f%%\n" %(light,temp,humidity)))
    #Log to InitialState Dashboard
    streamer.log("Humidity(%)", humidity)
    streamer.log("Termperature(C)", temp)
    streamer.log("Light", light)
    streamer.flush()
    
    #Slow down the loop
    time.sleep(time_to_sleep)

