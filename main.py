import mediapipe as mp
from mediapipe.framework.formats import landmark_pb2
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
import time
from music import MusicPlayer

from data_collection.calculate_data_points import calculate_data_points
from logic import playing_air_guitar

# =======================================================================================================

guitar_detected = False
last_guitar_detected = False
music_playing = False

# Read until video is completed
num_frames = 0
stable_guitar_pose = 0
stable_no_guitar = 0

# =======================================================================================================

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

def reset_pose_counters():
    global stable_guitar_pose
    global stable_no_guitar
    stable_guitar_pose = 0
    stable_no_guitar = 0

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

#cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture('test_videos/IMG_0664.MOV')
if not cap.isOpened():
    print("Error in opening video file.")

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
    #timestamp = int(cap.get(cv2.CAP_PROP_POS_MSEC))
    detector.detect_async(mp_image, num_frames)

    # Signal detected guitar
    if guitar_detected:
        if last_guitar_detected != guitar_detected:
            reset_pose_counters()
        stable_guitar_pose += 1
        print("Guitar detected at", num_frames)
    else:
        if last_guitar_detected != guitar_detected:
            reset_pose_counters()
        stable_no_guitar += 1
        print("No guitar at", num_frames)

    if music_playing and stable_no_guitar >= 8:
        # Stop the music
        player.stop_thread()
        print("Stopping music playback.")
        music_playing = False
        reset_pose_counters()
    elif not music_playing and stable_guitar_pose >= 4:
        # Start the music
        player.start_thread()
        print("Starting music playback.")
        music_playing = True
        reset_pose_counters()

    cv2.imshow("Video", frame)

    # Press Q on keyboard to exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()