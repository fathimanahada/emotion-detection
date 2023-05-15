from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.http import HttpResponse

import time
import face_recognition
import os, sys
import cv2
import numpy as np
import math
import collections
from deepface import DeepFace
from datetime import datetime
from pymongo import MongoClient


detectedNameList=[] # a list to store detected name for searching
item=''
currenSectionTime= datetime.now().time()

client = MongoClient("mongodb+srv://fathimanahada06:fnhd_681@cluster0.clnokkg.mongodb.net/?retryWrites=true&w=majority")
 #db
db = client.get_database('emotion')
#collection
records = db.collection

def add_data(name, time, avg_emotion):
     document = {
         "Name": name,
         "Time": time,
         #"Dominant_emotion": dominant_emotion,
         "Average_emotion": avg_emotion
     }
     return records.insert_one(document)


FACE_DETECTOR_PATH = "{base_path}/cascades/haarcascade_frontalface_default.xml".format(
	base_path=os.path.abspath(os.path.dirname(__file__)))
@csrf_exempt
def facedetect(request):
	# initialize the data dictionary to be returned by the request
	data = {"success": False}
	# check to see if this is a post request
	if request.method == "GET":
		
          class FaceRecognition:
            face_locations = []
            face_encodings = []
            face_names = []
            known_face_encodings = []
            known_face_names = []
            process_current_frame = True
            


            def __init__(self):
                self.encode_faces()
                self.employee_recognized = False 

            def encode_faces(self):
                for image in os.listdir('face_detector/faces'):
                    face_image = face_recognition.load_image_file(f'faces/{image}')
                    #face_encoding = face_recognition.face_encodings(face_image)[1]
                    face_encodings = face_recognition.face_encodings(face_image)
                    if len(face_encodings) > 0:
                        face_encoding = face_encodings[0]
                    else:
                        continue  # Skip this image if no faces were found

                    print(face_image)

                    self.known_face_encodings.append(face_encoding)
                    self.known_face_names.append(image)
                print(self.known_face_names)

            def run_recognition(self):

                face_cascade = cv2.CascadeClassifier('face_detector/haarcascade_frontalface_default.xml')
                
                video_capture = cv2.VideoCapture(0)
                #
                # f = open('labels.txt', 'a')
                start_time = time.time()
                session_duration = 30
                exp_time =  start_time + float(session_duration)
                emotion_count = 0
                name_count =0
                emotion_list = []


                while True:
                    current_time = datetime.now().strftime('%Y-%m-%d  %I:%M:%S')
                    if time.time() >= exp_time:
                        print("Session expired")
                        break

                    ret, frame = video_capture.read()
                
                
                    # Only process every other frame of video to save time
                    if self.process_current_frame:
                        # Resize frame of video to 1/4 size for faster face recognition processing
                         small_frame = cv2.resize(frame, (0, 0), fx=0, fy=0)

                        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
                         rgb_small_frame = small_frame[:, :, ::-1]

                        # Find all the faces and face encodings in the current frame of video
                         self.face_locations = face_recognition.face_locations(rgb_small_frame)
                         self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

                    self.face_names = []
                    for face_encoding in self.face_encodings:
                            # See if the face is a match for the known face(s)
                            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                            name = "Unknown"
                            confidence = '???'
                        

                            # Calculate the shortest distance to face
                            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)

                            best_match_index = np.argmin(face_distances)
                            if matches[best_match_index]:
                                name = self.known_face_names[best_match_index]
                                #confidence = face_confidence(face_distances[best_match_index])
                            detectedNameList.append(name)
                            self.face_names.append(f'{name}')

                    self.process_current_frame = not self.process_current_frame

                    def check(): 
                        # check if the current face matches any of the known faces
                        if len(detectedNameList)> 1: # ensuring that the condition only happen after 2nd face matche
                            if item in detectedNameList: 
                                if currenSectionTime+datetime.timedelta(minutes =15)<=current_time: # type: ignore
                                    add_data(name,current_time,avg_emotion)
                                    
                                else:
                                    print('Employee already recognized: '+item) 
                                    #add_data(current_time,avg_emotion)                 
                                    # do something with the recognized employee, such as displaying their name or logging their presence                 
                            else:
                                #add_data(name,current_time,avg_emotion)
                        # else:
                        #     add_data(name,current_time,avg_emotion)
                    
                                print(detectedNameList)  

                    # Display the results
                    for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
                        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                        top *= 4
                        right *= 4
                        bottom *= 4
                        left *= 4
                            
                            # Create the frame with the name
                        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                        # #cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)
                        # def check()  : 
                    
                        #  found = False
                        #  recognized_namelist = []
                        #  # check if the current face matches any of the known faces
                        #  if True in matches:
                        # # find the index of the first match and use it to get the name of the employee
                        #         first_match_index = matches.index(True)
                        #         name = self.known_face_names[first_match_index]
                        #         recognized_namelist.append(name)
                        #         name_count +1
                        #         if collections.Counter(recognized_namelist):
                        #           print('Employee already recognized: {}'.format(name))
                        #           found = True
                        #         else :
                        #             print('New employee recognized: {}'.format(name))
                                
                        # # #do something with the recognized employee, such as displaying their name or logging their presence
                        # if not self.employee_recognized :
                        #     if db.records.count_documents({'Name': name}) > 0 and time.time()+ session_duration > exp_time:
                        #             print('Employee already recognized: {}'.format(name))
                        #             break
                        #             # do something with the existing employee, such as updating their information
                        #     else:
                        #             print('New employee recognized: {}'.format(name))
                        #         # print("Employee recognized: {}".format(name))
                        #             self.employee_recognized =True
                                    
                        
                        # # else:
                        # #         self.employee_recognized = False
                                
                # Add the emotion label to the image
                    
                        result = DeepFace.analyze(frame,actions="emotion",enforce_detection=False)
                        dominant_emotion = result[0]['dominant_emotion']
                        print(dominant_emotion)
                        #insert into db
                        if name != 'Unknown':
                        
                        
                        
                         add_data(name,current_time,dominant_emotion)
                        
                    
                    
                        cv2.putText(frame,dominant_emotion,(left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)    
                    
                        emotion_list.append(dominant_emotion)
                        # Increment the emotion counter
                    emotion_count += 1
                    

                    # Display the resulting image
                    cv2.imshow('Face Recognition', frame)

                    # Hit 'q' on the keyboard to quit!
                    if cv2.waitKey(1) & 0xff == ord('q'):
                            break
                    if emotion_count >= 10 :
                        break
                avg_emotion = collections.Counter(emotion_list).most_common(1)[0][0]
                #check()
                    
                # def check(): 
                #          # check if the current face matches any of the known faces
                #         if len(detectedNameList)> 1: # ensuring that the condition only happen after 2nd face matche
                #             if item in detectedNameList: 
                #                 if currenSectionTime+datetime.timedelta(minutes =15)<=current_time:
                #                     add_data(name,current_time,avg_emotion)
                                    
                #                 else:
                #                     print('Employee already recognized: '+item) 
                #                     add_data(current_time,avg_emotion)                 
                #                     # do something with the recognized employee, such as displaying their name or logging their presence                 
                #             else:
                #                 add_data(name,current_time,avg_emotion)
                #         else:
                #             add_data(name,current_time,avg_emotion)
                    
                #         print(detectedNameList)   
                        #check()       
            
            

            

            
                # Release handle to the webcam
                video_capture.release()
                cv2.destroyAllWindows()
                
                


                if __name__ == '__main__':
                        fr = FaceRecognition()
                        fr.run_recognition()

          return HttpResponse('success')
		 
		 

