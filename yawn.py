# Yawn Class

class Yawn:
    """
    Class representing a yawn detection mechanism.

    This class monitors the occurrence of yawns by counting the number of frames where a yawn is detected. When the
    frame count exceeds a given threshold, it triggers an alarm by playing a warning sound.

    Attributes:
        frames (int): The current count of frames where a yawn is detected.
        frames_threshold (int): The threshold value of frames to trigger the alarm.
        alarm_wav_file_path (str): The file path of the warning sound file in WAV format.

    Methods:
        __init__(self, frames_threshold: int, alarm_wav_file_path: str) -> None:
            Initializes a new instance of the Yawn class with the specified frames threshold and alarm sound file path.
        
        add_frame(self) -> None:
            Adds a yawn frame to the frame count. If the frame count exceeds the threshold, triggers the alarm.

        reset(self) -> None:
            Resets the frame count back to zero.
        
        trigger_alarm(self) -> None:
            Plays the warning sound to trigger the alarm.

    Example usage:
        # Initialize yawn detector with frames threshold and alarm sound file path
        yawn_detector = Yawn(frames_threshold=5, alarm_wav_file_path='warning.wav')

        # Loop over frames and detect yawns
        for frame in frames:
            if is_yawn_detected(frame):
                yawn_detector.add_frame()
            else:
                yawn_detector.reset()

    Note:
        - The Yawn class is designed to be used as part of a larger system that captures and processes video frames to detect
          yawns in real-time or near-real-time.
        - The frames_threshold attribute specifies the number of consecutive yawn frames required to trigger the alarm.
        - The alarm_wav_file_path attribute should be a valid file path to the warning sound file in WAV format.
        - The add_frame method is used to increment the frame count and trigger the alarm if the threshold is exceeded.
        - The reset method can be used to reset the frame count back to zero.
        - The trigger_alarm method is responsible for playing the warning sound to indicate the occurrence of a yawn.
    """

    def __init__(self, frames_threshold: int, alarm_wav_file_path: str) -> None:
        """
        Initializes a new instance of the Yawn class with the specified frames threshold and alarm sound file path.

        Args:
            frames_threshold (int): The threshold value of frames to trigger the alarm.
            alarm_wav_file_path (str): The file path of the warning sound file in WAV format.

        Returns:
            None.

        Raises:
            None.
        """
        self.frames: int = 0
        self.frames_threshold: int = frames_threshold

    def add_frame(self) -> None:
        """
        Adds a yawn frame to the frame count. If the frame count exceeds the threshold, triggers the alarm.

        Args:
            None.

        Returns:
            None.

        Raises:
            None.
        """
        self.frames += 1
        if self.frames > self.frames_threshold:
            self.trigger_alarm()

    def reset(self) -> None:
        """
        Resets the frame count back to zero.

        Args:
            None.

        Returns:
            None.

        Raises:
            None.
        """
        self.frames = 0

    def trigger_alarm(self) -> None:
        """
        Plays the warning sound to trigger the alarm.

        Args:
            None.

        Returns:
            None.

        Raises:
            None.
        """
        # play yawing warning alaram sound
        pass
