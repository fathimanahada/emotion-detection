import time
import cv2

def set_emotion_capture_timer(seconds):
    """Sets a timer for capturing emotion with a camera after a specified number of seconds"""
    
    # Wait for the specified number of seconds
    time.sleep(seconds)
    
    # Initialize the camera
cap = cv2.VideoCapture(0)
    
while True:
    # Capture an image from the camera
      ret, frame = cap.read()

      
      
      #cv2.putText(frame,(top, right-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
      for (x, y, w, h) in frame:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
       #Save the captured image
      #cv2.imwrite("emotion_capture.jpg", frame)
      cv2.imshow('face recognition',frame)

      if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    # Release the camera
      cap.release()
      cv2.destroyAllWindows()
