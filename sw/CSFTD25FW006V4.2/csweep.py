from pickle import FALSE

import serial
import time
import math
from csftd import Csftd
import matplotlib.pyplot as plt
import numpy as np
import os
import csv

DWELL_TIME = 2   # ms
# Emi sweep parameters
FREQ_BEGIN = 200*10000  # 20 kHz
FREQ_END = 271*10000  # 500 kHz

FREQ_BEGIN = 20*10000  # 20 kHz
FREQ_END = 271*10000  # 500 kHz
STEPS = 1000  # points between begin and end freq's

DDS_GAIN = 255  # 0-255
TIA_GAIN = 1  # 0-255 0 is maximum gain, 255 is minimum gain



csdev = Csftd()

# Open connection
csdev.connect('COM4', 115200)

if csdev.is_connected():
    print('Device connected')

    # Read MCU UID
    print('Device UID: ' + csdev.get_uuid())

    # Read MCU internal voltage reference
    print('MCU VREF INT: ' + str(csdev.get_mcu_adc_channel_raw(0)) + ' RAW')

    # Read MCU internal temperature
    print('MCU TEMPERATURE: ' + str(csdev.get_mcu_adc_channel_raw(1)) + ' RAW')

    # Set DDS gain
    print('DDS gain: ' + csdev.set_dds_gain(DDS_GAIN))

    # Set TIA gain
    print('TIA gain: ' + csdev.set_tia_gain(TIA_GAIN))

    # Get ADS1115 CHANNEL_AIN0_GND
    print('ADS1115 AIN0_GND: ' + str(csdev.get_ext_adc_channel(4)) + ' RAW')

    # Get ADS1115 CHANNEL_AIN1_GND
    print('ADS1115 AIN1_GND: ' + str(csdev.get_ext_adc_channel(5)) + ' RAW')

    # Get ADS1115 CHANNEL_AIN2_GND
    print('ADS1115 AIN2_GND: ' + str(csdev.get_ext_adc_channel(6)) + ' RAW')

    # Get ADS1115 CHANNEL_AIN3_GND
    print('ADS1115 AIN3_GND: ' + str(csdev.get_ext_adc_channel(7)) + ' RAW')

    # Emi sweep parameters
    freqbegin = FREQ_BEGIN  # 20 kHz
    freqend = FREQ_END  # 500 kHz
    steps = STEPS  # points between begin and end freq's
    dwelltime = DWELL_TIME   # ms

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

    test = csdev.get_emi_mag_phase(freq, dwelltime, False)
    test = csdev.get_emi_mag_phase(freq, dwelltime, True)



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

    # # Plot data
    # plt.subplot(2, 1, 1)
    # plt.plot(x, mag)
    # plt.xlabel("Frequency [Hz]")
    # plt.ylabel("Magnitude")

    # plt.subplot(2, 1, 2)
    # plt.plot(x, phi)
    # plt.xlabel("Frequency [Hz]")
    # plt.ylabel("Phase [°]")
    # plt.show()

    
    # Output directory
    output_dir = r"C:\CorroSenseBoardV4\measurements\dwell test"
    os.makedirs(output_dir, exist_ok=True)

    # Create a descriptive filename
    base_filename = f"sweep_{FREQ_BEGIN/10000}_{FREQ_END/10000}_{stepsize}res_{DWELL_TIME}ms_DDS{DDS_GAIN}_TIA{TIA_GAIN}"

    # Plot and save figure
    plt.figure(figsize=(10, 6))
    plt.subplot(2, 1, 1)
    plt.plot(x, mag)
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Magnitude")

    plt.subplot(2, 1, 2)
    plt.plot(x, phi)
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Phase [°]")

    plot_path = os.path.join(output_dir, f"{base_filename}.png")
    plt.tight_layout()
    plt.savefig(plot_path)
    #plt.show()

    plt.close()  # Closes the current figure

    # Save data as CSV
    csv_path = os.path.join(output_dir, f"{base_filename}.csv")
    with open(csv_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Frequency [Hz]", "Magnitude", "Phase [°]"])
        for freq, m, p in zip(x, mag, phi):
            writer.writerow([freq, m, p])

    print(f"Saving plot to: {plot_path}")
    print(f"Saving CSV to: {csv_path}")


else:
    print('Connection error')

