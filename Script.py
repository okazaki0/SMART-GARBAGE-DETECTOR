#!/usr/bin/env python
# coding: utf-8

# In[8]:


import keras as kr
import tensorflow as tf
import numpy as np
import pandas as pd
import RPi.GPIO as GPIO          
from time import sleep
import time
import picamera
from keras.preprocessing.image import ImageDataGenerator
import paho.mqtt.client as mqtt
zbal = tf.keras.models.load_model('garbage_model_v5.keras')


# In[67]:



#Driver PIN
in1 = 24
in2 = 23
in3 = 8
in4 = 25

#Ultarsonic PIN
echo=17
trig=4

#Varibles
seuil=30
temp1=1

GPIO.setmode(GPIO.BCM)





#Ultarsonic Setup
def SetupUltrasonic():
    GPIO.setup(trig,GPIO.OUT) 
    GPIO.setup(echo,GPIO.IN)

#Driver Setup
def SetupDriver():
    GPIO.setup(in1,GPIO.OUT)
    GPIO.setup(in2,GPIO.OUT)
    GPIO.setup(in3,GPIO.OUT)
    GPIO.setup(in4,GPIO.OUT)


#Ultrasonic distance
def Ultrasonic():
     pulse_start = 0
     pulse_stop = 0
     duration = 0
     distance = 0
     GPIO.output(trig,GPIO.LOW)
     time.sleep(0.1) 
     GPIO.output(trig,GPIO.HIGH)
     time.sleep(0.000010)
     GPIO.output(trig,GPIO.LOW)

     while GPIO.input(echo)==0:
         pulse_start = time.time()

     while GPIO.input(echo)==1:
         pulse_stop = time.time()

     duration = pulse_stop - pulse_start

     distance = duration*17150.0
     distance = round(distance,2)
     return distance
    
#Stop Function
def stop():
    print("stop")
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.LOW)
        
#Backward Function
def Backward():
    print("Backward")
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.HIGH)
    GPIO.output(in4,GPIO.LOW)
    GPIO.output(in3,GPIO.HIGH)
        
#Forward Function
def Forward():
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(in4,GPIO.HIGH)
    GPIO.output(in3,GPIO.LOW)

def Rotation():
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(in4,GPIO.LOW)
    GPIO.output(in3,GPIO.HIGH)

def Capture():
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        camera.framerate = 24
        output = np.empty((640, 480, 3), dtype=np.uint8)
    #     output.reshape(-1)
        camera.capture('class/c1/img.jpg')
    #print(zbal.predict([output]))

def predict():
    
    test_datagen = ImageDataGenerator(
        rescale=1./255,
        validation_split=0.1
    )
    v = test_datagen.flow_from_directory(
        '/home/pi/Desktop/class',
        target_size=(100, 100)
    )

    test_x, test_y = v.__getitem__(0)
    return zbal.predict(test_x)


# In[68]:


cls=['Biscuit','Bottle','none','Paper']
client = mqtt.Client()

client.connect("test.mosquitto.org", 1883)
SetupUltrasonic()
SetupDriver()
client.loop_start() 
#client.loop_forever()
try:
    while(1):
        d=Ultrasonic()
        if d>seuil or d<0:
            print(d)
            print("run")
            Forward()
            #time.sleep(0.5)
        else:
            stop()
            Capture()
            preds = predict()
            p=np.argmax(preds[0])
            res='pred:'+cls[p]+' with proba: ' +str(max(preds[0]))
            #print(res)
            if p!=2:
                client.publish('garbage/notif',res)
            if p==2 or max(preds[0])<0.80:
                Rotation()
                time.sleep(0.5)
            time.sleep(0.5)
except:
    GPIO.cleanup()





# In[ ]:




