#-*-coding:utf-8 -*-
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import RPi.GPIO as GPIO
from time import sleep

# firebase setting
cred = credentials.Certificate("pabloairteama-firebase-adminsdk-n7x78-5d3b0a74ae.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
doc_ref = db.collection(u'OrderDetail').document(u'A20220907AXC03')
state = False

# servomoter setting
servoPin = 12
SERVO_MAX_DUTY = 12.5
SERVO_MIN_DUTY = 4

GPIO.setmode(GPIO.BOARD)
GPIO.setup(servoPin, GPIO.OUT)
servo = GPIO.PWM(servoPin, 50)
servo.start(0)

# while
while True:
    try:
        degree = 0
        doc = doc_ref.get()
        onGoing = doc.to_dict()['onGoing']
        print(u'Ongoing data: {}'.format(onGoing))
        
        if state != onGoing :
            if onGoing == 0 :
                degree = 45
                duty = SERVO_MIN_DUTY + (degree*(SERVO_MAX_DUTY-SERVO_MIN_DUTY)/180.0)
                servo.ChangeDutyCycle(duty)
                print("turn 90 dgree")
            elif onGoing == 1 :
                degree = 0
                duty = SERVO_MIN_DUTY + (degree*(SERVO_MAX_DUTY-SERVO_MIN_DUTY)/180.0)
                servo.ChangeDutyCycle(duty)
                print("turn 0 dgree")
                
        else:
            print("do not turn")

        state = onGoing    
        sleep(5)
        servo.stop()
        GPIO.cleanup()
        
    except google.cloud.exceptions.NotFound:
        print(u'No such document!')

        
