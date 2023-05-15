# Ratio utility functions

import math

def euclidean_distance(point1, point2) -> float:
	"""
    Calculates the Euclidean distance between two points in 2D space.

    Args:
        point1 (tuple): The coordinates of the first point as a tuple of (x, y) values.
        point2 (tuple): The coordinates of the second point as a tuple of (x, y) values.

    Returns:
        float: The Euclidean distance between the two points.

    Raises:
        None.

    Example usage:
        # Define two points
        point1 = (0, 0)
        point2 = (3, 4)

        # Calculate Euclidean distance
        distance = euclidean_distance(point1, point2)
        print("Euclidean distance between point1 and point2: ", distance)

    Note:
        - The function uses the formula for Euclidean distance, which is the square root of the sum of the squared differences
          in x and y coordinates between the two points.
        - The point1 and point2 parameters should be tuples of (x, y) values, where x is the horizontal coordinate and y is the
          vertical coordinate.
        - The function returns the Euclidean distance as a float value.
    """
	return math.sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)

def eye_landmarks_horizontal_distance(eye_mesh_coordinates) -> float:
    return euclidean_distance(eye_mesh_coordinates[0], eye_mesh_coordinates[1])

def eye_landmarks_vertical_distance1(eye_mesh_coordinates) -> float:
    return euclidean_distance(eye_mesh_coordinates[2], eye_mesh_coordinates[3])

def eye_landmarks_vertical_distance2(eye_mesh_coordinates) -> float:
    return euclidean_distance(eye_mesh_coordinates[4], eye_mesh_coordinates[5])

def eye_landmarks_vertical_distance3(eye_mesh_coordinates) -> float:
    return euclidean_distance(eye_mesh_coordinates[6], eye_mesh_coordinates[7])

def eye_landmarks_vertical_distance4(eye_mesh_coordinates) -> float:
    return euclidean_distance(eye_mesh_coordinates[8], eye_mesh_coordinates[9])

def eye_landmarks_vertical_distance5(eye_mesh_coordinates) -> float:
    return euclidean_distance(eye_mesh_coordinates[10], eye_mesh_coordinates[11])

def eye_landmarks_vertical_distance6(eye_mesh_coordinates) -> float:
    return euclidean_distance(eye_mesh_coordinates[12], eye_mesh_coordinates[13])

def eye_landmarks_vertical_distance7(eye_mesh_coordinates) -> float:
    return euclidean_distance(eye_mesh_coordinates[14], eye_mesh_coordinates[15])

def eye_aspect_ratio(eye_mesh_coordinates):
	"""
    Calculates the eye aspect ratio (EAR) for a given list of eye landmark coordinates.

    Args:
        eye_mesh_coordinates (list of tuples): The list of eye landmark coordinates as tuples of (x, y) values.
                                              The list should contain 6 landmark coordinates for each eye, in a specific order.

    Returns:
        float: The eye aspect ratio (EAR) value.

    Raises:
        None.

    Example usage:
        # Define eye landmark coordinates
        left_eye_coordinates = [(x1, y1), (x2, y2), ..., (x6, y6)]  # List of 6 coordinates for the left eye
        right_eye_coordinates = [(x1, y1), (x2, y2), ..., (x6, y6)]  # List of 6 coordinates for the right eye

        # Calculate eye aspect ratio (EAR)
        left_eye_ear = eye_aspect_ratio(left_eye_coordinates)
        right_eye_ear = eye_aspect_ratio(right_eye_coordinates)

        # Print the calculated EAR values
        print("Left Eye Aspect Ratio (EAR): ", left_eye_ear)
        print("Right Eye Aspect Ratio (EAR): ", right_eye_ear)

    Note:
        - The function uses the eye landmark coordinates to calculate the eye aspect ratio (EAR) as a measure of eye openness.
        - The eye_mesh_coordinates parameter should be a list of tuples, where each tuple contains (x, y) values representing the
          landmark coordinates for each eye. The list should contain 6 landmark coordinates for each eye in a specific order.
        - The function returns the eye aspect ratio (EAR) as a float value.
        - The eye aspect ratio (EAR) is calculated as the ratio of the sum of distances between certain landmark points on the eye
          to the width of the eye, as defined by the distance between two specific landmark points on the eye.
        - The eye aspect ratio (EAR) is commonly used in eye tracking and drowsiness detection applications.
    """
	eye_width = euclidean_distance(eye_mesh_coordinates[0], eye_mesh_coordinates[1])
	eye_height_sum = 0
	i = 2
	while i < 16:
		eye_height_sum += euclidean_distance(eye_mesh_coordinates[i], eye_mesh_coordinates[i+1])
		i += 2
	return (1.0*eye_height_sum)/(7.0*eye_width)

