import streamlit as st
from st_pages import Page, Section, show_pages, add_page_title

add_page_title()

show_pages(
    [
        Page("streamlit_app.py", "Home", "🏠"),
        Section("Face Detection", "🧑"),
        Page("Face_Detection/dataset.py", "Create Dataset", "💾", in_section=True),
        Page("Face_Detection/face_detect.py", "Face Detect", "😀", in_section=True),
        Page("Object_Detection/main.py", "Object Detection", "📱", in_section=False),
        Section("Hand Detection", "🖐️"),
        Page("Hand_Detection/finger_count.py", "Finger Counting", "☝️️", in_section=True),
        Page("Hand_Detection/draw.py", "Drawing", "️✏️", in_section=True),
    ]
)
