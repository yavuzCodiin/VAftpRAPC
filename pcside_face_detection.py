import cv2 as cv
import os
import time

# Used Haar Cascade Frontal Face Default to detect people from their frontal face
face_cascade = cv.CascadeClassifier(r'haarcascade_frontalface_default.xml') # Face detection
body_cascade = cv.CascadeClassifier(r'haarcascade_fullbody.xml')  # Body detection

# FTP Server Directory as Image Directory
image_dir = r''

try:
    while True:
        # Counting frames to send output to the embedded system
        # when the conditions are suitable to open the door
        face_count = 0
        body_count = 0  # Added body count

        # Taking frame from its directory and puts into the process
        for filename in os.listdir(image_dir):

            # Reading the image
            img = cv.imread(os.path.join(image_dir, filename))
            if img is None:
                print(f'Failed to load {filename}')
                continue

            # Converting BGR image to the grayscale
            gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

            # Defining scaleFactor and minNeighbors parameters
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            bodies = body_cascade.detectMultiScale(gray, 1.1, 4)  # Added body detection

            # Illustrating the detected face and body by using blue and green rectangles
            for (x, y, w, h) in faces:
                cv.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
                face_count += 1

            for (x, y, w, h) in bodies:
                cv.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                body_count += 1

            # Showing image
            cv.imshow('person', img)
            cv.waitKey(1500)
            cv.destroyAllWindows()

        # For reading and writing text file through the FTP Server
        if face_count >= 13 or body_count >= 13:  # Updated condition to check both face and body count
            with open(r'on.txt', 'w') as f:
                pass
            print(f'{face_count} faces and {body_count} bodies detected. Output is 1.')


        else:
            with open(r'off.txt', 'w') as f:
                pass
            print(f'{face_count} face(s) and {body_count} body(ies) detected. Output is 0')


        #time.sleep(1)  # wait for 1 second before checking the directory again

except KeyboardInterrupt:
    print("Stopped by User")
