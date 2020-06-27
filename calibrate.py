import cwiid
import time
import pigpio

#wii mote test for gpio 12&13
#use for calibrating the servos at GPIO 12 & 13
# Connects the Wii mote directly to the PI
 
button_delay = 0.1
 
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
 
wii.rpt_mode = cwiid.RPT_BTN


pi = pigpio.pi() # Connect to local Pi.
pulse = 1500

pi.set_servo_pulsewidth(12, pulse)
pi.set_servo_pulsewidth(13, pulse)
 
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
    if(pulse>1000):
      pulse-=50
      pi.set_servo_pulsewidth(13, pulse)
    time.sleep(button_delay)
 
  if(buttons & cwiid.BTN_RIGHT):
    print 'Right pressed'
    if(pulse<2000):
      pulse+=50
      pi.set_servo_pulsewidth(13, pulse)
    time.sleep(button_delay)
 
  if (buttons & cwiid.BTN_UP):
    print 'Up pressed'
    if(pulse>1000):
      pulse-=50
      pi.set_servo_pulsewidth(12, pulse)
    time.sleep(button_delay)
 
  if (buttons & cwiid.BTN_DOWN):
    print 'Down pressed'
    if(pulse<2000):
      pulse+=50
      pi.set_servo_pulsewidth(12, pulse)
    time.sleep(button_delay)
 
  if (buttons & cwiid.BTN_1):
    print 'Button 1 pressed'
    time.sleep(button_delay)
 
  if (buttons & cwiid.BTN_2):
    print 'Button 2 pressed'
    time.sleep(button_delay)
 
  if (buttons & cwiid.BTN_A):
    print 'Button A pressed'
    pulse = 1500
    pi.set_servo_pulsewidth(12, pulse)
    time.sleep(button_delay)
 
  if (buttons & cwiid.BTN_B):
    pulse = 1500
    pi.set_servo_pulsewidth(13, pulse)
    time.sleep(button_delay)
 
  if (buttons & cwiid.BTN_HOME):
    print 'Home Button pressed'
    time.sleep(button_delay)
 
  if (buttons & cwiid.BTN_MINUS):
    print 'Minus Button pressed'
    time.sleep(button_delay)
 
  if (buttons & cwiid.BTN_PLUS):
    print 'Plus Button pressed'
    time.sleep(button_delay)