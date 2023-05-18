# Frames per Second (FPS) Class

import time


class FPS:
    def __init__(self) -> None:
        """
        Initializes the FPS (Frames Per Second) counter.

        Attributes:
        - _start_time (float): Start time of the FPS measurement.
        - _stop_time (float): Stop time of the FPS measurement.
        - _frames (int): Number of frames processed.
        """
        self._start_time: float = 0
        self._stop_time: float = 0
        self._frames: int = 0

    def start(self) -> None:
        """
        Starts the FPS measurement by recording the start time.

        Returns:
        None
        """
        self._start_time = time.time()

    def stop(self) -> None:
        """
        Stops the FPS measurement by recording the stop time.

        Returns:
        None
        """
        self._stop_time = time.time()

    def update(self) -> None:
        """
        Updates the FPS counter by incrementing the frame count.

        Returns:
        None
        """
        self._frames += 1

    def fps(self) -> float:
        """
        Calculates and returns the frames per second (FPS) based on the recorded start and stop times.

        Returns:
        - fps (float): Frames per second value.
        """
        return self._frames / (self._stop_time - self._start_time)
