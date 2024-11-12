import cv2
import mediapipe as mp
import data_collection.calculation_utilities as cu

from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.framework.formats import landmark_pb2

joints = {
    "left shoulder": 0,
    "right shoulder": 1,
    "left elbow": 2,
    "right elbow": 3,
    "left wrist": 4,
    "right wrist": 5,
    "left pinky": 6,
    "right pinky": 7,
    "left index": 8,
    "right index": 9,
    "left thumb": 10,
    "right thumb": 11,
    "left hip": 12,
    "right hip": 13
}


def collect_landmarks(filename):
    landmarks = []

    base_options = python.BaseOptions(model_asset_path='../models/pose_landmarker_lite.task')
    options = vision.PoseLandmarkerOptions(
        base_options=base_options,
        output_segmentation_masks=False) # Looking at segmentation masks may also be a solution

    detector = vision.PoseLandmarker.create_from_options(options)

    img = cv2.imread(filename)
    if img is None:
        print("Unable to open image:", filename)
        return ValueError

    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img)
    detection_result = detector.detect(mp_image)

    try:
        pose_landmarks_list = detection_result.pose_landmarks[0] # Index zero as we are only detecting one pose
        # in each image (for now). Should be general.
        for landmark in pose_landmarks_list[11:25]: # Trying first to only focus on the upper body with hands, hence [11:25].
            landmarks.append(landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y)) #Normalized

        print("Successfully collected landmarks from", filename)

    except IndexError:
        print("Unable to detect pose in", filename)

    return landmarks


def calculate_data_points(landmarks):
    data_points = []

    try:
        right_elbow_angle = cu.angle(landmarks[joints["right wrist"]],
                                     landmarks[joints["right elbow"]],
                                     landmarks[joints["right shoulder"]])

        left_elbow_angle = cu.angle(landmarks[joints["left wrist"]],
                                    landmarks[joints["left elbow"]],
                                    landmarks[joints["left shoulder"]])

        dist_rhand_waist = cu.distance_from_point_to_line(landmarks[joints["right wrist"]],
                                                          landmarks[joints["right shoulder"]],
                                                          landmarks[joints["right hip"]])

        dist_lhand_waist = cu.distance_from_point_to_line(landmarks[joints["left wrist"]],
                                                          landmarks[joints["left shoulder"]],
                                                          landmarks[joints["left hip"]])

        height_right_wrist = landmarks[joints["right wrist"]].y
        height_left_wrist = landmarks[joints["left wrist"]].y

        distance_between_wrists = cu.distance_between_two_points(landmarks[joints["right wrist"]],
                                                                 landmarks[joints["left wrist"]])

        angle_left_underarm = cu.angle_of_line(landmarks[joints["left wrist"]], landmarks[joints["left elbow"]])

        data_points.append(right_elbow_angle)
        data_points.append(left_elbow_angle)
        data_points.append(dist_rhand_waist)
        data_points.append(dist_lhand_waist)
        data_points.append(height_right_wrist)
        data_points.append(height_left_wrist)
        data_points.append(distance_between_wrists)
        data_points.append(abs(angle_left_underarm))
    except IndexError:
        data_points.append('IndexError')

    return data_points

def calculate_data_in_image(filename):
    landmarks = collect_landmarks(filename)
    data_points = calculate_data_points(landmarks)

    return data_points