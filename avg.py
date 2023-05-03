import cv2
from deepface import DeepFace
import collections

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
f = open('emotion_labels.txt', 'a')


# Initialize the emotion counter and the list of emotions
emotion_count = 0
emotion_list = []

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray,1.1,4)

    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),3)
        
        # Analyze the emotion using DeepFace
        result = DeepFace.analyze(frame,actions="emotion",enforce_detection=False)
        dominant_emotion = result[0]['dominant_emotion']
        data= current_time+': '+dominant_emotion
        #Add data to the file
        f.write(data+'\n')
        
        # Add the emotion to the list
        emotion_list.append(dominant_emotion)
        
        # Increment the emotion counter
        emotion_count += 1
        
        # Check if 10 emotions have been detected
        if emotion_count >= 10:
            break
    
    cv2.imshow('frame',frame)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break
        
    # Check if 10 emotions have been detected
    if emotion_count >= 10:
       break

avg_emotion = collections.Counter(emotion_list).most_common(1)[0][0]
print("Average Emotion:", avg_emotion)
f.write("Average Emotion: " + str(avg_emotion) + "\n")


cap.release()
cv2.destroyAllWindows()
f.close()

# Calculate the most frequent emotion from the list
# avg_emotion = collections.Counter(emotion_list).most_common(1)[0][0]
# print("Average Emotion:", avg_emotion)
