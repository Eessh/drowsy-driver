# Yawn Class

import simpleaudio as sa

class Yawn:
    """
    Class to track the duration of yawn events and trigger an alarm if the duration exceeds a threshold.

    Attributes:
        frames (int): The current count of frames where a yawn event is detected.
        time_threshold (int): The threshold value for the duration of yawn events in seconds before triggering an alarm.
        alarm_wav_file_path (str): The file path of the warning sound file in WAV format.

    Methods:
        __init__(self, time_threshold: int, alarm_wav_file_path: str) -> None:
            Constructor to initialize the Yawn object.

            Args:
                time_threshold (int): The threshold value for the duration of yawn events in seconds before triggering an alarm.
                alarm_wav_file_path (str): The file path of the warning sound file in WAV format.

        add_frame(self, fps: float) -> None:
            Method to increment the frames count when a yawn event is detected. The `fps` parameter is the frames per second
            of the video or stream being processed. If the duration of yawn events exceeds the time threshold, it triggers the alarm.

        reset(self) -> None:
            Method to reset the frames count to 0.

        trigger_alarm(self) -> None:
            Method to trigger the alarm when the duration of yawn events exceeds the time threshold.
            You can implement the logic to play the warning sound here using a sound library or system commands.
            For example, using PyDub library, or system commands to play the sound.

    Usage:
        yawn_detector = Yawn(time_threshold=5, alarm_wav_file_path='path/to/alarm.wav')
        # Call the add_frame() method for each frame where a yawn event is detected.
        # When the duration of yawn events exceeds the time threshold, the trigger_alarm() method will be called to play the alarm.
        yawn_detector.add_frame(fps=30)  # Assuming 30 frames per second
        # Call the reset() method to reset the frames count to 0 if needed.
        yawn_detector.reset()

    Note:
        - Please make sure to install the necessary libraries (e.g. PyDub) and provide a valid file path to the warning sound file in WAV format when using this class in your application.
        - You may need to implement the logic for playing the warning sound in the `trigger_alarm()` method using an appropriate sound library or system commands depending on your specific environment and requirements.
        - Adjust the time_threshold value to suit your needs. A higher value will require longer duration of yawn events before triggering the alarm, while a lower value will trigger the alarm sooner.
        - You can customize the trigger_alarm() method to implement the desired action when the alarm is triggered, such as playing a sound, displaying a notification, or sending an alert.
    """

    def __init__(self, time_threshold: int, alarm_wav_file_path: str) -> None:
        """
        Initializes a new instance of the Yawn class with the specified frames threshold and alarm sound file path.

        Args:
            time_threshold (int): The threshold value of time in seconds to trigger the alarm.
            alarm_wav_file_path (str): The file path of the warning sound file in WAV format.

        Returns:
            None.

        Raises:
            None.
        """
        self.frames: int = 0
        self.time_threshold: int = time_threshold
        self.alarm_wav_obj = sa.WaveObject.from_wave_file(alarm_wav_file_path)
        self.alarm_audio_instance = None

    def add_frame(self, fps: float) -> None:
        """
        Adds a yawn frame to the frame count. If the duration of frames added exceeds the time threshold, triggers the alarm.

        Args:
            None.

        Returns:
            None.

        Raises:
            None.
        """
        self.frames += 1
        if self.frames > self.time_threshold*fps:
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
        Plays the yawn warning alaram sound.

        Args:
            None.

        Returns:
            None.

        Raises:
            None.
        """
        # play yawing warning alaram sound
        if self.alarm_audio_instance:
            if self.alarm_audio_instance.is_playing():
                return
            else:
                self.alarm_audio_instance = self.alarm_wav_obj.play()
        else:
            self.alarm_audio_instance = self.alarm_wav_obj.play()
            # self.alarm_audio_instance.wait_done()
