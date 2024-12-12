import mediapipe as mp
import cv2
from music import MusicPlayer
from pose_detector import AirGuitarPoseDetector

# The music_player initialization
music_file = "music_tracks/smulik.mp3"
music_player = MusicPlayer(music_file)

# Callback function for air guitar detection
def cb_detect_air_guitar(result, output_image, timestamp_ms):
    detector.process_detection_result(result, timestamp_ms)

# Initialize pose detector with model path and callback
detector = AirGuitarPoseDetector(model_path='models/pose_landmarker_lite.task',
                                 result_callback=cb_detect_air_guitar)

# Video capture initialization
#cap = cv2.VideoCapture('test_videos/IMG_0664.MOV')
cap = cv2.VideoCapture(1)
if not cap.isOpened():
    print("Error in opening video file.")

num_frames = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Not able to capture frame.")
        break
    num_frames += 1

    # Detect pose
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
    detector.detect_async(mp_image, num_frames)

    # Update pose stability counters
    detector.update_stability()

    # Check if an air guitar pose has been detected
    if not music_player.is_playing and detector.stable_guitar_pose():
        # Start the music
        music_player.play_music()
        detector.reset_counters()
    elif music_player.is_playing and detector.stable_no_guitar_pose():
        # Stop the music
        music_player.stop_music()
        detector.reset_counters()

    cv2.imshow("LIVE_STREAM", frame)

    # Press Q on keyboard to exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
