
def playing_air_guitar(data_points) -> bool:
    (right_elbow_angle, left_elbow_angle,
     dist_rhand_waist, dist_lhand_waist,
     height_right_wrist, height_left_wrist,
     distance_between_wrists, angle_left_underarm) = data_points

    if ((30 < right_elbow_angle < 150)          and (0 < left_elbow_angle < 170) and
        (0 < dist_rhand_waist < 0.08)           and (0 < dist_lhand_waist < 0.2) and
        #(0.05 < height_right_wrist < 0.180)      and (0 < height_left_wrist < 0.1) and
        (0.1 < distance_between_wrists < 0.38)  and (100 < abs(angle_left_underarm) < 180)):
        return True
    return False