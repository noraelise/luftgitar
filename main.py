import mediapipe as mp
from mediapipe.framework.formats import landmark_pb2
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
import time
from music import MusicPlayer

from data_collection.calculate_data_points import calculate_data_points
from logic import playing_air_guitar

previous_cb_time = None # for cb_timing
guitar_detected = False
last_guitar_detected = False
music_playing = False

def cb_timing(result: mp.tasks.vision.PoseLandmarkerResult, output_image: mp.Image, timestamp_ms ):
    global previous_cb_time

    curr_time = time.time()

    # Calculate the time interval if there was a previous call
    if previous_cb_time is not None:
        interval = curr_time - previous_cb_time
        print(f"Time since last call: {interval:.4f} seconds")

    # Update the previous call time to the current time
    previous_cb_time = curr_time

def cb_detect_air_guitar(result: mp.tasks.vision.PoseLandmarkerResult, output_image: mp.Image, timestamp_ms ):
    landmarks = []
    try:
        pose_landmarks_list = result.pose_landmarks[0]  # Index zero as we are only detecting one pose
        # in each image (for now). Should be general.
        for landmark in pose_landmarks_list[11:25]:  # Trying first to only focus on the upper body with hands, hence [11:25].
            landmarks.append(landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y))  # Normalized

        data_points = calculate_data_points(landmarks)

        global guitar_detected
        global last_guitar_detected

        last_guitar_detected = guitar_detected
        guitar_detected = playing_air_guitar(data_points)

    except IndexError:
        print("Unable to detect pose at", timestamp_ms)


# =======================================================================================================

#BaseOptions = mp.tasks.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
VisionRunningMode = mp.tasks.vision.RunningMode

base_options = python.BaseOptions(model_asset_path='models/pose_landmarker_lite.task')
options = vision.PoseLandmarkerOptions(base_options=base_options,
                                       running_mode=VisionRunningMode.LIVE_STREAM,
                                       result_callback=cb_detect_air_guitar)

detector = PoseLandmarker.create_from_options(options)

# Example usage:
music_file = "music_tracks/smulik.mp3"  # Replace with your file path
player = MusicPlayer(music_file)

#qcap = cv2.VideoCapture(0)
cap = cv2.VideoCapture('test_videos/gitar_mobilkamera.MOV')
if not cap.isOpened():
    print("Error in opening video file.")

# Read until video is completed
timestamp = 0
num_frames = 0
stable_guitar_pose = 0
stable_no_guitar = 0
while (cap.isOpened()):
    ret, frame = cap.read()
    if not ret:
        print("Not able to capture frame.")
        cap.release()
        cv2.destroyAllWindows()
        break
    num_frames += 1

    # Detect pose
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
    timestamp = int(cap.get(cv2.CAP_PROP_POS_MSEC))
    if timestamp > 0:
        detector.detect_async(mp_image, timestamp)

    # Signal detected guitar
    if guitar_detected:
        if last_guitar_detected != guitar_detected:
            stable_guitar_pose = 0
            stable_no_guitar = 0
        stable_guitar_pose += 1
        print("Guitar detected at", timestamp)
    else:
        if last_guitar_detected != guitar_detected:
            stable_no_guitar = 0
            stable_guitar_pose = 0
        stable_no_guitar += 1
        print("No guitar at", timestamp)

    if music_playing and stable_no_guitar >= 10:
        stable_no_guitar = 0
        stable_guitar_pose = 0
        # Stop the music
        print("Stopping music playback.")
        player.stop()
        music_playing = False
    elif not music_playing and stable_guitar_pose >= 5:
        stable_no_guitar = 0
        stable_guitar_pose = 0
        # Start the music
        print("Starting music playback.")
        player.start()
        music_playing = True

    cv2.imshow("Video", frame)

    # Press Q on keyboard to exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()