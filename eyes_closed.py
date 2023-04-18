# EyesClosed Class

class EyesClosed:
    def __init__(self, frames_threshold: int, alarm_wav_file_path: str) -> None:
        self.frames: int = 0
        self.frames_threshold: int = frames_threshold

    def add_frame(self) -> None:
        self.frames += 1
        if self.frames > self.frames_threshold:
            self.trigger_alarm()

    def reset(self) -> None:
        self.frames = 0

    def trigger_alarm(self) -> None:
        # play sleepy alaram sound
        pass
