import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
from lib_nrf24 import NRF24
import time
import spidev
from gpiozero import Servo
from subprocess import call #for shutdown

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

#setup the servos
myCorrection=0.045
maxPW=(2.0+myCorrection)/1000
minPW=(1.0-myCorrection)/1000
 
rudderServo = Servo(12,min_pulse_width=minPW,max_pulse_width=maxPW)
elevatorServo = Servo(13,min_pulse_width=minPW,max_pulse_width=maxPW)

rudderServoVal = 0.0
elevatorServoVal = 0.0

rudderServo.detach()
elevatorServo.detach()

#delay for allowing servos time to move
delay = 0.1

while True:
    pipe = [0]
    while not radio2.available(pipe):
        time.sleep(10000/1000000.0)

    recv_buffer = []
    radio2.read(recv_buffer, radio2.getDynamicPayloadSize())
    #print ("Received:") ,
    #print (recv_buffer)

    prevRudderVal = rudderServoVal
    prevElevatorVal = elevatorServoVal

    if(recv_buffer[0] == 117): #up
        elevatorServoVal -= 0.1
        print('up')
        if (elevatorServoVal <= -1.0):
            elevatorServoVal = -1.0
        time.sleep(delay)

    if(recv_buffer[0] == 100): #down
        elevatorServoVal += 0.1
        print('down')
        if (elevatorServoVal >= 1.0):
          elevatorServoVal = 1.0
        time.sleep(delay)

    if(recv_buffer[0] == 108): #left
        rudderServoVal -= 0.1
        print('left')
        if (rudderServoVal <= -1.0):
            rudderServoVal = -1.0
        time.sleep(delay)

    if(recv_buffer[0] == 114): #right
        rudderServoVal += 0.1
        print('right')
        if (rudderServoVal >= 1.0):
            rudderServoVal = 1.0
        time.sleep(delay)

    if(recv_buffer[0] == 97): #a
        print('a')
        elevatorServoVal = 0.0
        time.sleep(delay)

    if(recv_buffer[0] == 98): #b
        print('b')
        rudderServoVal = 0.0
        time.sleep(delay)

    if(recv_buffer[0] == 111): #home
        #add functionality for what the home key does - shutdown both PI's??
        print('home')
        #shutdown pi if controller has pressed home key
        call("sudo shutdown -h now", shell=True)

    #move the servos based on the values received and pause them when they dont need to move
    if(rudderServoVal == prevRudderVal):
        rudderServo.detach()

    if(rudderServoVal != prevRudderVal):
        rudderServo.value = rudderServoVal

    if(elevatorServoVal == prevElevatorVal):
        elevatorServo.detach()

    if(elevatorServoVal != prevElevatorVal):
        elevatorServo.value = elevatorServoVal