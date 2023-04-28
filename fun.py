import cv2
import time


def capture_emotions(interval, max_emotions):
    """Captures up to max_emotions emotions at regular intervals of interval seconds"""
    
    # Initialize the camera
    cap = cv2.VideoCapture(0)
  # Read and display video frames

    emotions_captured = 0
    
    while emotions_captured < max_emotions:
        
        # Wait for the specified interval
        time.sleep(2000)
        
    ret, frame = cap.read()
    f.open()
    file  = "emotion_capture_" + str(emotions_captured) + ".jpg"
    cv2.imwrite(file, frame)
        
    emotions_captured += 1
    # Display the captured frame
    cv2.imshow("Webcam", frame)
    
    # Wait for 1 millisecond and check if the 'q' key is pressed to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        sys.exit()

capture_emotions(10, 5) # Captures up to 5 emotions every 10 seconds

cap.release()
cv2.destroyAllWindows()
