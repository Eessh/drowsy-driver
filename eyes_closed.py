# EyesClosed Class

class EyesClosed:
    """
    Class to track the number of frames where eyes are closed and trigger an alarm if the threshold is exceeded.

    Attributes:
        frames (int): The current count of frames where eyes are closed.
        frames_threshold (int): The threshold value for the number of frames where eyes are closed before triggering an alarm.
        alarm_wav_file_path (str): The file path of the warning sound file in WAV format.

    Methods:
        __init__(self, frames_threshold: int, alarm_wav_file_path: str) -> None:
            Constructor to initialize the EyesClosed object.

            Args:
                frames_threshold (int): The threshold value for the number of frames where eyes are closed before triggering an alarm.
                alarm_wav_file_path (str): The file path of the warning sound file in WAV format.

        add_frame(self) -> None:
            Method to increment the frames count when eyes are closed. If the frames count exceeds the threshold,
            it triggers the alarm.

        reset(self) -> None:
            Method to reset the frames count to 0.

        trigger_alarm(self) -> None:
            Method to trigger the alarm when the frames count exceeds the threshold.
            You can implement the logic to play the warning sound here using a sound library or system commands.
            For example, using PyDub library, or system commands to play the sound.

    Usage:
        eyes_closed = EyesClosed(frames_threshold=20, alarm_wav_file_path='path/to/alarm.wav')
        # Call the add_frame() method for each frame where eyes are closed.
        # When the frames count exceeds the threshold, the trigger_alarm() method will be called to play the alarm.
        eyes_closed.add_frame()
        # Call the reset() method to reset the frames count to 0 if needed.
        eyes_closed.reset()

    Note:
        - Please make sure to install the necessary libraries (e.g. PyDub) and provide a valid file path to the warning sound file in WAV format when using this class in your application.
        - You may need to implement the logic for playing the warning sound in the `trigger_alarm()` method using an appropriate sound library or system commands depending on your specific environment and requirements.
        - Adjust the frames_threshold value to suit your needs. A higher value will require more consecutive frames of closed eyes before triggering the alarm, while a lower value will trigger the alarm sooner.
        - You can customize the trigger_alarm() method to implement the desired action when the alarm is triggered, such as playing a sound, displaying a notification, or sending an alert.
    """

    def __init__(self, frames_threshold: int, alarm_wav_file_path: str) -> None:
        """
        Initializes a new instance of the EyesClosed class with the specified frames threshold and alarm sound file path.

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
        Adds a closed eyes frame to the frame count. If the frame count exceeds the threshold, triggers the alarm.

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
        Plays the sleeping alaram sound to trigger the alarm.

        Args:
            None.

        Returns:
            None.

        Raises:
            None.
        """
        # play sleepy alaram sound
        pass
