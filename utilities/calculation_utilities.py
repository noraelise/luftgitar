import numpy as np

# Calculates angle between two lines
def angle(pt1, pt2, pt3):
    # calculate the direction vectors
    v1 = np.array([pt2.x-pt1.x, pt2.y-pt1.y])
    v2 = np.array([pt3.x-pt2.x, pt3.y-pt2.y])

    # dot product and magnitude
    v12_dot = v1.dot(v2)
    v1_mag = np.linalg.norm(v1)
    v2_mag = np.linalg.norm(v2)

    # inverse cosine
    theta = np.arccos(v12_dot/(v1_mag*v2_mag))

    return theta*(180/np.pi) # Convert to degrees

# Calculates the distance from a point pt0 to a line passing through pt1 and pt2
# https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line
def distance_from_point_to_line(pt0, pt1, pt2):

    nominator = np.abs((pt2.y-pt1.y)*pt0.x-(pt2.x-pt1.x)*pt0.y+pt2.x*pt1.y-pt2.y*pt1.x)
    denominator = np.sqrt((pt2.y-pt1.y)**2+(pt2.x-pt1.x)**2)

    return nominator/denominator

# Calculates angle of a single line in reference to a horizontal line
def angle_of_line(line_pt1, line_pt2):
    dx = line_pt2.x-line_pt1.x
    dy = line_pt2.y-line_pt1.y
    theta = (np.degrees(np.arctan2(dy, dx)))
    return theta

# Calculates the Euclidian distance between two points
def distance_between_two_points(pt1, pt2):

    x_dist = pt2.x-pt1.x
    y_dist = pt2.y-pt1.y
    dist = np.sqrt(x_dist**2+y_dist**2)

    return dist



