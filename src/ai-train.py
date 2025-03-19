import face_recognition
import cv2
import numpy as np
import os

# Parameters
input_image_paths = ["group.png"]  # List of image paths
min_width, min_height = 100, 100  # Minimum face dimensions

def process_images(image_paths):
    """
    Process only faces that meet size criteria and generate encodings.
    Returns encodings and labels for faces larger than the defined thresholds.
    """
    encodings = []
    labels = []

    for image_path in image_paths:
        # Load the image
        image = face_recognition.load_image_file(image_path)
        face_locations = face_recognition.face_locations(image)
        face_landmarks_list = face_recognition.face_landmarks(image)

        # Initialize OpenCV for visualization
        image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Directory for saving cropped faces
        output_dir = "processed_faces"
        os.makedirs(output_dir, exist_ok=True)

        for i, ((top, right, bottom, left), landmarks) in enumerate(zip(face_locations, face_landmarks_list)):
            # Calculate dimensions of the detected face
            face_width = right - left
            face_height = bottom - top

            # Skip faces that are smaller than the thresholds
            if face_width < min_width or face_height < min_height:
                print(f"Face {i + 1} in {image_path} is too small, skipping...")
                continue

            # Visualize landmarks and save the cropped face
            for feature, points in landmarks.items():
                for point in points:
                    cv2.circle(image_bgr, point, 2, (0, 255, 0), -1)

            # Save the cropped face to a file
            cropped_face = image[top:bottom, left:right]
            cropped_face_path = os.path.join(output_dir, f"face_{i + 1}.png")
            cv2.imwrite(cropped_face_path, cropped_face)
            print(f"  -> Processed and saved face {i + 1} to '{cropped_face_path}'.")

            # Generate face encoding
            encoding = face_recognition.face_encodings(image, known_face_locations=[(top, right, bottom, left)])
            if encoding:
                encodings.append(encoding[0])  # Add the encoding
                label = input(f"Enter a label for face {i + 1} in {image_path}: ")  # Interactive labeling
                labels.append(label)

        # Save the image with landmarks drawn on it
        output_path = f"{image_path.split('.')[0]}_landmarks_output.png"
        cv2.imwrite(output_path, image_bgr)
        print(f"Image with landmarks saved as '{output_path}'")

    return encodings, labels

def train_and_evaluate(encodings, labels):
    """
    Train a KNN model and evaluate it.
    """
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.metrics import classification_report, accuracy_score

    model = KNeighborsClassifier(n_neighbors=5, metric="manhattan")
    model.fit(encodings, labels)
    print("\nModel training completed.")

    # Optionally validate with a portion of the training data (for demonstration purposes)
    predictions = model.predict(encodings)
    print("\nValidation Results:")
    print(classification_report(labels, predictions))
    print(f"Accuracy: {accuracy_score(labels, predictions) * 100:.2f}%")

if __name__ == "__main__":
    # Process images and extract encodings
    face_encodings, face_labels = process_images(input_image_paths)

    # Train and evaluate the model
    if face_encodings and face_labels:
        train_and_evaluate(face_encodings, face_labels)
    else:
        print("No valid faces detected for training.")
