import mediapipe as mp
import cv2
from music import MusicPlayer
from pose_detector import AirGuitarPoseDetector

# Music player initialization
music_file = "music_tracks/smulik.mp3"
player = MusicPlayer(music_file)

# Callback function for air guitar detection
def cb_detect_air_guitar(result, output_image, timestamp_ms):
    detector.process_detection_result(result, timestamp_ms)

# Initialize pose detector with model path and callback
detector = AirGuitarPoseDetector(model_path='models/pose_landmarker_lite.task',
                                 result_callback=cb_detect_air_guitar)

# Video capture initialization
cap = cv2.VideoCapture('test_videos/IMG_0664.MOV')
if not cap.isOpened():
    print("Error in opening video file.")

num_frames = 0
# Main loop
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Not able to capture frame.")
        cap.release()
        cv2.destroyAllWindows()
        break
    num_frames += 1

    # Detect pose
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
    detector.detect_async(mp_image, num_frames)

    # Update pose stability counters
    detector.update_stability()

    # Handle music playback based on detection
    if player.is_playing and detector.stable_no_guitar >= 8:
        # Stop the music
        player.stop_thread()
        print("Stopping music playback.")
        detector.reset_counters()
    elif not player.is_playing and detector.stable_guitar_pose >= 4:  # Higher sensitivity for guitar pose
        # Start the music
        player.start_thread()
        print("Starting music playback.")
        detector.reset_counters()

    cv2.imshow("Video", frame)

    # Press Q on keyboard to exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
