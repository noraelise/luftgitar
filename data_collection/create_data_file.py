import csv
import os

from sample_images import sample_images_from_videos_in_folder
from calculate_data_points import calculate_data_in_image

def add_to_csv(output_file: str, data_points: list):
    with open(output_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data_points)
        file.close()


def create_csv(output_file: str):
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['right_elbow_angle', 'left_elbow_angle',
                         'dist_rhand_waist', 'dist_lhand_waist',
                         'height_right_wrist', 'height_left_wrist',
                         'distance_between_wrists', 'angle_left_underarm'])
        file.close()

    print("CSV file with header created successfully!")


# ======================================================================================

# First: Sample images from the videos in the guitar_videos folder and add output images to guitar_images
sample_images_from_videos_in_folder('guitar_videos', 'guitar_images', 20)
#sample_images_from_videos_in_folder('../guitar_stats', 'guitar_images', 20)

# Second: Create the csv-file
output_csv = 'data/air_guitar.csv'
create_csv(output_csv)

# Third: Iterate through the images in the guitar_images folder, calculate and add the data to the csv-file
for filename in os.listdir('guitar_images'):
    image_path = os.path.join('guitar_images', filename)
    data_points = calculate_data_in_image(image_path)
    add_to_csv(output_csv, data_points)