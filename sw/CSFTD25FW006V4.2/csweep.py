from pickle import FALSE

import serial
import time
import math
from csftd import Csftd
import matplotlib.pyplot as plt
import numpy as np

csdev = Csftd()

# Open connection
csdev.connect('COM13', 115200)

if csdev.is_connected():
    print('Device connected')

    # Read MCU UID
    print('Device UID: ' + csdev.get_uuid())

    # Read MCU internal voltage reference
    print('MCU VREF INT: ' + str(csdev.get_mcu_adc_channel_raw(0)) + ' RAW')

    # Read MCU internal temperature
    print('MCU TEMPERATURE: ' + str(csdev.get_mcu_adc_channel_raw(1)) + ' RAW')

    # Set DDS gain
    print('DDS gain: ' + csdev.set_dds_gain(255))

    # Set TIA gain
    print('TIA gain: ' + csdev.set_tia_gain(255))

    # Get ADS1115 CHANNEL_AIN0_GND
    print('ADS1115 AIN0_GND: ' + str(csdev.get_ext_adc_channel(4)) + ' RAW')

    # Get ADS1115 CHANNEL_AIN1_GND
    print('ADS1115 AIN1_GND: ' + str(csdev.get_ext_adc_channel(5)) + ' RAW')

    # Get ADS1115 CHANNEL_AIN2_GND
    print('ADS1115 AIN2_GND: ' + str(csdev.get_ext_adc_channel(6)) + ' RAW')

    # Get ADS1115 CHANNEL_AIN3_GND
    print('ADS1115 AIN3_GND: ' + str(csdev.get_ext_adc_channel(7)) + ' RAW')

    # Emi sweep parameters
    freqbegin = 200000  # 20 kHz
    freqend = 5000000  # 500 kHz
    steps = 20  # points between begin and end freq's
    dwelltime = 20  # ms

    # Calc step size
    stepsize = int(round((freqend - freqbegin) / (steps - 1), 0))
    freq = freqbegin  # First sweep frequency

    # Arrays for sweep data
    x = []
    #vout = []
    mag = []
    phi = []

    # Begin sweep
    print('\n------Sweep start------\n')

    htresult = csdev.get_hum_temp()
    print('HIH6121 Temperature: '+ str(htresult[0]/100) + ' °C  Humidity: ' + str(htresult[1]/100) + ' RH\n')

    #print('Index ; Frequency [Hz] ; Vo ; Magnitude ; Phase [°]')
    print('Index ; Frequency [Hz] ; Magnitude ; Phase [°]')

    # Loop through frequencies
    for i in range(steps):

        if i == (steps - 1):
            result = csdev.get_emi_mag_phase(freq, dwelltime, False)
        else:
            result = csdev.get_emi_mag_phase(freq, dwelltime, True)

        # Convert measurements to application units
        #phi_degrees = math.degrees(2 * math.pi * (phase / vdd))
        # Mag = (Rf*Vin)./TIA_VOUT;
        #mag_ = (1000 * vo) / amp
        if result[0] != 0:
            #mag_ = (1000 * 1) / result[0]
            mag_ = result[0]
        else:
            mag_ = 0

        if result[1] != 0:
            #phi_degrees = math.degrees(2 * math.pi * (result[1] / 2.8))
            phi_degrees = result[1]
        else:
            phi_degrees = 0

        # Store data to arrays for plotting
        x.append(int(freq / 10))
        #vout.append(vo)
        mag.append(mag_)
        phi.append(phi_degrees)

        # Output data to console
        """print(str(i) + ' ; ' + str(freq / 10) + ' ; ' + str(round(vo, 3)) + ' ; ' + str(round(mag_, 3)) + ' ; ' + str(
            round(phi_degrees, 2)))"""

        print(str(i) + ' ; ' + str(freq / 10) + ' ; ' + str(round(mag_, 3)) + ' ; ' + str(
            round(phi_degrees, 2)))

        # Increment frequency
        freq += stepsize
    else:
        print("\n------Sweep done------\n")

    # Close connection
    csdev.disconnect()
    print('Device disconnected')

    # Plot data
    plt.subplot(2, 1, 1)
    plt.plot(x, mag)
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Magnitude")

    plt.subplot(2, 1, 2)
    plt.plot(x, phi)
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Phase [°]")
    plt.show()

else:
    print('Connection error')

