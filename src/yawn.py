# Yawn Class

import simpleaudio as sa
from frames import Frames


class Yawn:
    def __init__(self, time_threshold: int, alarm_wav_file_path: str) -> None:
        """
        Initializes the Yawn object.

        Args:
        - time_threshold (int): Time threshold in seconds for detecting yawns.
        - alarm_wav_file_path (str): File path of the WAV audio file for the alarm sound.

        Attributes:
        - time_threshold (int): Time threshold in seconds for detecting yawns.
        - alarm_wav_obj: WaveObject instance created from the alarm WAV audio file.
        - alarm_audio_instance: Audio instance for playing the alarm sound.
        - bounded_frames (Frames): Frames object to track the count of bounded frames.
        """
        self.time_threshold: int = time_threshold
        self.alarm_wav_obj = sa.WaveObject.from_wave_file(alarm_wav_file_path)
        self.alarm_audio_instance = None
        self.bounded_frames: Frames = Frames(80)

    def add_bounded_frame(self, ok: bool, fps: float) -> None:
        """
        Adds a bounded frame to the tracker and triggers the alarm if the conditions are met.

        Args:
        - ok (bool): Flag indicating if the frame is "ok" or "notok".
        - fps (float): Frames per second of the video stream.

        Returns:
        None
        """
        if ok:
            self.bounded_frames.add_ok()
        else:
            self.bounded_frames.add_notok()
        if (
            self.bounded_frames.crossed_threshold()
            and self.bounded_frames.ok + self.bounded_frames.notok > self.time_threshold * fps
        ):
            self.trigger_alarm()

    def update_time_threshold(self, time_threshold: int) -> None:
        """
        Updates the time threshold for detecting yawns.

        Args:
        - time_threshold (int): Time threshold in seconds.

        Returns:
        None
        """
        self.time_threshold = time_threshold

    def reset(self) -> None:
        """
        Resets the state of the Yawn object.

        Returns:
        None
        """
        self.bounded_frames.reset()
        if self.alarm_audio_instance:
            if self.alarm_audio_instance.is_playing():
                self.alarm_audio_instance.stop()
            self.alarm_audio_instance = None

    def trigger_alarm(self) -> None:
        """
        Triggers the alarm by playing the alarm sound.

        Returns:
        None
        """
        # play yawing warning alaram sound
        if self.alarm_audio_instance:
            if self.alarm_audio_instance.is_playing():
                return
            else:
                self.alarm_audio_instance = self.alarm_wav_obj.play()
        else:
            self.alarm_audio_instance = self.alarm_wav_obj.play()

    def stop_alarm(self) -> None:
        """
        Stops the alarm if it is currently playing.

        Returns:
        None
        """
        if self.alarm_audio_instance:
            if self.alarm_audio_instance.is_playing():
                self.alarm_audio_instance.stop()

    def is_playing(self) -> bool:
        """
        Checks if the alarm sound is currently playing.

        Returns:
        - is_playing (bool): True if the alarm sound is playing, False otherwise.
        """
        if self.alarm_audio_instance:
            return self.alarm_audio_instance.is_playing()
        return False
