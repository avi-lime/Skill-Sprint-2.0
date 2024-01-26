import cv2
from ultralytics import YOLO
import streamlit as st
from st_pages import add_page_title
from streamlit_webrtc import webrtc_streamer

webrtc_streamer(
    # ...
    rtc_configuration={  # Add this config
        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
    }
    # ...
)

add_page_title()
# loading model
model = YOLO('yolov8n.pt')

# loading video
path = 'sample.mp4'
# change path to input custom video

# read frames
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
# replace 'path' with 0 to capture webcam

frame_holder = st.empty()
stop_pressed_status = st.button("Stop")

ret = True
while ret:
    ret, frame = cap.read()
    if ret is True:
        # detecting objects from frame
        # track object
        result = model.track(frame, persist=True)

        # plot results
        frame_ = result[0].plot()

        # visualize
        frame_holder.image(frame_, channels="BGR")
        if cv2.waitKey(1) & 0xFF == ord('q') or stop_pressed_status:
            break

cap.release()
cv2.destroyAllWindows()
