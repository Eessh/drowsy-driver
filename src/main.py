# Imports
import time
import tomli
import cv2 as cv
import mediapipe as mp

import colors
import mesh_indices
import ratio_utils
import drawing_utils
import eyes_closed
import yawn

# Detection utility functions
def landmarks_detection(image, results, draw_detection_points=False, color=colors.GREEN):
	"""
    Detects facial landmarks on an input image using a pre-trained facial landmark detection model.

    Args:
        image (numpy.ndarray): The input image as a NumPy array.
        results (mediapipe.FaceLandmark): The facial landmark detection results from the Mediapipe library.
        draw_detection_points (bool, optional): Whether to draw the detected landmark points on the image. 
                                                Defaults to False.
        color (tuple, optional): The color of the drawn landmark points, specified as a tuple of (B, G, R) values. 
                                 Defaults to color.GREEN.

    Returns:
        list of tuple: A list of tuples representing the coordinates of the detected facial landmarks in the format (x, y),
                       where x is the horizontal coordinate and y is the vertical coordinate.

    Raises:
        None.

    Example usage:
        # Load an image
        image = cv.imread('face_image.jpg')

        # Detect facial landmarks
        face_mesh = mediapipe_face_mesh(image)

        # Extract facial landmark coordinates
        landmark_coordinates = landmarks_detection(image, face_mesh, draw_detection_points=True)

    Note:
        - The function assumes that the input image has already been preprocessed, resized, and passed through a face
          detection model to obtain the facial landmark detection results.
        - The function only extracts the coordinates of the facial landmarks for the first detected face in the image.
          If there are multiple faces, only the landmarks of the first face will be returned.
        - The facial landmarks are represented as a list of tuples, where each tuple contains the (x, y) coordinates
          of a single facial landmark point. The coordinates are normalized to the image size, with (0,0) at the top-left
          corner of the image and (1,1) at the bottom-right corner of the image.
        - If the `draw_detection_points` parameter is set to True, the detected facial landmarks will be drawn on the
          input image using circles with the specified `color` parameter.
    """
	image_height, image_width = image.shape[:2]
	if results.multi_face_landmarks:
		mesh_coordinates = [(int(point.x*image_width), int(point.y*image_height)) for point in results.multi_face_landmarks[0].landmark]
	else:
		return None
	if draw_detection_points:
		for point in mesh_coordinates:
			cv.circle(image, point, 2, color)
	return mesh_coordinates

# Face Mesh
face_mesh = mp.solutions.face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Start capturing video
camera = cv.VideoCapture(0)
width = int(camera.get(cv.CAP_PROP_FRAME_WIDTH)) # 3
height = int(camera.get(cv.CAP_PROP_FRAME_HEIGHT)) # 4
print(f"Video Resolution: ({width}, {height})")
frame_counter = 0

# Loading config
config_file = open("config.toml", mode="rb")
config = tomli.load(config_file)
print("Eye Aspect Ratio Threshold: " + str(config["ratio_thresholds"]["eye_aspect_ratio"]))
print("Magic Ratio Threshold: " + str(config["ratio_thresholds"]["magic_ratio"]))
print("Mouth Aspect Ratio Threshold: " + str(config["ratio_thresholds"]["mouth_aspect_ratio"]))

# Ratio Thresholds
EYE_ASPECT_RATIO_THRESHOLD = config["ratio_thresholds"]["eye_aspect_ratio"]
MAGIC_RATIO_THRESHOLD = config["ratio_thresholds"]["magic_ratio"] # Magic Ratio threshold varies according to person's distance from the camera.
MOUTH_ASPECT_RATIO_THRESHOLD = config["ratio_thresholds"]["mouth_aspect_ratio"]

# Time Thresholds
EYES_CLOSED_TIME_THRESHOLD = config["time_thresholds"]["eyes_closed"]
YAWN_TIME_THRESHOLD = config["time_thresholds"]["yawn"]

eyes_closed_alarm = eyes_closed.EyesClosed(time_threshold=EYES_CLOSED_TIME_THRESHOLD, alarm_wav_file_path="assets/audios/eyes_closed.wav")
yawn_alarm = yawn.Yawn(time_threshold=YAWN_TIME_THRESHOLD, alarm_wav_file_path="assets/audios/yawn.wav")

