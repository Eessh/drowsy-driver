import math
import time
import ratio_utils


class ModifiedEyeAspectRatioCalibrator:
	def __init__(self) -> None:
		self.calibrating: bool = False
		self.calibration_time: int = 7
		self.calibration_start_time: float = 0
		self.min_width: float = math.inf
		self.max_width: float = -math.inf
		self.min_height1: float = math.inf
		self.max_height1: float = -math.inf
		self.min_height2: float = math.inf
		self.max_height2: float = -math.inf
		self.min_height3: float = math.inf
		self.max_height3: float = -math.inf
		self.min_height4: float = math.inf
		self.max_height4: float = -math.inf
		self.min_height5: float = math.inf
		self.max_height5: float = -math.inf
		self.min_height6: float = math.inf
		self.max_height6: float = -math.inf
		self.min_height7: float = math.inf
		self.max_height7: float = -math.inf

	def start_calibration(self) -> None:
		self.calibrating = True
		self.calibration_start_time = time.perf_counter()

	def get_calibration_time(self) -> int:
		return self.calibration_time

	def set_calibration_time(self, calibration_time: int) -> None:
		self.calibration_time = calibration_time

	def update(self, eye_mesh_coordinates, callback = None, live_update_callback = None, show_update_logs: bool = False) -> None:
		if self.calibrating:
			if time.perf_counter() - self.calibration_start_time > self.calibration_time:
				self.calibrating = False
				if callback:
					callback(self.get_calibrated_ratio())
				return
			width = ratio_utils.eye_landmarks_horizontal_distance(eye_mesh_coordinates)
			height1 = ratio_utils.eye_landmarks_vertical_distance1(eye_mesh_coordinates)
			height2 = ratio_utils.eye_landmarks_vertical_distance2(eye_mesh_coordinates)
			height3 = ratio_utils.eye_landmarks_vertical_distance3(eye_mesh_coordinates)
			height4 = ratio_utils.eye_landmarks_vertical_distance4(eye_mesh_coordinates)
			height5 = ratio_utils.eye_landmarks_vertical_distance5(eye_mesh_coordinates)
			height6 = ratio_utils.eye_landmarks_vertical_distance6(eye_mesh_coordinates)
			height7 = ratio_utils.eye_landmarks_vertical_distance7(eye_mesh_coordinates)
			self.min_width = min(self.min_width, width)
			self.max_width = max(self.max_width, width)
			self.min_height1 = min(self.min_height1, height1)
			self.max_height1 = max(self.max_height1, height1)
			self.min_height2 = min(self.min_height2, height2)
			self.max_height2 = max(self.max_height2, height2)
			self.min_height3 = min(self.min_height3, height3)
			self.max_height3 = max(self.max_height3, height3)
			self.min_height4 = min(self.min_height4, height4)
			self.max_height4 = max(self.max_height4, height4)
			self.min_height5 = min(self.min_height5, height5)
			self.max_height5 = max(self.max_height5, height5)
			self.min_height6 = min(self.min_height6, height6)
			self.max_height6 = max(self.max_height6, height6)
			self.min_height7 = min(self.min_height7, height7)
			self.max_height7 = max(self.max_height7, height7)
			if live_update_callback:
				live_update_callback(self.get_calibrated_ratio())
			if show_update_logs:
				print("[LOG] Updated Calibration: Modified Eye Aspect Ratio: {:.5f}".format(self.get_calibrated_ratio()))

	def still_calibrating(self) -> bool:
		return self.calibrating

	def stop_calibrating(self) -> None:
		self.calibrating = False

	def get_seconds_elapsed(self) -> int:
		return int(time.perf_counter() - self.calibration_start_time)

	def get_calibrated_ratio(self) -> float:
		ear_closed = (self.min_height1+self.min_height2+self.min_height3+self.min_height4+self.min_height5+self.min_height6+self.min_height7)/(7*self.max_width)
		ear_open = (self.max_height1+self.max_height2+self.max_height3+self.max_height4+self.max_height5+self.max_height6+self.max_height7)/(7*self.min_width)
		return (ear_closed+ear_open)/2

	def reset_min_max_values(self) -> None:
		self.min_width: float = math.inf
		self.max_width: float = -math.inf
		self.min_height1: float = math.inf
		self.max_height1: float = -math.inf
		self.min_height2: float = math.inf
		self.max_height2: float = -math.inf
		self.min_height3: float = math.inf
		self.max_height3: float = -math.inf
		self.min_height4: float = math.inf
		self.max_height4: float = -math.inf
		self.min_height5: float = math.inf
		self.max_height5: float = -math.inf
		self.min_height6: float = math.inf
		self.max_height6: float = -math.inf
		self.min_height7: float = math.inf
		self.max_height7: float = -math.inf