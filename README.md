# Motion Detection Application

This project is a motion detection application that captures video from a camera and records it when significant movement is detected. It utilizes OpenCV for video processing and includes a simple interface for users to interact with the application.

## Project Structure

```
motion-detection-app
├── src
│   ├── main.py          # Entry point of the application
│   ├── camera.py        # Camera management
│   ├── motion_detector.py # Motion detection logic
│   └── utils.py         # Utility functions
├── requirements.txt     # Project dependencies
└── README.md            # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/motion-detection-app.git
   cd motion-detection-app
   ```

2. **Install the required dependencies:**
   Make sure you have Python installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

## Usage Guidelines

1. **Run the application:**
   To start the motion detection application, execute the following command:
   ```bash
   python src/main.py
   ```

2. **Adjust camera settings:**
   You may need to adjust the camera settings in `src/camera.py` if you encounter issues with video capture.

3. **Recording:**
   The application will automatically start recording when motion is detected. The recorded video will be saved in the project directory.

## Functionality Overview

- **Camera Management:** The application captures video from the camera using the `Camera` class in `src/camera.py`.
- **Motion Detection:** The `MotionDetector` class in `src/motion_detector.py` analyzes video frames to detect significant movement.
- **Video Recording:** When motion is detected, the application records the video using utility functions defined in `src/utils.py`.

## Contributing

Feel free to submit issues or pull requests if you would like to contribute to the project.