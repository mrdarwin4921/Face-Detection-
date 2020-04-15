from face_normalisation import get_normalised_faces
from train_model import *
import cv2
cap = cv2.VideoCapture(0)

faceCascade = cv2.CascadeClassifier('P:\\GIT_FILE\\Face_Recognition\\OpenCVDemo\\haarcascade_frontalface_default.xml')

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face_coord = faceCascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)

    if len(face_coord):
        faces = get_normalised_faces(gray, face_coord)

        for i, face in enumerate(faces):
            pred, conf = rec_fisher.predict(face)
            image, labels, labels_dict = collect_dataset()

            threshold = 1000
            if conf < threshold:
                per = int((threshold - conf) / threshold * 100)
                cv2.putText(frame, labels_dict[pred].capitalize() + str(per),
                            (face_coord[i][0], face_coord[i][1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)
            else:
                cv2.putText(frame, "Unknown",
                            (face_coord[i][0], face_coord[i][1] - 10),
                            cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 1)

            cv2.rectangle(frame, (face_coord[i][0], face_coord[i][1]), (face_coord[i][0] + face_coord[i][2], face_coord[i][1] + face_coord[i][3]), (255, 0, 0), 1)

    cv2.imshow('frame', frame)
    k = cv2.waitKey(30) & 0xff
    if k==27:
        break

cap.release()
cv2.destroyAllWindows()
