import threading
import queue
import cv2 as cv
import mediapipe as mp

import colors
import mesh_indices
import ratio_utils
import drawing_utils
import eyes_closed
import yawn
import fps

class VideoGet:
	def __init__(self, video_source_index: int) -> None:
		self.video_source_index: int = video_source_index
		self.video_stream = cv.VideoCapture(self.video_source_index)
		(self.frame_read_succesful, self.frame) = self.video_stream.read()
		self.video_stream_frames: queue.Queue = queue.Queue()
		self.video_stream_stopped: bool = False

	def start(self):
		threading.Thread(target=self.loop, args=()).start()

	def loop(self):
		while not self.video_stream_stopped:
			frame_read_succesful, frame = self.video_stream.read()
			if not frame_read_succesful:
				self.frame_read_succesful = False
				self.frame = None
			else:
				self.frame_read_succesful = True
				self.frame = frame
				self.video_stream_frames.put(frame)

	def get(self):
		frame = None
		try:
			frame = self.video_stream_frames.get_nowait()
		except queue.Empty:
			pass
		return frame
		# return self.video_stream_frames.get()

	def stop(self):
		self.video_stream_stopped = True

class VideoProcess:
	def __init__(self, video_get: VideoGet) -> None:
		self.video_get: VideoGet = video_get
		self.processing_stopped: bool = False
		self.face_mesh = mp.solutions.face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)
		self.processed_frames: queue.Queue = queue.Queue()

	def start(self) -> None:
		threading.Thread(target=self.loop, args=()).start()

	def loop(self) -> None:
		while not self.processing_stopped:
			frame = self.video_get.get()
			if frame is None:
				continue
			rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
			results = self.face_mesh.process(rgb_frame)
			if not results.multi_face_landmarks:
				continue

			mesh_coordinates = self.landmarks_detection(rgb_frame, results, draw_detection_points=True)
			self.processed_frames.put(rgb_frame)
			print(f"processed frames length: {self.processed_frames.qsize()}")

	def landmarks_detection(self, frame, results, draw_detection_points: bool = False, color=colors.GREEN):
		image_height, image_width = frame.shape[:2]
		if results.multi_face_landmarks:
			mesh_coordinates = [(int(point.x*image_width), int(point.y*image_height)) for point in results.multi_face_landmarks[0].landmark]
		else:
			return None
		if draw_detection_points:
			for point in mesh_coordinates:
				cv.circle(frame, point, 2, color)
		return mesh_coordinates

	def get(self):
		frame = None
		try:
			frame = self.processed_frames.get_nowait()
		except queue.Empty:
			pass
		return frame
		# return self.processed_frames.get()

	def stop(self):
		self.processing_stopped = True

class VideoShow:
	def __init__(self, video_process: VideoProcess) -> None:
		self.video_process: VideoProcess = video_process
		self.showing_stopped: bool = False

	def start(self) -> None:
		threading.Thread(target=self.loop, args=()).start()

	def loop(self) -> None:
		while not self.showing_stopped:
			frame = self.video_process.get()
			if frame is None:
				continue
			cv.imshow("Drowsy Driver Detection", frame)
			if cv.waitKey(1) == ord("q"):
				self.showing_stopped = True

	def stop(self):
		self.showing_stopped = True

def threaded_get_process_show() -> None:
	video_get: VideoGet = VideoGet(0)
	video_process: VideoProcess = VideoProcess(video_get)
	video_show: VideoShow = VideoShow(video_process)

	video_get.start()
	video_process.start()
	video_show.start()

	while True:
		if video_show.showing_stopped:
			video_process.stop()
			video_get.stop()
			break

threaded_get_process_show()