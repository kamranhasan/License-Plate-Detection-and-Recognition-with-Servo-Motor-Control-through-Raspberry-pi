filename = './video2.mp4'

import cv2
import imutils
from DetectPlate import detection
import text_recognition
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)
GPIO.setup(3, GPIO.OUT)
pwm=GPIO.PWM(3, 50)
pwm.start(0)

def SetAngle(angle):
    duty = angle / 18 + 2
    GPIO.output(3, True)
    pwm.ChangeDutyCycle(duty)
    sleep(10)
    GPIO.output(3, False)
    pwm.ChangeDutyCycle(0)

SetAngle(0)
print("Servo at 0 degree")

cap = cv2.VideoCapture(filename)
count = 0
while cap.isOpened():
    ret,frame = cap.read()
    if ret == True:
        cv2.imwrite("./output/frame%d.jpg" % count, frame)
        count = count + 1
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    else:
        break
cap.release()
cv2.destroyAllWindows()
plate_detect = False
i = 1
while not plate_detect and i < count:
    plate_detect=detection("./output/frame%d.jpg"%(count-i))
    i += 1

if plate_detect == False:
    print("Detection Not Successful")
else:
    permission=text_recognition.text_data()
    if permission==1:
        print("Permission Granted")
        print("Servo at 90 degree")
        SetAngle(90)
        SetAngle(0)
        print("Servo at 0 degree")
    else:
        print("Vehicle Not Allowed")
    
pwm.stop()
GPIO.cleanup()