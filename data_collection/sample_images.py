import cv2
import os
import random


def sample_images_from_videos_in_folder(input_folder: str, output_folder: str, sample_percentage: float):
    for filename in os.listdir(input_folder):
        sample_images_from_video(os.path.join(input_folder, filename), output_folder, sample_percentage)
        print("Successfully extracted images from", filename)


def sample_images_from_video(filename: str, output_folder: str, sample_percentage):
    cap = cv2.VideoCapture(filename)

    if not cap.isOpened():
        print("Error in opening video file.")

    # Remove video format from filename
    filename = filename.replace(".mp4", "")
    # Remove parent folder name
    filename = filename.split("/")[1]

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    sample_percentage *= 0.01
    step = int(1/sample_percentage)

    for i in range(0, total_frames, step):
        random_frame = random.randint(i, i+step)

        cap.set(cv2.CAP_PROP_POS_FRAMES, random_frame)
        success, frame = cap.read()
        if success:
            img_name = output_folder + "/" + filename + "_" + str(random_frame) + ".jpg"
            cv2.imwrite(img_name, frame)
