import cv2 as cv
import numpy as np
import Hand_Tracking_Module as htm

cap = cv.VideoCapture(0)
detector = htm.handDetector(detectionCon=1)


def FindHand(lmList):
    x = frame.shape[1]
    for i in range(20):
        if(lmList[i][1] < x):
            x = lmList[i][1]

    y = frame.shape[0]
    for i in range(20):
        if(lmList[i][2] < y):
            y = lmList[i][2]
    
    xEnd = 0
    for i in range(20):
        if(lmList[i][1] > xEnd):
            xEnd = lmList[i][1]

    yEnd = 0
    for i in range(20):
        if(lmList[i][2] > yEnd):
            yEnd = lmList[i][2]

    cv.rectangle(frame, (x,y), (xEnd,yEnd), (0, 0, 255), 2) 

def FindFingerCount(frame):
    frame = detector.findHands(frame, True)
    lmList = detector.findPosition(frame, draw=False)[0]

    fingerIds = [4, 8, 12, 16, 20]
    if(len(lmList) != 0):
        FindHand(lmList)
        fingers = []

        for fingerId in fingerIds:
            if fingerId == 4:
                if(lmList[fingerId][1] < lmList[fingerId-1][1]):
                    fingers.append(1)
                else:
                    fingers.append(0)
            else:
                if(lmList[fingerId][2] < lmList[fingerId-2][2]):
                    fingers.append(1)
                else:
                    fingers.append(0)
        
        total = fingers.count(1)
        cv.putText(frame, str(total), (50, 50), cv.FONT_HERSHEY_SCRIPT_COMPLEX, 2, (255, 0, 0), 3)

while cap.isOpened():
    ret, frame = cap.read()
    frame = cv.flip(frame, 1)
    FindFingerCount(frame)

    if cv.waitKey(10) & 0xFF == ord('q'):
        break

    cv.imshow("Video", frame)

cap.release()
cv.destroyAllWindows()