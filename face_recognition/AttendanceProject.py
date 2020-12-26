import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

path_training = 'Training_Images'
images_training = []
classTrainingNames = []
TrainingList = os.listdir(path_training)
for cl in TrainingList:                                 #Takes Names from images
    curImg = cv2.imread(f'{path_training}/{cl}')
    images_training.append(curImg)
    classTrainingNames.append(os.path.splitext(cl)[0])     #Remove jpg from name


def findEncodings(images_training):
    encodeList = []
    for img in images_training:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

def present(name):
    with open('Attendance.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []

        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%d/%m/%Y %H:%M:%S')
            f.writelines(f'\n{name},{dtString}')


encodeListKnow = findEncodings(images_training)

path_attendance = 'Attendance_Images'
images_attendance = []
classAttendanceName = []
AttendanceList = os.listdir(path_attendance)

i = 0
for cl in AttendanceList:
    curImg = cv2.imread(f'{path_attendance}/{cl}')
    cap = cv2.imread(cl)
    imgS = cv2.resize(curImg, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    facesCurFrame = face_recognition.face_locations(imgS)  # Detect more than one face
    encodeCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    # Compare faces from folder Pictures with ImagesAttendance
    for encodeFace, faceLoc in zip(encodeCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnow, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnow, encodeFace)
        print(faceDis)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classTrainingNames[matchIndex].upper()
        else:
            name = "UNKNOWN"
        present(name)
        y1, x2, y2, x1 = faceLoc
        y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
        cv2.rectangle(curImg, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.rectangle(curImg, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
        cv2.putText(curImg, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow("Test", curImg)
    cv2.waitKey(1000)
    i += 1

