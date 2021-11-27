import cv2
import time
from cvzone.HandTrackingModule import HandDetector
from pynput.keyboard import Controller

detector = HandDetector(detectionCon=0.8)
cap = cv2.VideoCapture(0)
cap.set(3, 720)
cap.set(4, 480)
keywords = Controller()
finalText = ""

keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ":", ], ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]


def drawAll(image, buttonlist):
    for bt in buttonlist:
        btx, bty = bt.pos
        btw, bth = bt.size
        cv2.rectangle(image, bt.pos, (btx + btw, bty + bth), (255, 0, 255), cv2.FILLED)
        cv2.putText(image, bt.text, (btx + 15, bty + 45), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 5)

    return image


class Button:
    def __init__(self, pos, text, size=None):
        if size is None:
            size = [80, 55]
        self.pos = pos
        self.size = size
        self.text = text


buttonList = []
for i in range(len(keys)):

    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))

while True:
    success, img = cap.read()

    img = cv2.resize(img, (1180, 720))
    hands, bbox = detector.findHands(img)
    img = drawAll(img, buttonList)

    if hands:
        lmList = hands[0]['lmList']
        for button in buttonList:
            x, y = button.pos
            w, h = button.size

            if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                cv2.rectangle(img, button.pos, (x + w, y + h), (175, 0, 175), cv2.FILLED)
                cv2.putText(img, button.text, (x + 15, y + 45), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 5)

                length, info = detector.findDistance(lmList[8], lmList[12])

                if length < 40:
                    keywords.press(button.text)

                    cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 15, y + 45), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 5)

                    finalText += button.text
                    time.sleep(0.30)
    cv2.rectangle(img, (70, 480), (1000, 550), (175, 0, 175), cv2.FILLED)
    cv2.putText(img, finalText, (115, 525), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 5)

    cv2.imshow("Original Image", img)
    cv2.waitKey(1)
