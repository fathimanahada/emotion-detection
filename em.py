import cv2
from deepface import DeepFace

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
while True:
    ret,frame = cap.read()
    result = DeepFace.analyze(frame,actions="emotion",enforce_detection=False)
        
    
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray,1.1,4)
    
    
    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),3)
    
        dominant_emotion = result[0]['dominant_emotion']
        print(dominant_emotion)
        
        # Add the emotion label to the image
        cv2.putText(frame,str(dominant_emotion) ,(x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)

    cv2.imshow('frame',frame)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()