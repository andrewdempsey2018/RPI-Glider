import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
from lib_nrf24 import NRF24
import time
import spidev
import cwiid
from subprocess import call #for shutdown

button_delay = 0.1

pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2]]

radio = NRF24(GPIO, spidev.SpiDev())

#Start listening on SPI bus 1 & GPIO17
radio.begin(1, 17)

time.sleep(1)
radio.setRetries(15,15)
radio.setPayloadSize(32)
radio.setChannel(0x60)

radio.setDataRate(NRF24.BR_2MBPS)
radio.setPALevel(NRF24.PA_MIN)
radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()

radio.openWritingPipe(pipes[1])
radio.openReadingPipe(1, pipes[0])
radio.printDetails()

while True:

    print("Sending signal to receiver...");
    radio.write('u')       
    time.sleep(3) #wait 3 seconds before resending