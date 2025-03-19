import cv2
import numpy as np
from camera import Camera
from motion_detector import MotionDetector
from utils import save_video
import paramiko
import time
import threading
from queue import Queue
import pygame
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

def upload_to_vps(local_file, remote_file, hostname, port, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, port, username, password)
    sftp = ssh.open_sftp()
    sftp.put(local_file, remote_file)
    sftp.close()
    ssh.close()

def send_gmail_email(sender_email, sender_password, receiver_email, subject, body, attachment_path):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    attachment = open(attachment_path, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % attachment_path)
    msg.attach(part)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        print("Email sent successfully!")
        return True, "Email sent successfully!"
    except Exception as e:
        print(f"Error sending email: {e}")
        return False, f"Error sending email: {e}"

def play_alarm_sound():
    pygame.mixer.init()
    alarm_sound = pygame.mixer.Sound("alarm_sound.wav")
    alarm_sound.play(-1)  # Loop the sound indefinitely

def stop_alarm_sound():
    pygame.mixer.stop()

def start_monitoring():
    global monitoring
    monitoring = True
    threading.Thread(target=monitor).start()

def stop_monitoring():
    global monitoring
    monitoring = False

def monitor():
    camera = Camera()
    motion_detector = MotionDetector()
    
    # Start capturing video
    camera.start_capture()
    
    # Initialize variables for video recording
    recording = False
    out = None
    upload_counter = 0
    
    # Add a small delay to avoid false positives
    time.sleep(2)
    
    while monitoring:
        frame = camera.get_frame()
        if frame is None:
            break
        
        # Detect motion
        if motion_detector.detect_motion(frame):
            if not recording:
                recording = True
                upload_counter += 1
                local_filename = f"motion_recording_{upload_counter}.avi"
                remote_filename = f"/home/ewd2955/camera/rec_{upload_counter}.avi"
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                out = cv2.VideoWriter(local_filename, fourcc, 20.0, (frame.shape[1], frame.shape[0]))
                start_time = time.time()
                # Play alarm sound when recording starts
                threading.Thread(target=play_alarm_sound).start()
        
        # If recording, write the frame to the video file
        if recording:
            out.write(frame)
            # Stop recording after 1 second
            if time.time() - start_time >= 1:
                out.release()
                # Send email with the video file
                threading.Thread(target=send_gmail_email, args=(
                    "",
                    "",  # Your app password
                    "",
                    "Motion Detected",
                    "",
                    local_filename
                )).start()
                # Upload the video file
                threading.Thread(target=upload_to_vps, args=(
                    local_filename,
                    remote_filename,
                    "",
                    22,
                    "",
                    ""
                )).start()
                recording = False
                # Stop alarm sound when recording stops
                threading.Thread(target=stop_alarm_sound).start()
        
        # Put the frame in the queue for UI update
        frame_queue.put(frame)
    
    # Release resources
    camera.release()
    if recording:
        out.release()
    cv2.destroyAllWindows()

def update_video():
    if not frame_queue.empty():
        frame = frame_queue.get()
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=img)
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)
    video_label.after(10, update_video)

if __name__ == "__main__":
    monitoring = False
    frame_queue = Queue()

    # Create the main window
    root = tk.Tk()
    root.title("Motion Detection App")

    # Create and place the buttons
    start_button = tk.Button(root, text="Start Monitoring", command=start_monitoring)
    start_button.pack(pady=10)

    stop_button = tk.Button(root, text="Stop Monitoring", command=stop_monitoring)
    stop_button.pack(pady=10)

    # Create a label to display the video
    video_label = tk.Label(root)
    video_label.pack()

    # Start the video update loop
    update_video()

    # Run the Tkinter event loop
    root.mainloop()
