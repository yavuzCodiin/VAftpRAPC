import ftplib              #Library for FTP 
import os                  #Library for Operating System 
import socket              #Library for Network Communication 
import time                #Library for Time 
import cv2                 #Library for Computer Vision
import RPi.GPIO as GPIO    #Library for Raspberry Pi GPIO 

GPIO.setmode(GPIO.BCM) #setting GPIO Mode
GPIO.setwarnings(False) # Suppress GPIO warnings

#Define pin numbers for the motor
PIN1 = 24
PIN2 = 23

#Set up the GPIO pins for output
GPIO.setup(PIN1, GPIO.OUT)
GPIO.setup(PIN2, GPIO.OUT)



def send_frames():
    # FTP connection setup
    ftp = ftplib.FTP('')
    ftp.login('username', 'password')
    # FTP settings for better performance and reliability
    ftp.set_pasv(True)
    ftp.set_debuglevel(2)
    ftp.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    ftp.sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    ftp.sock.setsockopt(socket.SOL_TCP, socket.TCP_KEEPIDLE, 300)
    ftp.sock.setsockopt(socket.SOL_TCP, socket.TCP_KEEPINTVL, 60)
    ftp.sock.setsockopt(socket.SOL_TCP, socket.TCP_KEEPCNT, 5)
    # FTP commands to send frames 
    for file in os.listdir('frames'):
        with open(os.path.join('frames', file), 'rb') as f:
            ftp.storbinary('STOR {}'.format(file), f, blocksize=65536)
        os.remove(os.path.join('frames', file))  # Delete the file after sending

    ftp.quit()


def capture_new_frames():
    cap = cv2.VideoCapture(0)  # Use the first available camera (index 0)

    # Calculate the time interval between capturing each frame
    num_frames = 6
    time_interval = 3.0 / num_frames
    # Capture frames and save them to 'frames' directory
    for i in range(num_frames):
        ret, frame = cap.read()
        if ret:
            frame_file = os.path.join('frames', f'frame{i:03d}.jpg')
            cv2.imwrite(frame_file, frame)
            time.sleep(time_interval) #Wait for the specified time interval
        else:
            print("Error capturing frame")

    cap.release()


def check_file():
    # FTP connection setup
    ftp = ftplib.FTP('')
    ftp.login('username', 'password')
    # FTP settings for better performance and reliability
    ftp.set_pasv(True)
    ftp.set_debuglevel(2)
    ftp.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    ftp.sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    ftp.sock.setsockopt(socket.SOL_TCP, socket.TCP_KEEPIDLE, 300)
    ftp.sock.setsockopt(socket.SOL_TCP, socket.TCP_KEEPINTVL, 60)
    ftp.sock.setsockopt(socket.SOL_TCP, socket.TCP_KEEPCNT, 5)
    # Check for specific files on the FTP server
    files = ftp.nlst()
    if 'on.txt' in files:
        open_door()
        print("Door is opening")
        time.sleep(1)
        ftp.delete("on.txt") # Delete the file after processing

    elif 'off.txt' in files:
        close_door()
        print("Door is closing")
        time.sleep(1)
        ftp.delete("off.txt") # Delete the file after processing

    ftp.quit()


def open_door():
    # Control the motor to open the door
    GPIO.output(PIN1, GPIO.HIGH) 
    GPIO.output(PIN2, GPIO.LOW)
    time.sleep(1.6)
    stop_door()
    time.sleep(10)
    close_door() # Close the door after 10 seconds

def close_door():
    # Control the motor to close the door
    GPIO.output(PIN1, GPIO.LOW)
    GPIO.output(PIN2, GPIO.HIGH)
    time.sleep(1.6)
    stop_door()

def stop_door():
    # Stop the motor
    GPIO.output(PIN1, GPIO.LOW)
    GPIO.output(PIN2, GPIO.LOW)


while True:
    check_file()
    capture_new_frames()
    send_frames()
    time.sleep(5)  # Wait for 5 seconds before repeat

# Clean up GPIO channels
GPIO.cleanup()
