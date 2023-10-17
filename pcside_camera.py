import cv2

# Load the cascade classifier
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Set up the video capture
capture = cv2.VideoCapture(0)

while True:
    # Read the frame
    _, frame = capture.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 6)

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    # Display the frame
    cv2.imshow('Frame', frame)

    # Check if the user pressed the 'q' key
    if cv2.waitKey(1) == ord('q'):
        break

# Release the video capture
capture.release()

# Destroy the windows
cv2.destroyAllWindows()

