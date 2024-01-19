import cv2
import os
import numpy as np
import time

haar_file = "haarcascade_frontalface_default.xml"
datasets = 'C:\\Users\\sa319\\OneDrive\\Desktop\\coding\\python\\workshop\\Face_Detection\\Dataset\\'
(images, labels, names, id) = ([], [], {}, 0)

for (subdirs, dirs, files) in os.walk(datasets):
    for subdir in dirs:
        names[id] = subdir
        subjectpath = os.path.join(datasets, subdir)
        for filename in os.listdir(subjectpath):
            path = os.path.join(subjectpath, filename)
            label = id
            images.append(cv2.imread(path, 0))
            labels.append(int(label))
        id = id + 1

(images, labels) = [np.array(lists) for lists in [images, labels]]
model = cv2.face.LBPHFaceRecognizer.create()
model.train(images, labels)

face_cascade = cv2.CascadeClassifier(haar_file)

cap = cv2.VideoCapture(0)

print("Web cam is open?", cap.isOpened())

time.sleep(2)
count = 1

while True:
    ret, frame = cap.read()
    if ret is True:
        img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(img_gray, 1.3, 4)
        # detectMultiScale(source, scaleFactor, minNeighbors)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 255), 2)
            face = img_gray[y:y+h, x:x+h]
            face_resize = cv2.resize(face, (640, 400))
            predictions = model.predict(face_resize)
            if predictions[1] < 30:
                cv2.putText(frame, '%s' % (names[predictions[0]].strip()), (x + 5, y + 25 + h), cv2.FONT_HERSHEY_COMPLEX,
                            1.5, (20, 185, 20), 2)
            else:
                cv2.putText(frame, "Unknown", (x + 5, y + 25 + h), cv2.FONT_HERSHEY_SIMPLEX,
                            1.5, (0, 0, 255), 2)

        cv2.imshow("Face Recognition", frame)
        if cv2.waitKey(1) == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()

