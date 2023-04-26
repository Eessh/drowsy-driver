import multiprocessing
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
import fps

def landmarks_detection(image, results, draw_detection_points=False, color=colors.GREEN):
	image_height, image_width = image.shape[:2]
	if results.multi_face_landmarks:
		mesh_coordinates = [(int(point.x*image_width), int(point.y*image_height)) for point in results.multi_face_landmarks[0].landmark]
	else:
		return None
	if draw_detection_points:
		for point in mesh_coordinates:
			cv.circle(image, point, 2, color)
	return mesh_coordinates

# def initialize_pool(
# 	pool_frames_queue: multiprocessing.Queue,
# 	pool_face_mesh,
# 	pool_width: int,
# 	pool_height: int,
# 	pool_frames_per_second: fps.FPS,
# 	pool_EYE_ASPECT_RATIO_THRESHOLD,
# 	pool_MAGIC_RATIO_THRESHOLD,
# 	pool_MOUTH_ASPECT_RATIO_THRESHOLD,
# 	pool_EYES_CLOSED_TIME_THRESHOLD,
# 	pool_YAWN_TIME_THRESHOLD,
# 	pool_eyes_closed_alarm: eyes_closed.EyesClosed,
# 	pool_yawn_alarm: yawn.Yawn,
# 	pool_config
# 	):
# 	global processed_frames, face_mesh, width, height, frames_per_second, EYE_ASPECT_RATIO_THRESHOLD, MAGIC_RATIO_THRESHOLD, MOUTH_ASPECT_RATIO_THRESHOLD, EYES_CLOSED_TIME_THRESHOLD, YAWN_TIME_THRESHOLD, eyes_closed_alarm, yawn_alarm, config
# 	processed_frames = pool_frames_queue
# 	face_mesh = pool_face_mesh
# 	width = pool_width
# 	height = pool_height
# 	frames_per_second = pool_frames_per_second
# 	EYE_ASPECT_RATIO_THRESHOLD = pool_EYE_ASPECT_RATIO_THRESHOLD
# 	MAGIC_RATIO_THRESHOLD = pool_MAGIC_RATIO_THRESHOLD
# 	MOUTH_ASPECT_RATIO_THRESHOLD = pool_MOUTH_ASPECT_RATIO_THRESHOLD
# 	EYES_CLOSED_TIME_THRESHOLD = pool_EYES_CLOSED_TIME_THRESHOLD
# 	YAWN_TIME_THRESHOLD = pool_YAWN_TIME_THRESHOLD
# 	eyes_closed_alarm = pool_eyes_closed_alarm
# 	yawn_alarm = pool_yawn_alarm
# 	config = pool_config

def initialize_pool(
	pool_frames_queue: multiprocessing.Queue,
	):
	global processed_frames
	processed_frames = pool_frames_queue

def process_frame(
	frame,
	face_mesh,
	width: int,
	height: int,
	frames_per_second: fps.FPS,
	EYE_ASPECT_RATIO_THRESHOLD,
	MAGIC_RATIO_THRESHOLD,
	MOUTH_ASPECT_RATIO_THRESHOLD,
	EYES_CLOSED_TIME_THRESHOLD,
	YAWN_TIME_THRESHOLD,
	eyes_closed_alarm: eyes_closed.EyesClosed,
	yawn_alarm: yawn.Yawn,
	config
	) -> None:
	print("[INFO] Called.")

	results = face_mesh.process(frame)

	if not results.multi_face_landmarks:
		return

	mesh_coordinates = landmarks_detection(frame, results, draw_detection_points=False)

	if not mesh_coordinates:
		return

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
	# end_time = time.time() - start_time
	frames_per_second.stop()
	# fps = frame_counter / end_time
	frames_per_second_value = frames_per_second.fps()

	# Drawing FPS
	if config["draw_info"]["fps"]:
		frame = drawing_utils.text(frame, f"FPS: {round(frames_per_second_value, 1)}", (width-80, 0))

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
		eyes_closed_alarm.add_bounded_frame(ok = True, fps = frames_per_second_value)
	else:
		frame = drawing_utils.text_with_background(
							frame,
							"Eyes: CLOSE",
							(0, 69),
							text_color=colors.WHITE,
							background_color=colors.RED,
							background_opacity=0.8
						)
		eyes_closed_alarm.add_bounded_frame(ok = False, fps = frames_per_second_value)

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
		yawn_alarm.add_bounded_frame(ok = True, fps = frames_per_second_value)
	else:
		frame = drawing_utils.text_with_background(
							frame,
							"Mouth: YAWNING",
							(0, 92),
							text_color=colors.WHITE,
							background_color=colors.RED,
							background_opacity=0.8
						)
		yawn_alarm.add_bounded_frame(ok = False, fps = frames_per_second_value)
	
	# Adding processed frame to the queue
	processed_frames.put(frame)
	cv.imshow("Drowsy Driver Detection", frame)

def show() -> None:
	while True:
		if processed_frames.empty():
			print("[INFO] Processed frames empty!")
			continue
		frame = processed_frames.get()
		if frame is None:
			print("[INFO] Stopped showing frames.")
			break
		cv.imshow("Drowsy Driver Detection", frame)
		key_pressed = cv.waitKey(1)
		if key_pressed == ord('q'):
			break

if __name__ == "__main__":
	face_mesh = mp.solutions.face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)

	camera = cv.VideoCapture(0)
	width = int(camera.get(cv.CAP_PROP_FRAME_WIDTH)) # 3
	height = int(camera.get(cv.CAP_PROP_FRAME_HEIGHT)) # 4
	print(f"Video Resolution: ({width}, {height})")
	# frame_counter = 0
	frames_per_second: fps.FPS = fps.FPS()
	frames_per_second.start()

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

	eyes_closed_alarm: eyes_closed.EyesClosed = eyes_closed.EyesClosed(time_threshold=EYES_CLOSED_TIME_THRESHOLD, alarm_wav_file_path="assets/audios/eyes_closed.wav")
	yawn_alarm: yawn.Yawn = yawn.Yawn(time_threshold=YAWN_TIME_THRESHOLD, alarm_wav_file_path="assets/audios/yawn.wav")

	# Multiprocessing Pool
	processed_frames = multiprocessing.Queue()
	pool = multiprocessing.Pool(processes=2, initializer=initialize_pool, initargs=(processed_frames,))

	# Showing processed frames task
	# show_task_future = pool.apply_async(func=show, args=(), callback=None, error_callback=None)

	futures = []
	while True:
		frame_read_successful, frame = camera.read()
		if frame_read_successful:
			frames_per_second.update()
			rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

			f = pool.apply_async(func=process_frame, args=(rgb_frame, face_mesh, width, height, frames_per_second, EYE_ASPECT_RATIO_THRESHOLD, MAGIC_RATIO_THRESHOLD, MOUTH_ASPECT_RATIO_THRESHOLD, EYES_CLOSED_TIME_THRESHOLD, YAWN_TIME_THRESHOLD, eyes_closed_alarm, yawn_alarm, config,), callback=None, error_callback=None)
			futures.append(f)
		else:
			print("[ERROR] Unable to read frame from webcam video feed!")
			break
		# time.sleep(0.0025)

	for f in futures:
		f.get()

	processed_frames.put(None)
	# show_task_future.get()

	print("[DONE]")