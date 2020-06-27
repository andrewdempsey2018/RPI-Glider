#receiver program that utilizes pigpio

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
from lib_nrf24 import NRF24
import time
import spidev
import pigpio
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
pi = pigpio.pi() # Connect to local Pi.
pulse = 1500

elevatorServo = 13
rudderServo = 12

pi.set_servo_pulsewidth(rudderServo, pulse)
pi.set_servo_pulsewidth(elevatorServo, pulse)

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

    if(recv_buffer[0] == 117): #up
        print('up')
        if(pulse>1000):
            pulse-=50
            pi.set_servo_pulsewidth(rudderServo, pulse)
        time.sleep(delay)

    if(recv_buffer[0] == 100): #down
        print('down')
        if(pulse<2000):
            pulse+=50
            pi.set_servo_pulsewidth(rudderServo, pulse)
        time.sleep(delay)

    if(recv_buffer[0] == 108): #left
        print('left')
        if(pulse>1000):
            pulse-=50
            pi.set_servo_pulsewidth(elevatorServo, pulse)
        time.sleep(delay)

    if(recv_buffer[0] == 114): #right
        print('right')
        if(pulse<2000):
            pulse+=50
            pi.set_servo_pulsewidth(elevatorServo, pulse)
        time.sleep(delay)

    if(recv_buffer[0] == 97): #a
        print('a')
        pulse = 1500
        pi.set_servo_pulsewidth(rudderServo, pulse)
        time.sleep(delay)

    if(recv_buffer[0] == 98): #b
        print('b')
        pulse = 1500
        pi.set_servo_pulsewidth(elevatorServo, pulse)
        time.sleep(delay)

    if(recv_buffer[0] == 111): #home shutdown
        print('home shutdown triggered')
        #shutdown pi if controller has pressed home key 10 times
        call("sudo shutdown -h now", shell=True)