# Frames per Second (FPS) Class

import time

class FPS:
	def __init__(self) -> None:
		self._start_time: float = 0
		self._stop_time: float = 0
		self._frames: int = 0
	
	def start(self) -> None:
		self._start_time = time.time()
	
	def stop(self) -> None:
		self._stop_time = time.time()
	
	def update(self) -> None:
		self._frames += 1
	
	def fps(self) -> float:
		return self._frames / (self._stop_time - self._start_time)
