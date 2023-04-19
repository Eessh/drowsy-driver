# EyesClosed Class

import simpleaudio as sa

class EyesClosed:
    """
    Class to track the duration of eyes closed events and trigger an alarm if the duration exceeds a threshold.

    Attributes:
        frames (int): The current count of frames where eyes closed events are detected.
        time_threshold (int): The threshold value for the duration of eyes closed events in seconds before triggering an alarm.
        alarm_wav_file_path (str): The file path of the warning sound file in WAV format.

    Methods:
        __init__(self, time_threshold: int, alarm_wav_file_path: str) -> None:
            Constructor to initialize the EyesClosed class.

            Args:
                time_threshold (int): The threshold value for the duration of eyes closed events in seconds before triggering an alarm.
                alarm_wav_file_path (str): The file path of the warning sound file in WAV format.

        add_frame(self, fps: float) -> None:
            Method to increment the frames count when an eyes closed event is detected.

            Args:
                fps (float): The frames per second of the video or stream being processed.

            Returns:
                None

            Notes:
                - The `add_frame()` method should be called for each frame where an eyes closed event is detected.
                - If the duration of eyes closed events exceeds the time threshold, it triggers the alarm.

        reset(self) -> None:
            Method to reset the frames count to 0.

            Returns:
                None

        trigger_alarm(self) -> None:
            Method to trigger the alarm when the duration of eyes closed events exceeds the time threshold.
            You can implement the logic to play the warning sound here using a sound library or system commands.

            Returns:
                None

            Notes:
                - Please make sure to install the necessary libraries (e.g. PyDub) and provide a valid file path to the warning sound file in WAV format when using this class in your application.
                - You may need to implement the logic for playing the warning sound in the `trigger_alarm()` method using an appropriate sound library or system commands depending on your specific environment and requirements.
                - Adjust the time_threshold value to suit your needs. A higher value will require longer duration of eyes closed events before triggering the alarm, while a lower value will trigger the alarm sooner.
                - You can customize the `trigger_alarm()` method to implement the desired action when the alarm is triggered, such as playing a sound, displaying a notification, or sending an alert.

    Example Usage:
        # Create an instance of EyesClosed with a time threshold of 5 seconds and the path to the alarm sound file
        eyes_closed_detector = EyesClosed(time_threshold=5, alarm_wav_file_path="/path/to/alarm.wav")

        # Process frames and call add_frame() for each frame where eyes closed event is detected
        for frame in frames:
            if eyes_closed_detected(frame):
                eyes_closed_detector.add_frame(fps)

        # Reset the frames count
        eyes_closed_detector.reset()

        # Implement your logic to trigger the alarm when necessary
        if need_to_trigger_alarm():
            eyes_closed_detector.trigger_alarm()
    """

    def __init__(self, time_threshold: int, alarm_wav_file_path: str) -> None:
        """
        Initializes a new instance of the EyesClosed class with the specified frames threshold and alarm sound file path.

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
        Adds a closed eyes frame to the frame count. If the duration of eyes closed events exceeds the time threshold, it triggers the alarm.

        Args:
            fps (int): The frames per second of the video or stream being processed.

        Returns:
            None

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
        if self.alarm_audio_instance:
            if self.alarm_audio_instance.is_playing():
                self.alarm_audio_instance.stop()
            self.alarm_audio_instance = None

    def trigger_alarm(self) -> None:
        """
        Plays the sleepy alaram sound.

        Args:
            None.

        Returns:
            None.

        Raises:
            None.
        """
        # play sleepy alaram sound
        if self.alarm_audio_instance:
            if self.alarm_audio_instance.is_playing():
                return
            else:
                self.alarm_audio_instance = self.alarm_wav_obj.play()
        else:
            self.alarm_audio_instance = self.alarm_wav_obj.play()
            # self.alarm_audio_instance.wait_done()

    def stop_alarm(self) -> None:
        if self.alarm_audio_instance:
            if self.alarm_audio_instance.is_playing():
                self.alarm_audio_instance.stop()

    def is_playing(self) -> bool:
        if self.alarm_audio_instance:
            return self.alarm_audio_instance.is_playing()
        return False
