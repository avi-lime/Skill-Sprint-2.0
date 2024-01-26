import cv2
from cvzone.HandTrackingModule import HandDetector
import streamlit as st
from st_pages import Page, Section, show_pages, add_page_title

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector()
paths = []
i = -1
# streamlit

add_page_title()

frame_placeholder = st.empty()
stop_button_pressed = st.button("Stop")

while True and not stop_button_pressed:
    ret, frame = cap.read()
    if ret is True:
        hands, frame = detector.findHands(frame, draw=False)
        if hands:
            for hand in hands:
                

        if hands:
            for hand in hands:
                fingers = detector.fingersUp(hand)

                x, y, w, h = hand["bbox"]
                lmList = hand["lmList"]
                index_finger = lmList[8]
                ix, iy, iz = index_finger
                totalFingers = fingers.count(1)
                if totalFingers == 1 and fingers[1]:
                    try:
                        paths[i].append((ix, iy))
                    except IndexError:
                        paths.append([])
                        paths[i].append((ix, iy))
                elif totalFingers == 0:
                    paths.clear()
        if paths:
            for path in paths:
                for index, point in enumerate(path):
                    cv2.circle(frame, point, 2, (0, 0, 255), 1)
                    if len(path) > 2 and index > 0:
                        cv2.line(frame, point, path[index - 1], (0, 0, 255), 2)

        frame_placeholder.image(frame, channels="BGR")

        if cv2.waitKey(1) & 0xFF == ord("q") or stop_button_pressed:
            break

cap.release()
cv2.destroyAllWindows()
