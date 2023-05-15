# Video Stream Class (Uses Multithreading)

import threading
import cv2 as cv


class VideoStream:
    def __init__(self, video_source_index: int = 0) -> None:
        self.video_source_index = video_source_index
        self.stream = cv.VideoCapture(self.video_source_index)
        (self.frame_read_success, self.frame) = self.stream.read()
        self.stream_started: bool = False
        self.stream_ended: bool = False
        self.thread = None
        self.read_lock = threading.Lock()

    def start(self):
        if self.stream_started:
            print("[WARNING] Threaded VideoStream has already started !")
            return None
        print("[INFO] Starting threaded VideoStream ...")
        self.stream_started = True
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.start()
        return self

    def update(self) -> None:
        while not self.stream_ended:
            (frame_read_success, frame) = self.stream.read()
            with self.read_lock:
                self.frame_read_success = frame_read_success
                self.frame = frame

    def read_frame(self):
        with self.read_lock:
            frame_read_success = self.frame_read_success
            frame = self.frame.copy()
        return frame_read_success, frame

    def end(self) -> None:
        self.stream_started = False
        self.stream_ended = True
        self.thread.join()

    def width(self) -> int:
        return int(self.stream.get(cv.CAP_PROP_FRAME_WIDTH))

    def height(self) -> int:
        return int(self.stream.get(cv.CAP_PROP_FRAME_HEIGHT))

    def __exit__(self, exec_type, exec_value, traceback) -> None:
        self.stream.release()
