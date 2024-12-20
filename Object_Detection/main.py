import cv2
from ultralytics import YOLO
import streamlit as st

# loading model
model = YOLO('yolov8n.pt')

# loading video
path = 'sample.mp4'
# change path to input custom video

# read frames
cap = cv2.VideoCapture("acb.png")
cap.set(3, 1280)
cap.set(4, 720)
# replace 'path' with 0 to capture webcam

frame_holder = st.empty()
stop_pressed_status = st.button("Stop")

ret = True

from inference_sdk import InferenceHTTPClient

CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="WB1P5a9qPZXi6Ym4DIB7"
)

while ret:
    ret, frame = cap.read()
    if ret is True:
        # detecting objects from frame
        # track object
        result = CLIENT.infer(frame, model_id="substation-elements-detection/1")

        # Extract prediction details
        if len(result['predictions']) > 0:    
            prediction = result['predictions'][0]
            print(prediction)
            x_center = prediction['x']
            y_center = prediction['y']
            width = prediction['width']
            height = prediction['height']
            confidence = prediction['confidence']
            class_name = prediction['class']

            # Calculate bounding box coordinates
            x_min = int(x_center - width / 2)
            y_min = int(y_center - height / 2)
            x_max = int(x_center + width / 2)
            y_max = int(y_center + height / 2)

            # Draw the bounding box and label on the image
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (255, 0, 0), 2)
            label = f"{class_name} ({confidence:.2f})"
            cv2.putText(frame, label, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

        # visualize
        frame_holder.image(frame, channels="BGR")
        if cv2.waitKey(1) & 0xFF == ord('q') or stop_pressed_status:
            break

cap.release()
cv2.destroyAllWindows()