def mouth_aspect_ratio(mouth_mesh_coordinates):
	"""
    Calculates the mouth aspect ratio for a given list of mouth landmark coordinates.

    Args:
        mouth_mesh_coordinates (list of tuples): The list of mouth landmark coordinates as tuples of (x, y) values.
                                                 The list should contain 20 landmark coordinates in a specific order.

    Returns:
        float: The mouth aspect ratio value.

    Raises:
        None.

    Example usage:
        # Define mouth landmark coordinates
        mouth_coordinates = [(x1, y1), (x2, y2), ..., (x20, y20)]  # List of 20 coordinates for the mouth

        # Calculate mouth aspect ratio
        mouth_ratio = mouth_aspect_ratio(mouth_coordinates)

        # Print the calculated mouth aspect ratio value
        print("Mouth Aspect Ratio: ", mouth_ratio)

    Note:
        - The function uses the mouth landmark coordinates to calculate the mouth aspect ratio, which is the ratio of the
          sum of heights of certain landmark points on the mouth to the width of the mouth.
        - The mouth_mesh_coordinates parameter should be a list of tuples, where each tuple contains (x, y) values representing the
          landmark coordinates for the mouth. The list should contain 20 landmark coordinates in a specific order.
        - The function returns the mouth aspect ratio as a float value.
        - The mouth aspect ratio is used in facial expression recognition and speech analysis applications as a measure of
          mouth openness or lip movement.
    """
	mouth_width = euclidean_distance(mouth_mesh_coordinates[0], mouth_mesh_coordinates[1])
	mouth_heights_sum = 0
	i = 2
	while i < 20:
		mouth_heights_sum += euclidean_distance(mouth_mesh_coordinates[i], mouth_mesh_coordinates[i+1])
		i += 2
	return (1.0*mouth_heights_sum)/(7.0*mouth_width)

def magic_ratio(eye_mesh_coordinates):
	"""
    Calculates the magic ratio for a given list of eye landmark coordinates.

    Args:
        eye_mesh_coordinates (list of tuples): The list of eye landmark coordinates as tuples of (x, y) values.
                                              The list should contain 16 landmark coordinates for each eye in a specific order.

    Returns:
        float: The magic ratio value.

    Raises:
        None.

    Example usage:
        # Define eye landmark coordinates
        left_eye_coordinates = [(x1, y1), (x2, y2), ..., (x16, y16)]  # List of 16 coordinates for the left eye
        right_eye_coordinates = [(x1, y1), (x2, y2), ..., (x16, y16)]  # List of 16 coordinates for the right eye

        # Calculate magic ratio
        left_eye_magic_ratio = magic_ratio(left_eye_coordinates)
        right_eye_magic_ratio = magic_ratio(right_eye_coordinates)

        # Print the calculated magic ratio values
        print("Left Eye Magic Ratio: ", left_eye_magic_ratio)
        print("Right Eye Magic Ratio: ", right_eye_magic_ratio)

    Note:
        - The function uses the eye landmark coordinates to calculate the magic ratio, which is a weighted sum of heights
          of different landmark points on the eye.
        - The eye_mesh_coordinates parameter should be a list of tuples, where each tuple contains (x, y) values representing the
          landmark coordinates for each eye. The list should contain 16 landmark coordinates for each eye in a specific order.
        - The function returns the magic ratio as a float value.
        - The magic ratio is calculated by assigning different weightages to different heights of landmark points on the eye,
          based on their deviation from a normal range of heights. Points with higher deviation are assigned higher weightages.
        - The magic ratio is used in eye tracking and drowsiness detection applications as a measure of eye openness.
    """
	eye_width = euclidean_distance(eye_mesh_coordinates[0], eye_mesh_coordinates[1])
	eye_height1 = euclidean_distance(eye_mesh_coordinates[2], eye_mesh_coordinates[3])
	eye_height2 = euclidean_distance(eye_mesh_coordinates[4], eye_mesh_coordinates[5])
	eye_height3 = euclidean_distance(eye_mesh_coordinates[6], eye_mesh_coordinates[7])
	eye_height4 = euclidean_distance(eye_mesh_coordinates[8], eye_mesh_coordinates[9])
	eye_height5 = euclidean_distance(eye_mesh_coordinates[10], eye_mesh_coordinates[11])
	eye_height6 = euclidean_distance(eye_mesh_coordinates[12], eye_mesh_coordinates[13])
	eye_height7 = euclidean_distance(eye_mesh_coordinates[14], eye_mesh_coordinates[15])
	# heights: 4 will have maximum weightage
	# heights: 3, 5 will have second maximum weightage
	# heights: 2, 6 will have third maximum weightage
	# heights: 1, 7 will have least weightage
	# As we need to reflect even the smallest change, so
	# we need to give more weightage to those heights which
	# change more dramatically, giving higher deviation in output
	return (4.0*eye_height4+3.0*(eye_height3+eye_height5)+2.0*(eye_height2+eye_height6)+(eye_height1+eye_height7))/16.0*eye_width
