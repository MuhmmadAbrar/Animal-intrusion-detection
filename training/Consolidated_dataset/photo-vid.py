import cv2
import os
import re

# Function to sort file names numerically
def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split('(\d+)', s)]

def convert_photos_to_video(photo_folder, output_path, fps):
    # Get the list of JPG photos in the folder
    photo_files = sorted(
        [file for file in os.listdir(photo_folder) if file.lower().endswith('.jpg')],
        key=natural_sort_key
    )

    if not photo_files:
        print("No JPG photos found in the folder.")
        return

    # Read the first image to get dimensions
    img = cv2.imread(os.path.join(photo_folder, photo_files[0]))
    height, width, _ = img.shape

    # Create a VideoWriter object to save the video
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # Change codec as per your requirement
    video = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # Convert photos to video frames
    for photo_file in photo_files:
        photo_path = os.path.join(photo_folder, photo_file)
        img = cv2.imread(photo_path)

        # Add the frame to the video
        video.write(img)

    # Release the video writer and close the file
    video.release()

# Usage example
photo_folder = "D:/SEMESTER 5/IOT/PROJECT/dataset-github/Animal-intrusion-detection/Consolidated_dataset/train"  # Replace with your photo folder path
output_path = "D:/SEMESTER 5/IOT/PROJECT/dataset-github/Animal-intrusion-detection/Consolidated_dataset/video24fps.mp4"  # Replace with your desired output path
fps = 24  # Set the desired frame rate

convert_photos_to_video(photo_folder, output_path, fps)
