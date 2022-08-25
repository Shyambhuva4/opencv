

import numpy as np
import cv2
import handTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import time

wCam,hCam=640,480


cap=cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
ptime =0

detector=htm.handdetector(detectionCon=0.7)


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volrange=volume.GetVolumeRange()

minvol=volrange[0]
maxvol=volrange[1]
vol=0
volbar=400
volper=0

while True:
    succes, img =cap.read()
    # find hand
    img=detector.findHands(img)
    lmlist,_=detector.Position(img,draw=False)
    print(lmlist)
    if len(lmlist)!=0:
     print(lmlist[4],lmlist[8])

     x1,y1=lmlist[4][1], lmlist[4][2]
     x2, y2 = lmlist[8][1], lmlist[8][2]
     x3,y3 = lmlist[12][1],lmlist[12][2]
     cx,cy=(x1+x2)//2,(y1+y2)//2

     cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
     cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
     cv2.circle(img, (x3, y3), 15, (255, 0, 255), cv2.FILLED)
     cv2.line(img,(x1,y1),(x2,y2),(255,0,400),3)
     cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
     cv2.line(img, (x2, y2), (x3, y3), (255, 300, 400), 3)
     length=math.hypot(x2-x1,y2-y1)
     #print(length)
     length2 = math.hypot(x3 - x2, y3 - y2)
     vol=np.interp(length,[40,200],[minvol,maxvol])
     volbar=np.interp(length,[40,200],[400,150])
     volper=np.interp(length,[40,200],[0,100])
     print(length2)

     if(length2>=40):
      volume.SetMasterVolumeLevel(vol, None)
      if length<40:
         cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)
      if length>200:
         cv2.circle(img, (cx, cy), 15, (0, 0, 255), cv2.FILLED)

      cv2.rectangle(img,(50,150),(85,400),(0,255,0),3)
      cv2.rectangle(img, (50,int(volbar)), (85, 400), (0, 255, 0), cv2.FILLED)
      cv2.putText(img, f'VOL:{int(volper)}%', (40, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    ctime =time.time()
    fps = 1 / (ctime - ptime)
    ptime = ctime
    cv2.putText(img,f'FPS:{int(fps)}',(40,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,400,32),2)
    cv2.imshow("Tracker",img)
    cv2.waitKey(1)