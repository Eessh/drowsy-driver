import tomli_w


class ConfigurationWriter:
    def __init__(self):
        """
        Initializes the ConfigurationWriter.

        Attributes:
        - None
        """
        pass

    def write(
        self,
        ratio_to_use: str,
        deamonize: bool,
        draw_info__resolution: bool,
        draw_info__fps: bool,
        draw_landmarks__face: bool,
        draw_landmarks__eye: bool,
        draw_landmarks__mouth: bool,
        ratio_thresholds__eye_aspect_ratio: float,
        ratio_thresholds__modified_eye_aspect_ratio_left: float,
        ratio_thresholds__modified_eye_aspect_ratio_right: float,
        ratio_thresholds__mouth_aspect_ratio: float,
        time_thresholds__eyes_closed: int,
        time_thresholds__yawn: int,
        show_ratios__eye_aspect_ratio: bool,
        show_ratios__mouth_aspect_ratio: bool,
    ):
        """
        Writes the configuration parameters to a TOML file.

        Understand the configuration through the config.toml file in the root folder of this project.

        Parameters:
        - ratio_to_use (str): The ratio to use.
        - deamonize (bool): Whether to daemonize.
        - draw_info__resolution (bool): Whether to draw resolution information.
        - draw_info__fps (bool): Whether to draw FPS information.
        - draw_landmarks__face (bool): Whether to draw face landmarks.
        - draw_landmarks__eye (bool): Whether to draw eye landmarks.
        - draw_landmarks__mouth (bool): Whether to draw mouth landmarks.
        - ratio_thresholds__eye_aspect_ratio (float): The threshold for eye aspect ratio.
        - ratio_thresholds__modified_eye_aspect_ratio_left (float): The threshold for modified eye aspect ratio (left eye).
        - ratio_thresholds__modified_eye_aspect_ratio_right (float): The threshold for modified eye aspect ratio (right eye).
        - ratio_thresholds__mouth_aspect_ratio (float): The threshold for mouth aspect ratio.
        - time_thresholds__eyes_closed (int): The threshold for detecting closed eyes.
        - time_thresholds__yawn (int): The threshold for detecting yawn.
        - show_ratios__eye_aspect_ratio (bool): Whether to show eye aspect ratio.
        - show_ratios__mouth_aspect_ratio (bool): Whether to show mouth aspect ratio.

        Returns:
        - None
        """
        doc = {
            "ratio_to_use": ratio_to_use,
            "deamonize": deamonize,
            "draw_info": {"resolution": draw_info__resolution, "fps": draw_info__fps},
            "draw_landmarks": {
                "face": draw_landmarks__face,
                "eye": draw_landmarks__eye,
                "mouth": draw_landmarks__mouth,
            },
            "ratio_thresholds": {
                "eye_aspect_ratio": ratio_thresholds__eye_aspect_ratio,
                "modified_eye_aspect_ratio_left": ratio_thresholds__modified_eye_aspect_ratio_left,
                "modified_eye_aspect_ratio_right": ratio_thresholds__modified_eye_aspect_ratio_right,
                "mouth_aspect_ratio": ratio_thresholds__mouth_aspect_ratio,
            },
            "time_thresholds": {
                "eyes_closed": time_thresholds__eyes_closed,
                "yawn": time_thresholds__yawn,
            },
            "show_ratios": {
                "eye_aspect_ratio": show_ratios__eye_aspect_ratio,
                "mouth_aspect_ratio": show_ratios__mouth_aspect_ratio,
            },
        }
        with open("config.toml", "wb") as config_file:
            tomli_w.dump(doc, config_file)
