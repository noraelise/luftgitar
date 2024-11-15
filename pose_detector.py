from mediapipe.framework.formats import landmark_pb2
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from data_collection.calculate_data_points import calculate_data_points
from logic import playing_air_guitar

class AirGuitarPoseDetector:
    def __init__(self, model_path, result_callback):
        self.guitar_detected = False
        self.last_guitar_detected = False
        self.stable_guitar_pose = 0
        self.stable_no_guitar = 0

        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.PoseLandmarkerOptions(base_options=base_options,
                                               running_mode=vision.RunningMode.LIVE_STREAM,
                                               result_callback=result_callback)
        self.detector = vision.PoseLandmarker.create_from_options(options)

    def detect_async(self, image, timestamp):
        self.detector.detect_async(image, timestamp)

    def process_detection_result(self, result, timestamp_ms):
        landmarks = []
        try:
            pose_landmarks_list = result.pose_landmarks[0]  # Only one pose detected
            for landmark in pose_landmarks_list[11:25]:  # Focus on upper body landmarks
                landmarks.append(landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y))

            data_points = calculate_data_points(landmarks)

            self.last_guitar_detected = self.guitar_detected
            self.guitar_detected = playing_air_guitar(data_points)

        except IndexError:
            print("Unable to detect pose at", timestamp_ms)

    def reset_counters(self):
        self.stable_guitar_pose = 0
        self.stable_no_guitar = 0

    def update_stability(self):
        if self.guitar_detected:
            if self.last_guitar_detected != self.guitar_detected:
                # A new guitar pose has been detected
                self.reset_counters()
            self.stable_guitar_pose += 1
        else:
            if self.last_guitar_detected != self.guitar_detected:
                # A new no guitar pose has been detected
                self.reset_counters()
            self.stable_no_guitar += 1
