#!/usr/bin/python
#
# Autonomous animal by m.e. of cartheur
# Started 27.01.2015 and only now is it cool!
# This script is for utilization of three motors, although it will also drive only two.

# DEPENDENCIES
# apt-get install python-setuptools python-dev build-essential espeak alsa-utils
# apt-get install python-alsaaudio python-numpy python-twitter python-bottle mplayer

import sys
import time
import subprocess
import os
from random import randint
from threading import Thread
from animalsFred_audioPlayer import AudioPlayer
from animalsFred_gpio import GPIO
from animalsFred_webFramework import WebFramework

fullMsg = ""

NOSE_OPEN = 1015 # GPIO pin assigned to open the nose. XIO-P2
NOSE_CLOSE = 1016 # GPIO pin assigned to close the nose. XIO-P3
EYES_OPEN = 1017 # GPIO pin assigned to open the eyes. XIO-P4
EYES_CLOSE = 1019 # GPIO pin assigned to close the eyes. XIO-P6
MOUTH_OPEN = 1018 # GPIO pin assigned to open the mouth. XIO-P5
MOUTH_CLOSE = 1020 # GPIO pin assigned to close the mouth. XIO-P7

# Establish a connection to the GPIO pins.
io = GPIO()
io.setup( EYES_OPEN )
io.setup( NOSE_OPEN )
io.setup( MOUTH_OPEN )
io.setup( EYES_CLOSE )
io.setup( NOSE_CLOSE )
io.setup( MOUTH_CLOSE )

audio = None
isRunning = True

# Set the mouth in motion to approximate visual pronunciation of audio.
def updateMouth():
    lastMouthEvent = 0
    lastMouthEventTime = 0

    while( audio == None ):
        time.sleep( 0.1 )
        
    while isRunning:
        if( audio.mouthValue != lastMouthEvent ):
            lastMouthEvent = audio.mouthValue
            lastMouthEventTime = time.time()

            if( audio.mouthValue == 1 ):
                io.set( NOSE_OPEN, 1 )
		io.set( MOUTH_OPEN, 1 )
		io.set( NOSE_CLOSE, 0 )
                io.set( MOUTH_CLOSE, 0 )
            else:
                io.set( NOSE_OPEN, 0 )                
		io.set( MOUTH_OPEN, 0 )
		io.set( NOSE_CLOSE, 1 )
                io.set( MOUTH_CLOSE, 1 )
        else:
            if( time.time() - lastMouthEventTime > 0.4 ):
		io.set( NOSE_OPEN, 0 )
                io.set( NOSE_CLOSE, 0 )                
		io.set( MOUTH_OPEN, 0 )
                io.set( MOUTH_CLOSE, 0 )

# A routine for blinking the eyes in a semi-random fashion.
def updateEyes():
    while isRunning:
        io.set( EYES_CLOSE, 1 )
        io.set( EYES_OPEN, 0 )
        time.sleep(0.4)
        io.set( EYES_CLOSE, 0 )
        io.set( EYES_OPEN, 1 )
        time.sleep(0.4)
        io.set( EYES_CLOSE, 1 )
        io.set( EYES_OPEN, 0 )
        time.sleep(0.4)
        io.set( EYES_CLOSE, 0 )
        io.set( EYES_OPEN, 0 )
        time.sleep( randint( 0,7) )
   
def talk(myText):
    if( myText.find( "twitter" ) >= 0 ):
        myText += "0"
        myText = myText[7:-1]
    
    os.system( "espeak \",...\" 2>/dev/null" ) # <-- Sometimes the beginning of audio can get cut off, so, insert silence.
    time.sleep( 0.5 )
    os.system( "espeak -w speech.wav \"" + myText + "\" -s 130" )
    audio.play("speech.wav")
    return myText

mouthThread = Thread(target=updateMouth)
mouthThread.start()
eyesThread = Thread(target=updateEyes)
eyesThread.start()     
audio = AudioPlayer()

web = WebFramework(talk)
isRunning = False
io.cleanup()
sys.exit(1)
