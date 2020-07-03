import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
from lib_nrf24 import NRF24
import time
import spidev
from subprocess import call #for shutdown

import cwiid

pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2]]

radio2 = NRF24(GPIO, spidev.SpiDev())

#Start listening on SPI 1 and GPIO17
radio2.begin(1, 17)

radio2.setRetries(15,15)

radio2.setPayloadSize(32)
radio2.setChannel(0x60)
radio2.setDataRate(NRF24.BR_2MBPS)
radio2.setPALevel(NRF24.PA_MIN)

radio2.setAutoAck(True)
radio2.enableDynamicPayloads()
radio2.enableAckPayload()

radio2.openWritingPipe(pipes[0])
radio2.openReadingPipe(1, pipes[1])

radio2.startListening()
radio2.stopListening()

radio2.printDetails()

radio2.startListening()

#delay = 0.1

print 'Press 1 + 2 on your Wii Remote now ...'
time.sleep(1)

# Connect to the Wii Remote. If it times out
# then quit.
try:
  wii=cwiid.Wiimote()
except RuntimeError:
  print "Error opening wiimote connection"
  quit()

print 'Wii Remote connected...\n'
print 'Press some buttons!\n'
print 'Press PLUS and MINUS together to disconnect and quit.\n'

#rumble on good connection
wii.rumble = 1
time.sleep(1)
wii.rumble = 0

wii.rpt_mode = cwiid.RPT_BTN

while True:

    #buttons = wii.state['buttons']

    pipe = [0]
    while not radio2.available(pipe):
        time.sleep(10000/1000000.0)

    recv_buffer = []
    radio2.read(recv_buffer, radio2.getDynamicPayloadSize())
    
    if(recv_buffer[0] == 117): #up
        wii.rumble = 1
        time.sleep(0.5)
        wii.rumble = 0

    if(recv_buffer[0] == 111): #home
        #add functionality for what the home key does - shutdown both PI's??
        print('home')
        #shutdown pi if controller has pressed home key
        call("sudo shutdown -h now", shell=True)