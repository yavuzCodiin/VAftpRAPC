import ftplib
import os
import socket
import time
import cv2

def send_frames():
    ftp = ftplib.FTP('192.168.1.2')
    ftp.login('ftp-user', '1327')
    ftp.set_pasv(True)
    ftp.set_debuglevel(2)
    ftp.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    ftp.sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    ftp.sock.setsockopt(socket.SOL_TCP, socket.TCP_KEEPIDLE, 300)
    ftp.sock.setsockopt(socket.SOL_TCP, socket.TCP_KEEPINTVL, 60)
    ftp.sock.setsockopt(socket.SOL_TCP, socket.TCP_KEEPCNT, 5)

    for file in os.listdir('frames'):
        with open(os.path.join('frames', file), 'rb') as f:
            ftp.storbinary('STOR {}'.format(file), f, blocksize=65536)
        os.remove(os.path.join('frames', file))  # Delete the file after sending

    ftp.quit()


def capture_new_frames():
    cap = cv2.VideoCapture(0)  # Use the first available camera (index 0)

    # Calculate the time interval between capturing each frame
    num_frames = 15
    time_interval = 3.0 / num_frames

    for i in range(num_frames):
        ret, frame = cap.read()
        if ret:
            frame_file = os.path.join('frames', f'frame{i:03d}.jpg')
            cv2.imwrite(frame_file, frame)
            time.sleep(time_interval)
        else:
            print("Error capturing frame")

    cap.release()


while True:
    capture_new_frames()
    send_frames()
    time.sleep(5)  # Wait for 5 seconds before repeating the process