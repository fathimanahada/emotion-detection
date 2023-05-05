import cv2
from deepface import DeepFace
import time
from datetime import datetime
import collections

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
f = open('emotion_labels.txt', 'a')

# Record the start time
start_time = time.time()

# Initialize the emotion counter
emotion_count = 0
emotion_list = []

while True:
    current_time = datetime.now().strftime('%Y-%m-%d  %I:%M:%S')
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray,1.1,4)

    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),3)
        
        # Analyze the emotion using DeepFace
        result = DeepFace.analyze(frame,actions="emotion",enforce_detection=False)
        dominant_emotion = result[0]['dominant_emotion']
        print(dominant_emotion)
        data= current_time+': '+dominant_emotion
        #Add data to the file
        f.write(data+'\n')
        # Add the emotion label to the image
        cv2.putText(frame,str(dominant_emotion) ,(x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)

        # Add the emotion to the list
        emotion_list.append(dominant_emotion)

        # Increment the emotion counter
        emotion_count += 1
        
        # Check if 5 emotions have been detected or 15 minutes have elapsed
        elapsed_time = time.time() - start_time
        if emotion_count >= 10 or elapsed_time >= 60:
        #if emotion_count >=10 :
            break
    
    cv2.imshow('frame',frame)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break
        
    # Check if 5 emotions have been detected or 15 minutes have elapsed
    elapsed_time = time.time() - start_time
    #if emotion_count >= 10 :
    if emotion_count >= 10 or elapsed_time >= 60:
        break
avg_emotion = collections.Counter(emotion_list).most_common(1)[0][0]
print("Average Emotion:", avg_emotion)
f.write("Average Emotion: " + str(avg_emotion) + "\n")

cap.release()
cv2.destroyAllWindows()
f.close()

# avg_emotion = collections.Counter(emotion_list).most_common(1)[0][0]
# print("Average Emotion:", avg_emotion)