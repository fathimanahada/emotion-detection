import cv2
import face_recognition
import numpy as np
import os

# create a flag variable to keep track of whether an employee has been recognized
employee_recognized = False

for image in os.listdir('faces'):
            face_image = face_recognition.load_image_file(f'faces/{image}')
            #face_encoding = face_recognition.face_encodings(face_image)[1]
            face_encodings = face_recognition.face_encodings(face_image)

# load the known faces and embeddings
known_face_encodings = []
known_face_names = []

# initialize the webcam
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

video_capture = cv2.VideoCapture(0)

# loop over frames from the webcam
while True:
    # grab the frame from the video feed
    ret, frame = video_capture.read()

    # resize the frame to make it smaller and faster to process
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # detect all faces in the image
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    # loop through each face in the image
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # compare the current face encoding to the known face encodings
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        # check if the current face matches any of the known faces
        if True in matches:
            # find the index of the first match and use it to get the name of the employee
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
            
            # check if the employee has already been recognized in this session
            if not employee_recognized:
                # set the flag variable to True to indicate that the employee has been recognized
                employee_recognized = True
                
                # do something with the recognized employee, such as displaying their name or logging their presence
                print("Employee recognized: {}".format(name))
                
        else:
            # set the flag variable to False to indicate that the employee has not been recognized
            employee_recognized = False

        # draw a box around the face and label it with the name of the employee
        cv2.rectangle(frame, (left*4, top*4), (right*4, bottom*4), (0, 0, 255), 2)
        cv2.putText(frame, name, (left*4, top*4 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

    # display the resulting image
    cv2.imshow('Video', frame)

    # wait for the 'q' key to be pressed to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# release the video capture and close the window
video_capture.release()
cv2.destroyAllWindows()
