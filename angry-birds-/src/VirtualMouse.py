import AppKit
import cv2
import time
import pygetwindow
import pygame.mouse
import  threading

import HandTrackingModule as htm
import numpy as np
import pyautogui





wCam, hCam = 640, 480
frameR = 100  # frame reduction
smoothening = 5
pTime = 0
plocX, plocY = 140, 450  # previous locations of x and y
clocX, clocY = 0, 0  # current locations of x and y
boolean_fingers = False
index=False
def resc(frame,scale=0.4):
    width=int(frame.shape[1] * scale)
    height=int(frame.shape[1] * scale)
    dimensions = (width,height)
    return  cv2.resize(frame,dimensions,interpolation=cv2.INTER_AREA)

cap = cv2.VideoCapture(0)

cap.set(3, wCam)  # width
cap.set(4, hCam)  # height
detector = htm.handDetector(detectionCon=0.60, maxHands=1)  # only one hand at a time
wScr, hScr = pyautogui.size()



pyautogui.FAILSAFE = False
pygame.init()


def run():

 while True:
    global index
    global pTime
    global plocX
    global  boolean_fingers
    global plocY
    # 1. Find hand Landmarks
    #print(game.game_state)



   # print(pyautogui.position())
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)



    if index:
        boolean_fingers=True


    # 2. Get the tip of the index and middle fingers
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[4][1:]
        # print(x1, y1, x2, y2)


        # 3. Check which fingers are up
        fingers = detector.fingersUp()

        # in moving mouse it was easy to move mouse upwards but in downward direction it is tough so we are setting region
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)

        # 4. Only Index Finger : Moving Mode
        if fingers[1] == 1 and fingers[2] == 0:
            # 5. Convert Coordinates as our cv window is 640*480 but my screen is full HD so have to convert it accordingly
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))  # converting x coordinates
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))  # converting y
            index=True
            # 6. Smoothen Values avoid fluctuations
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening

            # 7. Move Mouse
            pyautogui.moveTo(wScr - clocX, clocY)  # wscr-clocx for avoiding mirror inversion
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)  # circle shows that we are in moving mode
            plocX, plocY = clocX, clocY


        # 8. Both Index and middle fingers are up : Clicking Mode but only if both fingers are near to each other
        if fingers[1] == 1 and fingers[2] == 1:
            index=False
            # 9. Find distance between fingers so that we can make sure fingers are together
            length, img, lineInfo = detector.findDistance(8, 12, img)
            # print(length)
            if boolean_fingers == False:

                pyautogui.moveTo(147, 460)

            # 10. Click mouse if distance short
            if length < 50:
                boolean_fingers = True

                x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
                y3 =  np.interp(y1, (frameR, wCam - frameR), (0, wScr))  # converting x coordinates
                #print(x3,y3)
                #y3 = np.interp(-450, (frameR, hCam - frameR), (0, hScr))  # converting y

                # 6. Smoothen Values avoid fluctuations
                clocX = plocX + (x3 - plocX) / smoothening
                clocY = plocY + (y3 - plocY) / smoothening

                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                plocX, plocY = clocX, clocY

                pyautogui.mouseDown((wScr - clocX)/14, clocY+184, button="left",duration=1)
                #pyautogui.mouseDown()
                #pyautogui.moveTo(wScr - clocX, clocY)
                #print(wScr-clocX,clocY)

            if length > 54 :
                pyautogui.mouseUp()
                boolean_fingers = False


    # 11. Frame Rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)


    # 12. Display
    r=resc(img)
    cv2.imshow("Image", r)

    #cv2.resizeWindow("Image", r)

    cv2.moveWindow('Image', 1180, 450)
    cv2.setWindowProperty('Image', cv2.WND_PROP_TOPMOST, 1)


    if cv2.waitKey(1) == ord('q'):
        break

    #if cv2.waitKey(0):
        #break
    #cv2.waitKey(1)

if __name__ == "__main__":
    run()





