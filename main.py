import mediapipe as mp
from mediapipe.framework.formats import landmark_pb2
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
import time

from data_collection.calculate_data_points import calculate_data_points
from logic import playing_air_guitar

previous_cb_time = None # for cb_timing
guitar_detected = False

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

#cap = cv2.VideoCapture(1) # 1=webcam, 0=phone
cap = cv2.VideoCapture('test_videos/august.mp4')

if not cap.isOpened():
    print("Error in opening video file.")

# Read until video is completed
while (cap.isOpened()):
    ret, frame = cap.read()
    if not ret:
        print("Not able to capture frame.")
        break

    # Detect pose
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
    timestamp = int(cap.get(cv2.CAP_PROP_POS_MSEC))
    if timestamp > 0:
        detector.detect_async(mp_image, timestamp)

    # Signal detected guitar
    if guitar_detected:
        #name = 'test_videos/wrongly_classified/IMG_0257'+str(timestamp)+'.jpg'
        #cv2.imwrite(name, frame)
        print("Guitar detected at", timestamp)
    else:
        print("No guitar at", timestamp )

    cv2.imshow("Video", frame)

    # Press Q on keyboard to exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()