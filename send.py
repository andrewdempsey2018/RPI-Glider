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

  buttons = wii.state['buttons']

  # If Plus and Minus buttons pressed
  # together then rumble and quit.
  if (buttons - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0):  
    print '\nClosing connection ...'
    wii.rumble = 1
    time.sleep(1)
    wii.rumble = 0
    exit(wii)  
  
  # Check if other buttons are pressed by
  # doing a bitwise AND of the buttons number
  # and the predefined constant for that button.
  if (buttons & cwiid.BTN_LEFT):
    print 'Left pressed'
    radio.write('l')
    time.sleep(button_delay)         

  if(buttons & cwiid.BTN_RIGHT):
    print 'Right pressed'
    radio.write('r')
    time.sleep(button_delay)          

  if (buttons & cwiid.BTN_UP):
    print 'Up pressed' 
    radio.write('u')       
    time.sleep(button_delay)          
    
  if (buttons & cwiid.BTN_DOWN):
    print 'Down pressed'  
    radio.write('d')    
    time.sleep(button_delay)  
    
  if (buttons & cwiid.BTN_1):
    print 'Button 1 pressed'
    time.sleep(button_delay)          

  if (buttons & cwiid.BTN_2):
    print 'Button 2 pressed'
    time.sleep(button_delay)          

  if (buttons & cwiid.BTN_A):
    print 'Button A pressed'
    radio.write('a') 
    time.sleep(button_delay)          

  if (buttons & cwiid.BTN_B):
    print 'Button B pressed'
    radio.write('b') 
    time.sleep(button_delay)

  if (buttons - cwiid.BTN_HOME - cwiid.BTN_2 == 0):
    print 'Shutting down transmitter'
    time.sleep(button_delay)
	#shutdown pi if home is pressed
    wii.rumble = 1
    time.sleep(1)
    wii.rumble = 0
    radio.write('o')
    call("sudo shutdown -h now", shell=True)          
    
  if (buttons & cwiid.BTN_MINUS):
    print 'Minus Button pressed'
    time.sleep(button_delay)   
    
  if (buttons & cwiid.BTN_PLUS):
    print 'Plus Button pressed'
    time.sleep(button_delay)