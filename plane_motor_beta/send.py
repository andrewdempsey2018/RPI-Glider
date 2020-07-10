#Use the GPIO numbering system for RPI pins
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

#Needed for interfacing with the LORA module
from lib_nrf24 import NRF24
import spidev

#For time dependent functions
import time

#Library for Wii mote functionality
import cwiid

#'Call' is needed so we can shutdown the Pi from Python
from subprocess import call

#function definitions
def rumble():
  wii.rumble = 1
  time.sleep(0.25)
  wii.rumble = 0
  time.sleep(0.25)
  wii.rumble = 1
  time.sleep(0.25)
  wii.rumble = 0
  time.sleep(0.25)

def getMillis():
  return int(round(time.time() * 1000))

#Import emum for clean switching of program state
from enum import Enum

class State(Enum):
    MENU = 1
    FLY = 4
    EXIT = 3
    CALIBRATE = 2

#set the initial state of the program to FLY mode
programState = State.FLY

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

print('Press 1 + 2 on your Wii Remote now ...')
time.sleep(1)

# Connect to the Wii Remote. If it times out
# then quit.
try:
    wii=cwiid.Wiimote()
except RuntimeError:
    print("Error opening wiimote connection")
    quit()

print('Wii Remote connected...\n')
print('Press some buttons!\n')
print('Press PLUS and MINUS together to disconnect and quit.\n')

#rumble on good connection
rumble()

wii.rpt_mode = cwiid.RPT_BTN

#These two variables are used for checking how long the A button is held
aPressedStart = 0
aPressedEnd = 0

oncePerLoop = False #this variable is used to initialise some settings once everytime a menu is navigated

#This loop contains functionality that is universal to the program
while True:

    buttons = wii.state['buttons']

    #check how long the a buttons is pressed and see if we need to go to the main menu
    if(buttons & cwiid.BTN_A):

        if(aPressedStart == 0):
            aPressedStart = getMillis()

        if((aPressedEnd - aPressedStart) >= 5000):
            print("A has been held for 5000 milliseconds(5 seconds), going to menu")
            aPressedStart = 0
            programState = State.MENU
            oncePerLoop = False
    else:
        aPressedStart = 0

    if(programState == State.FLY):

        buttons = wii.state['buttons']

        #Set the Wii mote led to fly mode indication
        if not(oncePerLoop):
            oncePerLoop = True
            wii.led = 2
            print("Program in FLY mode")

        # If Plus and Minus buttons pressed
        # together then rumble and quit.
        #if (buttons - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0):  
        #    print('\nClosing connection ...')
        #    rumble()
        #    exit(wii)  
  
        # Check if other buttons are pressed by
        # doing a bitwise AND of the buttons number
        # and the predefined constant for that button.
        if (buttons & cwiid.BTN_LEFT):
            print('Left pressed')
            radio.write('l')
            time.sleep(button_delay)         

        if(buttons & cwiid.BTN_RIGHT):
            print('Right pressed')
            radio.write('r')
            time.sleep(button_delay)          

        if (buttons & cwiid.BTN_UP):
            print('Up pressed')
            radio.write('u')       
            time.sleep(button_delay)          
    
        if (buttons & cwiid.BTN_DOWN):
            print('Down pressed') 
            radio.write('d')    
            time.sleep(button_delay)  
    
        if (buttons & cwiid.BTN_1):
            print('Button 1 pressed')
            time.sleep(button_delay)          

        if (buttons & cwiid.BTN_2):
            print('Button 2 pressed')
            time.sleep(button_delay)          

        if (buttons & cwiid.BTN_A):
            print('Button A pressed')
            radio.write('a') 
            time.sleep(button_delay)          

        if (buttons & cwiid.BTN_B):
            print('Button B pressed')
            radio.write('b') 
            time.sleep(button_delay)

        if (buttons & cwiid.BTN_MINUS):
            print('Minus Button pressed')
            radio.write('-')
            time.sleep(button_delay)

        if (buttons & cwiid.BTN_PLUS):
            print('Plus Button pressed')
            radio.write('+')
            time.sleep(button_delay)

        if (buttons & cwiid.BTN_HOME):
            print('Home Button pressed')
            radio.write('h')
            time.sleep(button_delay)

    if(programState == State.MENU):

        buttons = wii.state['buttons']

        #Set the Wii mote led to menu mode indication
        if not(oncePerLoop):
            oncePerLoop = True
            wii.led = 1
            print("Program in MENU mode")

        if (buttons & cwiid.BTN_UP):
            print('Up pressed, going to FLY mode')
            oncePerLoop = False
            programState = State.FLY
            radio.write('f')       
            #time.sleep(button_delay)

        if (buttons & cwiid.BTN_DOWN):
            print('Down pressed, going to Calibrate mode')
            oncePerLoop = False
            programState = State.CALIBRATE
            radio.write('c')       
            #time.sleep(button_delay)

        if (buttons & cwiid.BTN_LEFT):
            print('Left pressed, going to EXIT menu')
            oncePerLoop = False
            programState = State.EXIT
            #time.sleep(button_delay)

    if(programState == State.EXIT):

        buttons = wii.state['buttons']

        #Set the Wii mote led to exit mode indication
        if not(oncePerLoop):
            oncePerLoop = True
            wii.led = 8
            print("Program in EXIT menu")

        if (buttons & cwiid.BTN_UP):
            print('Up pressed, going to FLY mode')
            oncePerLoop = False
            programState = State.FLY
            #radio.write('u')       
            #time.sleep(button_delay)

        if (buttons & cwiid.BTN_2):
            print('Shutting down transmitter')
            rumble()
            radio.write('o')
            call("sudo shutdown -h now", shell=True) 

    if(programState == State.CALIBRATE):

        buttons = wii.state['buttons']

        #Set the Wii mote led to calibrate mode indication
        if not(oncePerLoop):
            oncePerLoop = True
            wii.led = 4
            print("Program in MOTOR CALIBRATE mode")

        if (buttons & cwiid.BTN_MINUS):
            print('Minus Button pressed')
            radio.write('-')
            time.sleep(button_delay)   
    
        if (buttons & cwiid.BTN_PLUS):
            print('Plus Button pressed')
            radio.write('+')
            time.sleep(button_delay)

    # used for determining how long A button is pressed
    aPressedEnd = getMillis()