# Main loop
start_time = time.time()
while True:
	frame_read_successful, frame = camera.read()
	if not frame_read_successful:
		break

	frame_counter += 1

	rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
	results = face_mesh.process(rgb_frame)

	if results.multi_face_landmarks:
		mesh_coordinates = landmarks_detection(frame, results, draw_detection_points=False)
		if config["draw_landmarks"]["face"]:
			for point in mesh_coordinates:
				cv.circle(frame, point, 1, colors.CYAN, -1, cv.LINE_AA)
		if config["draw_landmarks"]["eye"]:
			for index in mesh_indices.left_eye:
				cv.circle(frame, mesh_coordinates[index], 1, colors.GREEN, -1, cv.LINE_AA)
			for index in mesh_indices.right_eye:
				cv.circle(frame, mesh_coordinates[index], 1, colors.GREEN, -1, cv.LINE_AA)
		if config["draw_landmarks"]["mouth"]:
			for index in mesh_indices.mouth:
				cv.circle(frame, mesh_coordinates[index], 1, colors.MAGNETA, -1, cv.LINE_AA)

		# Calculating eye aspect ratios
		left_eye_aspect_ratio = ratio_utils.eye_aspect_ratio([mesh_coordinates[index] for index in mesh_indices.left_eye])
		right_eye_aspect_ratio = ratio_utils.eye_aspect_ratio([mesh_coordinates[index] for index in mesh_indices.right_eye])

		# Calculating magic ratios
		left_eye_magic_ratio = ratio_utils.magic_ratio([mesh_coordinates[index] for index in mesh_indices.left_eye])
		right_eye_magic_ratio = ratio_utils.magic_ratio([mesh_coordinates[index] for index in mesh_indices.right_eye])

		# Calculating mouth aspect ratio
		mouth_aspect_ratio = ratio_utils.mouth_aspect_ratio([mesh_coordinates[index] for index in mesh_indices.mouth])

		# Calculating FPS
		end_time = time.time() - start_time
		fps = frame_counter / end_time

		# Drawing FPS
		if config["draw_info"]["fps"]:
			frame = drawing_utils.text(frame, f"FPS: {round(fps, 1)}", (width-80, 0))

		# Drawing ratios
		if config["show_ratios"]["eye_aspect_ratio"]:
			frame = drawing_utils.text_with_background(
								frame,
								f"(Left, Right) Eye Aspect Ratios: ({round(left_eye_aspect_ratio,3)}, {round(right_eye_aspect_ratio,3)})",
								(0, 0),
								text_color=colors.GREEN,
								background_color=colors.BLACK,
								background_opacity=0.8
							)
		if config["show_ratios"]["magic_ratio"]:
			frame = drawing_utils.text_with_background(
								frame,
								f"(Left, Right) Magic Ratios: ({round(left_eye_magic_ratio,3)}, {round(right_eye_magic_ratio,3)})",
								(0, 23),
								text_color=colors.GREEN,
								background_color=colors.BLACK,
								background_opacity=0.8
							)
		if config["show_ratios"]["mouth_aspect_ratio"]:
			frame = drawing_utils.text_with_background(
								frame,
								f"Mouth Aspect Ratio: {round(mouth_aspect_ratio, 3)}",
								(0, 46),
								text_color=colors.GREEN,
								background_color=colors.BLACK,
								background_opacity=0.8
							)

		# Deciding eyes open or closed
		if left_eye_aspect_ratio>=EYE_ASPECT_RATIO_THRESHOLD or right_eye_aspect_ratio>=EYE_ASPECT_RATIO_THRESHOLD:
			frame = drawing_utils.text_with_background(
								frame,
								"Eyes: OPEN",
								(0, 69),
								text_color=colors.BLACK,
								background_color=colors.GREEN,
								background_opacity=0.8
							)
			eyes_closed_alarm.reset()
		else:
			frame = drawing_utils.text_with_background(
								frame,
								"Eyes: CLOSE",
								(0, 69),
								text_color=colors.WHITE,
								background_color=colors.RED,
								background_opacity=0.8
							)
			eyes_closed_alarm.add_frame(fps)

		# Deciding mouth yawning or normal
		if mouth_aspect_ratio <= MOUTH_ASPECT_RATIO_THRESHOLD:
			frame = drawing_utils.text_with_background(
								frame,
								"Mouth: NORMAL",
								(0, 92),
								text_color=colors.BLACK,
								background_color=colors.GREEN,
								background_opacity=0.8
							)
			yawn_alarm.reset()
		else:
			frame = drawing_utils.text_with_background(
								frame,
								"Mouth: YAWNING",
								(0, 92),
								text_color=colors.WHITE,
								background_color=colors.RED,
								background_opacity=0.8
							)
			yawn_alarm.add_frame(fps)

	cv.imshow("Drowsy Driver", frame)

	key_pressed = cv.waitKey(1)
	if key_pressed == ord('q'):
		break

# Cleaning up resources used
cv.destroyAllWindows()
camera.release()
