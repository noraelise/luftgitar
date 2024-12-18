from mediapipe.framework.formats import landmark_pb2
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from utilities.calculate_features import calculate_features
from utilities.logic import playing_air_guitar

class AirGuitarPoseDetector:
    def __init__(self, model_path, result_callback):
        self.guitar_detected = False
        self.last_pose_detected = False
        self.guitar_pose = 0
        self.no_guitar_pose = 0

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

            features = calculate_features(landmarks)

            self.last_pose_detected = self.guitar_detected
            self.guitar_detected = playing_air_guitar(features)

        except IndexError:
            print("Unable to detect pose at", timestamp_ms)

    def reset_counters(self):
        self.guitar_pose = 0
        self.no_guitar_pose = 0

    def update_stability(self):
        if self.last_pose_detected != self.guitar_detected:
            # A new guitar pose has been detected
            self.reset_counters()

        if self.guitar_detected:
            self.guitar_pose += 1
        else:
            self.no_guitar_pose += 1

    def stable_guitar_pose(self):
        if self.guitar_pose >= 1:
            self.reset_counters()
            return True
        return False

    def stable_no_guitar_pose(self):
        if self.no_guitar_pose >= 3:
            self.reset_counters()
            return True
        return False