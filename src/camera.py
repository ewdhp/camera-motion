import cv2

class Camera:
    def __init__(self):
        self.capture = cv2.VideoCapture(0)

    def start_capture(self):
        if not self.capture.isOpened():
            raise Exception("Could not open video device")

    def get_frame(self):
        ret, frame = self.capture.read()
        if not ret:
            raise Exception("Could not read frame")
        return frame

    def release(self):
        self.capture.release()