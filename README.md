# Repository Overview for Project "Strumming the Air: Real-Time Air Guitar Detection and Audio Feedback"

## Data
### data_collection
- create_data_file.py: Script to generate .csv-files.
- sample_images.py: Script to sample images from videos explained in subsection 4.3.2.

### data_plotting
- plotting.py: Script for plotting histograms from .csv-files.

## The Application
### utilities
- calculate_features.py: Script for calculating the selected features explained in section 4.4.
- calculation_utilities.py: Implementation of geometrical calculations explained in section 3.4.
- logic.py: Contains the function playing_air_guitar() referenced in 4.4.

### main.py
The initialization of the necessary modules and the main while loop of the system. See section 4.2.

### music.py
The module is described in section 4.5.

### pose_detector.py
The full implementation of the AirGuitarDetector class, explained in section 4.4.
