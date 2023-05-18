# Video Stream Class (Uses Multithreading)

import threading
import cv2 as cv


class VideoStream:
    def __init__(self, video_source_index: int = 0) -> None:
        """
        Initializes the VideoStream object.

        Args:
        - video_source_index (int): Index of the video source device.

        Attributes:
        - video_source_index (int): Index of the video source device.
        - stream: OpenCV VideoCapture object for capturing video frames.
        - frame_read_success (bool): Flag indicating if the frame read was successful.
        - frame: Captured video frame.
        - stream_started (bool): Flag indicating if the video stream has started.
        - stream_ended (bool): Flag indicating if the video stream has ended.
        - thread: Thread object for running the video stream update loop.
        - read_lock: Threading lock for reading the video frame.
        """
        self.video_source_index = video_source_index
        self.stream = cv.VideoCapture(self.video_source_index)
        (self.frame_read_success, self.frame) = self.stream.read()
        self.stream_started: bool = False
        self.stream_ended: bool = False
        self.thread = None
        self.read_lock = threading.Lock()

    def start(self):
        """
        Starts the threaded video stream.

        Returns:
        - self: The VideoStream object itself.

        Notes:
        - If the video stream has already started, a warning message is printed and None is returned.
        """
        if self.stream_started:
            print("[WARNING] Threaded VideoStream has already started !")
            return None
        print("[INFO] Starting threaded VideoStream ...")
        self.stream_started = True
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.start()
        return self

    def update(self) -> None:
        """
        Continuously reads video frames from the video source and updates the frame attribute.

        Returns:
        None
        """
        while not self.stream_ended:
            (frame_read_success, frame) = self.stream.read()
            with self.read_lock:
                self.frame_read_success = frame_read_success
                self.frame = frame

    def read_frame(self):
        """
        Reads the latest video frame from the stream.

        Returns:
        - frame_read_success (bool): Flag indicating if the frame read was successful.
        - frame: The captured video frame.
        """
        with self.read_lock:
            frame_read_success = self.frame_read_success
            frame = self.frame.copy()
        return frame_read_success, frame

    def end(self) -> None:
        """
        Ends the video stream by stopping the update loop and joining the thread.

        Returns:
        None
        """
        self.stream_started = False
        self.stream_ended = True
        self.thread.join()

    def width(self) -> int:
        """
        Returns the width of the video stream in pixels.

        Returns:
        - width (int): Width of the video stream.
        """
        return int(self.stream.get(cv.CAP_PROP_FRAME_WIDTH))

    def height(self) -> int:
        """
        Returns the height of the video stream in pixels.

        Returns:
        - height (int): Height of the video stream.
        """
        return int(self.stream.get(cv.CAP_PROP_FRAME_HEIGHT))

    def __exit__(self, exec_type, exec_value, traceback) -> None:
        """
        Releases the video stream resource when exiting the context.

        Returns:
        None
        """
        self.stream.release()
