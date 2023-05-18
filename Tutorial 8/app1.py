from flask import Flask, render_template, Response
import cv2
import face_recognition
import numpy as np
import os
import math
import collections
import time
from deepface import DeepFace
from datetime import datetime
from pymongo import MongoClient


app=Flask(__name__)

# detectedNameList=[] # a list to store detected name for searching
# item=''
# currenSectionTime= datetime.now().time()

# client = MongoClient("mongodb+srv://fathimanahada06:fnhd_681@cluster0.clnokkg.mongodb.net/?retryWrites=true&w=majority")
#  #db
# db = client.get_database('emotion')
# #collection
# records = db.collection

# def add_data(name, time, avg_emotion):
#      document = {
#          "Name": name,
#          "Time": time,
#          #"Dominant_emotion": dominant_emotion,
#          "Average_emotion": avg_emotion
#      }
#      return records.insert_one(document)



# Initialize some variables
#class FaceRecognition:
face_locations = []
face_encodings = []
face_names = []
known_face_encodings = []
known_face_names = []
process_current_frame = True

for image in os.listdir('faces'):
            face_image = face_recognition.load_image_file(f'faces/{image}')
            #face_encoding = face_recognition.face_encodings(face_image)[1]
            face_encodings = face_recognition.face_encodings(face_image)


def gen_frames():  

    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    camera = cv2.VideoCapture(-1)

    # start_time = time.time()
    # session_duration = 30
    # exp_time =  start_time + float(session_duration)
    # emotion_count = 0
    # name_count =0
    # emotion_list = []

    while True:

        current_time = datetime.now().strftime('%Y-%m-%d  %I:%M:%S')
        # if time.time() >= exp_time:
        #         print("Session expired")
        #         break

            
           
        success, frame = camera.read()  # read the camera frame
        if not success:
            print('cant able to access camera')
            break
        else:
            small_frame = cv2.resize(frame, (0, 0), fx=10, fy=10)
            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]
           

                # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    name = "Unknown"
                    confidence = '???'
                   

                    # Calculate the shortest distance to face
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)

                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]
                    #detectedNameList.append(name)
                    face_names.append(f'{name}')

            #process_current_frame = not process_current_frame

            # def check(): 
            #      # check if the current face matches any of the known faces
            #      if len(detectedNameList)> 1: # ensuring that the condition only happen after 2nd face matche
            #         if item in detectedNameList: 
            #             if currenSectionTime+datetime.timedelta(minutes =15)<=current_time: # type: ignore
            #                 add_data(name,current_time,dominant_emotion)
                            
            #             else:
            #                 print('Employee already recognized: '+item) 
            #                 #add_data(current_time,avg_emotion)                 
            #                 # do something with the recognized employee, such as displaying their name or logging their presence                 
            #         else:
            #             #add_data(name,current_time,avg_emotion)
            #     # else:
            #     #     add_data(name,current_time,avg_emotion)
               
            #             print(detectedNameList)  

             # Display the results
            for (top, right, bottom, left), name in zip(face_locations,face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                    
                    # Create the frame with the name
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                
                
        # Add the emotion label to the image
            
                # result = DeepFace.analyze(frame,actions="emotion",enforce_detection=False)
                # dominant_emotion = result[0]['dominant_emotion']
                # print(dominant_emotion)
                # #insert into db
                # if name != 'Unknown':
                 
                 
                
                #   #add_data(name,current_time,dominant_emotion)
                
               
               
                #  cv2.putText(frame,dominant_emotion,(left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)    
               
            #     emotion_list.append(dominant_emotion)
            #     # Increment the emotion counter
            # emotion_count += 1
            

            # Display the resulting image
        cv2.imshow('Face Recognition', frame)

            # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xff == ord('q'):
                    break
        # if emotion_count >= 10 :
        #            break
        # avg_emotion = collections.Counter(emotion_list).most_common(1)[0][0]

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
if __name__=='__main__':
    app.run(debug=True)