
def playing_air_guitar(data_points) -> bool:
    (right_elbow_angle, left_elbow_angle,
     dist_rhand_waist, dist_lhand_waist,
     height_right_wrist, height_left_wrist) = data_points

    if ((30 < right_elbow_angle < 140)      and (30 < left_elbow_angle < 180) and
        (0 < dist_rhand_waist < 0.08)       and (0 < dist_lhand_waist < 0.2) and
        (0.35 < height_right_wrist < 0.65)  and (0.3 < height_left_wrist < 0.63)):
        return True
    return False