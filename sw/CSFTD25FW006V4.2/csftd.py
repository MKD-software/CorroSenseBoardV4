from pickle import FALSE
from enum import Enum
import serial
import time

class SysStatusStates(Enum):
    ERROR = 0
    OK = 1
    BUSY = 2
    TIMEOUT = 3
    INVALID = 4
    BUS_BUSY = 5

class Csftd:

    def __init__(self):
        self.serialPort = serial.Serial()
        self.serialPort.timeout = 0
        self.serialPort.baudrate = 115200
        self.serialPort.port=''

    def connect(self, _port, _baudrate):
        if not self.is_connected():
            self.serialPort.port = _port
            self.serialPort.baudrate = _baudrate
            self.serialPort.open()

    def disconnect(self):
        if self.is_connected():
            self.serialPort.close()

    def is_connected(self):
        return self.serialPort.is_open

    def send_request_no_payload(self, cmdid):

        if self.is_connected():
            datagram = bytearray([35])
            datagram.append(0)
            datagram.append(cmdid)
            datagram.append(36)
            self.serialPort.write(datagram)
            time.sleep(1)  # Sleep for x seconds
            return True
        return False

    def send_request(self, cmdid, payload):

        if self.is_connected():
            datagram = bytearray([35])
            datagram.append(len(payload))
            datagram.append(cmdid)
            datagram += payload
            #datagram.append(payload)
            datagram.append(36)
            self.serialPort.write(datagram)
            time.sleep(0.05)  # Sleep for x seconds
            return True
        return False

    def read_response(self, length):

        if self.is_connected():
            s = bytearray(self.serialPort.read(length+4))
            if len(s) != 0:
                if s[0] == 35:
                    if s[1] == length:
                        if s[(3+length)] == 36:
                            return s[3:3+length]

                    return False

    def get_uuid(self):

        if self.is_connected():
            # Read MCU UID
            self.send_request_no_payload(1)
            uid = self.read_response(12)
            return ''.join(format(byte, '02x') for byte in uid)
        return False

    def get_mcu_adc_channel_raw(self, channel):

        if self.is_connected():
            # Prepare payload
            s = channel.to_bytes(1, "big")
            payload = bytearray(s)
            # Send request and receive answer
            self.send_request(6, payload)
            response = self.read_response(3)  # 1 byte payload
            # Parse response
            if response[0] == SysStatusStates.OK.value:
                return int.from_bytes([response[1], response[2]], "big")
            return SysStatusStates(response[0]).name  # 1 byte payload
        return False


    def get_ext_adc_channel(self, channel):

        if self.is_connected():
            # Prepare payload
            s = channel.to_bytes(1, "big")
            payload = bytearray(s)
            # Send request and receive answer
            self.send_request(18, payload)
            response = self.read_response(3)  # 1 byte payload
            # Parse response
            if response[0] == SysStatusStates.OK.value:
                return int.from_bytes([response[1], response[2]], "big")
            return SysStatusStates(response[0]).name  # 1 byte payload
        return False

    def set_dds_gain(self, value):

        if self.is_connected():
            # Prepare payload
            s = value.to_bytes(1, "big")
            payload = bytearray(s)
            # Send request and receive answer
            self.send_request(15, payload)
            response = self.read_response(1)
            return SysStatusStates(response[0]).name  # 1 byte payload
        return False

    def set_tia_gain(self, value):

        if self.is_connected():
            # Prepare payload
            s = value.to_bytes(1, "big")
            payload = bytearray(s)
            # Send request and receive answer
            self.send_request(16, payload)
            response = self.read_response(1)
            return SysStatusStates(response[0]).name  # 1 byte payload
        return False

    def get_emi_mag_phase(self, frequency, dwelltime, sustain):

        if self.is_connected():
            # "Constants" - Do not change.
            sustaintrue = 90  # 90=TRUE, 165=FALSE
            sustainfalse = 165

            # Prepare payload
            s = frequency.to_bytes(4, "big")
            s += dwelltime.to_bytes(2, "big")
            # Disable DDS after last measurement
            if sustain:
                s += sustaintrue.to_bytes(1, "big")
            else:
                s += sustainfalse.to_bytes(1, "big")

            payload = bytearray(s)

            # Send request and receive answer
            self.send_request(30, payload)

            # Device response time depends on dwelltime
            if dwelltime != 0:
                time.sleep(0.5+dwelltime/1000)  # Sleep for x seconds

            response = self.read_response(5)  # 7 byte payload

            # Parse response
            if len(response) == 5 and response[0] == SysStatusStates.OK.value:
                # Translate response payload
                magnitude = int.from_bytes([response[1], response[2]], "big")
                phase = int.from_bytes([response[3], response[4]], "big")
                return [magnitude, phase]
            return SysStatusStates(response[0]).name
        return False

    def get_hum_temp(self):

        if self.is_connected():
            # Send request and receive answer
            self.send_request_no_payload(19)
            response = self.read_response(5)  # 1 byte payload
            # Parse response
            if response[0] == SysStatusStates.OK.value:
                ambienttemp = int.from_bytes([response[1], response[2]], "big")
                relhumidity = int.from_bytes([response[3], response[4]], "big")
                return [ambienttemp, relhumidity]
            return SysStatusStates(response[0]).name  # 1 byte payload
        return False
