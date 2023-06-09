import tkinter as tk
from tkinter import ttk
import sv_ttk
import tomli
import cv2 as cv
import mediapipe as mp
import threading

import colors
import mesh_indices
import ratio_utils
import drawing_utils
import eyes_closed
import yawn
import fps
import modified_eye_aspect_ratio_calibrator
import configuration_writer


"""
    Loading Config
"""
config_file = open("config.toml", mode="rb")
config = tomli.load(config_file)


"""
    Creating app window
"""
app_window = tk.Tk()
app_window.title("Drowsy Driver - Options, Configurations & Calibrations")
app_window.geometry("720x800")
app_window.resizable(False, False)


"""
    Modified Eye Aspect Ratio Calibrator
"""
calibrator_left = (
    modified_eye_aspect_ratio_calibrator.ModifiedEyeAspectRatioCalibrator()
)
calibrator_right = (
    modified_eye_aspect_ratio_calibrator.ModifiedEyeAspectRatioCalibrator()
)


"""
    Initializing Tkinter variables
"""
# Ratio to use Tkinter variable
tk_var_ratio_to_use = tk.StringVar(master=app_window, value=config["ratio_to_use"])

# Deamonizing processing worker thread, with no GUI
tk_var_deamonize_processing_thread = tk.BooleanVar(
    master=app_window, value=config["deamonize"]
)

# Draw info Tkinter variables
tk_var_draw_resolution = tk.BooleanVar(
    master=app_window, value=config["draw_info"]["resolution"]
)
tk_var_draw_fps = tk.BooleanVar(master=app_window, value=config["draw_info"]["fps"])

# Draw landmarks Tkinter variables
tk_var_draw_face_landmarks = tk.BooleanVar(
    master=app_window, value=config["draw_landmarks"]["face"]
)
tk_var_draw_eye_landmarks = tk.BooleanVar(
    master=app_window, value=config["draw_landmarks"]["eye"]
)
tk_var_draw_mouth_landmarks = tk.BooleanVar(
    master=app_window, value=config["draw_landmarks"]["mouth"]
)

# Threshold ratio Tkinter variables
tk_var_eye_aspect_ratio = tk.DoubleVar(
    master=app_window, value=config["ratio_thresholds"]["eye_aspect_ratio"]
)
tk_var_mouth_aspect_ratio = tk.DoubleVar(
    master=app_window, value=config["ratio_thresholds"]["mouth_aspect_ratio"]
)
tk_var_modified_eye_aspect_ratio_left = tk.DoubleVar(
    master=app_window,
    value=config["ratio_thresholds"]["modified_eye_aspect_ratio_left"],
)
tk_var_modified_eye_aspect_ratio_right = tk.DoubleVar(
    master=app_window,
    value=config["ratio_thresholds"]["modified_eye_aspect_ratio_right"],
)

# Draw ratio thresholds Tkinter variables
tk_var_draw_eye_aspect_ratio = tk.BooleanVar(
    master=app_window, value=config["show_ratios"]["eye_aspect_ratio"]
)
tk_var_draw_mouth_aspect_ratio = tk.BooleanVar(
    master=app_window, value=config["show_ratios"]["mouth_aspect_ratio"]
)

# Threshold time Tkinter variables
tk_var_eyes_closed = tk.IntVar(
    master=app_window, value=config["time_thresholds"]["eyes_closed"]
)
tk_var_yawn = tk.IntVar(master=app_window, value=config["time_thresholds"]["yawn"])


"""
    Initializing UI Widgets
"""
# Info, Landmarks, Ratios holder frame
info_landmarks_ratios_wrapper_frame = ttk.Frame(master=app_window, padding=10)
info_landmarks_ratios_wrapper_frame.pack(side="top", anchor="w")

# Info Frame
info_frame = ttk.LabelFrame(
    master=info_landmarks_ratios_wrapper_frame,
    labelwidget=ttk.Label(text="Info", font="SansSerif 13"),
    padding=10,
)
info_frame_resolution_checkbutton = ttk.Checkbutton(
    master=info_frame, text="Show video resolution", variable=tk_var_draw_resolution
)
info_frame_fps_checkbutton = ttk.Checkbutton(
    master=info_frame, text="Show FPS", variable=tk_var_draw_fps
)
info_frame_resolution_checkbutton.pack(side="top", anchor="w")
info_frame_fps_checkbutton.pack(side="top", anchor="w")
info_frame.pack(side="left", anchor="nw")

# Landmarks Frame
landmarks_frame = ttk.LabelFrame(
    master=info_landmarks_ratios_wrapper_frame,
    labelwidget=ttk.Label(text="Landmarks", font="SansSerif 13"),
    padding=10,
)
landmarks_frame_face_checkbutton = ttk.Checkbutton(
    master=landmarks_frame,
    text="Show face landmarks",
    variable=tk_var_draw_face_landmarks,
)
landmarks_frame_eye_checkbutton = ttk.Checkbutton(
    master=landmarks_frame,
    text="Show eye landmarks",
    variable=tk_var_draw_eye_landmarks,
)
landmarks_frame_mouth_checkbutton = ttk.Checkbutton(
    master=landmarks_frame,
    text="Show mouth landmarks",
    variable=tk_var_draw_mouth_landmarks,
)
landmarks_frame_face_checkbutton.pack(side="top", anchor="w")
landmarks_frame_eye_checkbutton.pack(side="top", anchor="w")
landmarks_frame_mouth_checkbutton.pack(side="top", anchor="w")
landmarks_frame.pack(side="left", anchor="nw", padx=10)

# Ratios Frame
show_ratios_frame = ttk.LabelFrame(
    master=info_landmarks_ratios_wrapper_frame,
    labelwidget=ttk.Label(text="Ratios", font="SansSerif 13"),
    padding=10,
)
show_ratios_frame_eye_aspect_ratio_checkbutton = ttk.Checkbutton(
    master=show_ratios_frame,
    text="Show eye aspect ratios",
    variable=tk_var_draw_eye_aspect_ratio,
)
show_ratios_frame_mouth_aspect_ratio_checkbutton = ttk.Checkbutton(
    master=show_ratios_frame,
    text="Show mouth aspect ratios",
    variable=tk_var_draw_mouth_aspect_ratio,
)
show_ratios_frame_eye_aspect_ratio_checkbutton.pack(side="top", anchor="w")
show_ratios_frame_mouth_aspect_ratio_checkbutton.pack(side="top", anchor="w")
show_ratios_frame.pack(side="left", anchor="nw")

# Ratio Thresholds Frame
ratios_frame = ttk.LabelFrame(
    master=app_window,
    labelwidget=ttk.Label(text="Ratio Thresholds", font="SansSerif 13"),
    padding=10,
)
ratios_frame_eye_aspect_frame = ttk.LabelFrame(
    master=ratios_frame,
    labelwidget=ttk.Label(text="Eye Aspect Ratio (EAR)", font="SansSerif 13"),
    padding=10,
)
ratios_frame_eye_aspect_frame_ratio_scale = ttk.Scale(
    master=ratios_frame_eye_aspect_frame,
    from_=0.0,
    to=1.0,
    variable=tk_var_eye_aspect_ratio,
    length=400,
)
ratios_frame_eye_aspect_frame_ratio_label = ttk.Label(
    master=ratios_frame_eye_aspect_frame, textvariable=tk_var_eye_aspect_ratio
)
ratios_frame_mouth_aspect_frame = ttk.LabelFrame(
    master=ratios_frame,
    labelwidget=ttk.Label(text="Mouth Aspect Ratio", font="SansSerif 13"),
    padding=10,
)
ratios_frame_mouth_aspect_frame_ratio_scale = ttk.Scale(
    master=ratios_frame_mouth_aspect_frame,
    from_=0.0,
    to=1.0,
    variable=tk_var_mouth_aspect_ratio,
    length=400,
)
ratios_frame_mouth_aspect_frame_ratio_label = ttk.Label(
    master=ratios_frame_mouth_aspect_frame, textvariable=tk_var_mouth_aspect_ratio
)
ratios_frame_modified_eye_aspect_frame = ttk.LabelFrame(
    master=ratios_frame,
    labelwidget=ttk.Label(
        text="Modified Eye Aspect Ratio (Modified-EAR)", font="SansSerif 13"
    ),
    padding=10,
)
ratios_frame_modified_eye_aspect_left_right_wrapper_frame = ttk.Frame(
    master=ratios_frame_modified_eye_aspect_frame
)
ratios_frame_modified_eye_aspect_frame_left = ttk.Labelframe(
    master=ratios_frame_modified_eye_aspect_left_right_wrapper_frame,
    labelwidget=ttk.Label(text="Left Eye"),
    padding=10,
)
ratios_frame_modified_eye_aspect_frame_right = ttk.Labelframe(
    master=ratios_frame_modified_eye_aspect_left_right_wrapper_frame,
    labelwidget=ttk.Label(text="Right Eye"),
    padding=10,
)
ratios_frame_modified_aspect_frame_left_ratio_scale = ttk.Scale(
    master=ratios_frame_modified_eye_aspect_frame_left,
    from_=0.0,
    to=1.0,
    variable=tk_var_modified_eye_aspect_ratio_left,
    length=300,
)
ratios_frame_modified_aspect_frame_left_ratio_label = ttk.Label(
    master=ratios_frame_modified_eye_aspect_frame_left,
    textvariable=tk_var_modified_eye_aspect_ratio_left,
)
ratios_frame_modified_aspect_frame_right_ratio_scale = ttk.Scale(
    master=ratios_frame_modified_eye_aspect_frame_right,
    from_=0.0,
    to=1.0,
    variable=tk_var_modified_eye_aspect_ratio_right,
    length=300,
)
ratios_frame_modified_aspect_frame_right_ratio_label = ttk.Label(
    master=ratios_frame_modified_eye_aspect_frame_right,
    textvariable=tk_var_modified_eye_aspect_ratio_right,
)
ratios_frame_modified_eye_aspect_button_checkbutton_wrapper_frame = ttk.Frame(
    master=ratios_frame_modified_eye_aspect_frame
)


def handle_calibrate_button_click():
    calibrator_left.start_calibration()
    calibrator_right.start_calibration()
    ratios_frame_modified_aspect_frame_ratio_calibrate_button.state(["disabled"])


ratios_frame_modified_aspect_frame_ratio_calibrate_button = ttk.Button(
    master=ratios_frame_modified_eye_aspect_button_checkbutton_wrapper_frame,
    text="⚙️ Calibrate",
    command=handle_calibrate_button_click,
)
ratios_frame_modified_aspect_frame_ratio_checkbutton = ttk.Checkbutton(
    master=ratios_frame_modified_eye_aspect_button_checkbutton_wrapper_frame,
    text="Use Modified-EAR",
    variable=tk_var_ratio_to_use,
    onvalue="modified_eye_aspect_ratio",
    offvalue="eye_aspect_ratio",
)
ratios_frame_eye_aspect_frame_ratio_scale.pack()
ratios_frame_eye_aspect_frame_ratio_label.pack()
ratios_frame_eye_aspect_frame.pack(side="top", anchor="w")
ratios_frame_mouth_aspect_frame_ratio_scale.pack()
ratios_frame_mouth_aspect_frame_ratio_label.pack()
ratios_frame_mouth_aspect_frame.pack(side="top", anchor="w", pady=5)
ratios_frame_modified_aspect_frame_left_ratio_scale.pack()
ratios_frame_modified_aspect_frame_left_ratio_label.pack()
ratios_frame_modified_aspect_frame_right_ratio_scale.pack()
ratios_frame_modified_aspect_frame_right_ratio_label.pack()
ratios_frame_modified_eye_aspect_frame_left.pack(side="left")
ratios_frame_modified_eye_aspect_frame_right.pack(side="left", padx=10)
ratios_frame_modified_eye_aspect_left_right_wrapper_frame.pack(side="top")
ratios_frame_modified_aspect_frame_ratio_calibrate_button.pack(side="left")
ratios_frame_modified_aspect_frame_ratio_checkbutton.pack(side="left", padx=10)
ratios_frame_modified_eye_aspect_button_checkbutton_wrapper_frame.pack(
    side="top", anchor="w", pady=(10, 0)
)
ratios_frame_modified_eye_aspect_frame.pack(side="top", anchor="w")
ratios_frame.pack(side="top", anchor="w", padx=10)

# Time Thresholds Frame
times_frame = ttk.LabelFrame(
    master=app_window,
    labelwidget=ttk.Label(text="Time Thresholds", font="SansSerif 13"),
    padding=10,
)
times_frame_eyes_closed_frame = ttk.LabelFrame(
    master=times_frame,
    labelwidget=ttk.Label(text="Eyes closed time", font="SansSerif 13"),
    padding=10,
)


def update_eyes_closed_label(*args):
    times_frame_eyes_closed_frame_label.configure(
        text="{:.0f}".format(tk_var_eyes_closed.get())
    )
    eyes_closed_alarm.update_time_threshold(
        int("{:.0f}".format(tk_var_eyes_closed.get()))
    )
    print(
        "[DEBUG] Updated: EyesClosed time threshold: {:.0f}".format(
            tk_var_eyes_closed.get()
        )
    )


times_frame_eyes_closed_frame_scale = ttk.Scale(
    master=times_frame_eyes_closed_frame,
    from_=1,
    to=10,
    variable=tk_var_eyes_closed,
    length=400,
    command=update_eyes_closed_label,
)
times_frame_eyes_closed_frame_label = ttk.Label(
    master=times_frame_eyes_closed_frame, text="{:.0f}".format(tk_var_eyes_closed.get())
)
times_frame_yawn_frame = ttk.LabelFrame(
    master=times_frame,
    labelwidget=ttk.Label(text="Yawn time", font="SansSerif 13"),
    padding=10,
)


def update_yawn_label(*args):
    times_frame_yawn_frame_label.configure(text="{:.0f}".format(tk_var_yawn.get()))
    yawn_alarm.update_time_threshold(int("{:.0f}".format(tk_var_yawn.get())))
    print("[DEBUG] Updated: Yawn time threshold: {:.0f}".format(tk_var_yawn.get()))


times_frame_yawn_frame_scale = ttk.Scale(
    master=times_frame_yawn_frame,
    from_=1,
    to=10,
    variable=tk_var_yawn,
    length=400,
    command=update_yawn_label,
)
times_frame_yawn_frame_label = ttk.Label(
    master=times_frame_yawn_frame, text="{:.0f}".format(tk_var_yawn.get())
)
times_frame_eyes_closed_frame_scale.pack()
times_frame_eyes_closed_frame_label.pack()
times_frame_eyes_closed_frame.pack(side="top", anchor="w")
times_frame_yawn_frame_scale.pack()
times_frame_yawn_frame_label.pack()
times_frame_yawn_frame.pack(side="top", anchor="w", pady=5)
times_frame.pack(side="top", anchor="w", padx=10, pady=10)

deamonize_checkbutton = ttk.Checkbutton(
    master=app_window, text="👻 Deamonize", variable=tk_var_deamonize_processing_thread
)


def handle_save_button_click():
    config_writer = configuration_writer.ConfigurationWriter()
    config_writer.write(
        ratio_to_use=tk_var_ratio_to_use.get(),
        deamonize=tk_var_deamonize_processing_thread.get(),
        draw_info__resolution=tk_var_draw_resolution.get(),
        draw_info__fps=tk_var_draw_fps.get(),
        draw_landmarks__face=tk_var_draw_face_landmarks.get(),
        draw_landmarks__eye=tk_var_draw_eye_landmarks.get(),
        draw_landmarks__mouth=tk_var_draw_mouth_landmarks.get(),
        ratio_thresholds__eye_aspect_ratio=tk_var_eye_aspect_ratio.get(),
        ratio_thresholds__modified_eye_aspect_ratio_left=tk_var_modified_eye_aspect_ratio_left.get(),
        ratio_thresholds__modified_eye_aspect_ratio_right=tk_var_modified_eye_aspect_ratio_right.get(),
        ratio_thresholds__mouth_aspect_ratio=tk_var_mouth_aspect_ratio.get(),
        time_thresholds__eyes_closed=tk_var_eyes_closed.get(),
        time_thresholds__yawn=tk_var_yawn.get(),
        show_ratios__eye_aspect_ratio=tk_var_draw_eye_aspect_ratio.get(),
        show_ratios__mouth_aspect_ratio=tk_var_draw_mouth_aspect_ratio.get(),
    )


save_button = ttk.Button(
    master=app_window, text="📝 Save Configuration", command=handle_save_button_click
)
save_button.pack(side="right", anchor="e", padx=10, pady=10)
deamonize_checkbutton.pack(side="right", anchor="e", padx=10, pady=10)

# Sun Valley Theme
sv_ttk.set_theme("dark")


"""
    Real Processing
"""


def landmarks_detection(
    image, results, draw_detection_points=False, color=colors.GREEN
):
    image_height, image_width = image.shape[:2]
    if results.multi_face_landmarks:
        mesh_coordinates = [
            (int(point.x * image_width), int(point.y * image_height))
            for point in results.multi_face_landmarks[0].landmark
        ]
    else:
        return None
    if draw_detection_points:
        for point in mesh_coordinates:
            cv.circle(image, point, 2, color)
    return mesh_coordinates


quit_processing: bool = False
eyes_closed_alarm = eyes_closed.EyesClosed(
    time_threshold=tk_var_eyes_closed.get(),
    alarm_wav_file_path="assets/audios/eyes_closed.wav",
)
yawn_alarm = yawn.Yawn(
    time_threshold=tk_var_yawn.get(), alarm_wav_file_path="assets/audios/yawn.wav"
)


def update_calibrated_modified_eye_aspect_ratio_left(calibrated_m_ear):
    tk_var_modified_eye_aspect_ratio_left.set(float("{:.2f}".format(calibrated_m_ear)))
    ratios_frame_modified_aspect_frame_ratio_calibrate_button.state(["!disabled"])
    print(
        "[DEBUG] Calibrated: Modified Eye Aspect Ratio (Left Eye): {:.2f}".format(
            calibrated_m_ear
        )
    )


def live_update_calibration_left(calibration_value):
    tk_var_modified_eye_aspect_ratio_left.set(float("{:.8f}".format(calibration_value)))


def update_calibrated_modified_eye_aspect_ratio_right(calibrated_m_ear):
    tk_var_modified_eye_aspect_ratio_right.set(float("{:.2f}".format(calibrated_m_ear)))
    ratios_frame_modified_aspect_frame_ratio_calibrate_button.state(["!disabled"])
    print(
        "[DEBUG] Calibrated: Modified Eye Aspect Ratio (Right Eye): {:.2f}".format(
            calibrated_m_ear
        )
    )


def live_update_calibration_right(calibration_value):
    tk_var_modified_eye_aspect_ratio_right.set(
        float("{:.8f}".format(calibration_value))
    )


def process():
    face_mesh = mp.solutions.face_mesh.FaceMesh(
        min_detection_confidence=0.5, min_tracking_confidence=0.5
    )

    # Starting video capture
    # Use threaded video capture (VideoStream) here for multithreading
    camera = cv.VideoCapture(0)
    width = int(camera.get(cv.CAP_PROP_FRAME_WIDTH))  # 3
    height = int(camera.get(cv.CAP_PROP_FRAME_HEIGHT))  # 4
    print(f"Video Resolution: ({width}, {height})")

    # FPS Counter
    frames_per_second = fps.FPS()
    frames_per_second.start()

    # Processing loop
    while not quit_processing:
        frame_read_successful, frame = camera.read()
        if not frame_read_successful:
            break

        frames_per_second.update()

        rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_frame)
        if results.multi_face_landmarks:
            mesh_coordinates = landmarks_detection(
                frame, results, draw_detection_points=False
            )

            # Drawing landmarks
            if tk_var_draw_face_landmarks.get():
                for point in mesh_coordinates:
                    cv.circle(frame, point, 1, colors.CYAN, -1, cv.LINE_AA)
            if tk_var_draw_eye_landmarks.get():
                for index in mesh_indices.left_eye:
                    cv.circle(
                        frame, mesh_coordinates[index], 1, colors.GREEN, -1, cv.LINE_AA
                    )
                for index in mesh_indices.right_eye:
                    cv.circle(
                        frame, mesh_coordinates[index], 1, colors.GREEN, -1, cv.LINE_AA
                    )
            if tk_var_draw_mouth_landmarks.get():
                for index in mesh_indices.mouth:
                    cv.circle(
                        frame,
                        mesh_coordinates[index],
                        1,
                        colors.MAGNETA,
                        -1,
                        cv.LINE_AA,
                    )

            # Calibrator updation
            calibrator_left.update(
                eye_mesh_coordinates=[
                    mesh_coordinates[index] for index in mesh_indices.left_eye
                ],
                callback=update_calibrated_modified_eye_aspect_ratio_left,
                live_update_callback=live_update_calibration_left,
                show_update_logs=True,
            )
            calibrator_right.update(
                eye_mesh_coordinates=[
                    mesh_coordinates[index] for index in mesh_indices.right_eye
                ],
                callback=update_calibrated_modified_eye_aspect_ratio_right,
                live_update_callback=live_update_calibration_right,
                show_update_logs=True,
            )

            # Calculating eye aspect ratios
            left_eye_aspect_ratio = ratio_utils.eye_aspect_ratio(
                [mesh_coordinates[index] for index in mesh_indices.left_eye]
            )
            right_eye_aspect_ratio = ratio_utils.eye_aspect_ratio(
                [mesh_coordinates[index] for index in mesh_indices.right_eye]
            )

            # Calculating mouth aspect ratio
            mouth_aspect_ratio = ratio_utils.mouth_aspect_ratio(
                [mesh_coordinates[index] for index in mesh_indices.mouth]
            )

            # Calculating FPS
            frames_per_second.stop()
            frames_per_second_value = frames_per_second.fps()

            # Drawing Video Resolutiom
            if tk_var_draw_resolution.get():
                frame = drawing_utils.text(
                    frame, f"Resolution: {width} x {height}", (width - 180, 0)
                )

            # Drawing FPS
            if tk_var_draw_fps.get():
                frame = drawing_utils.text(
                    frame, f"FPS: {round(frames_per_second_value, 2)}", (width - 90, 23)
                )

            # Drawing ratios
            if tk_var_draw_eye_aspect_ratio.get():
                frame = drawing_utils.text_with_background(
                    frame,
                    f"(Left, Right) Eye Aspect Ratios: ({round(left_eye_aspect_ratio,3)}, {round(right_eye_aspect_ratio,3)})",
                    (0, 0),
                    text_color=colors.GREEN,
                    background_color=colors.BLACK,
                    background_opacity=0.8,
                )
            if tk_var_mouth_aspect_ratio.get():
                frame = drawing_utils.text_with_background(
                    frame,
                    f"Mouth Aspect Ratio: {round(mouth_aspect_ratio, 3)}",
                    (0, 23),
                    text_color=colors.GREEN,
                    background_color=colors.BLACK,
                    background_opacity=0.8,
                )

            # Deciding eyes open or closed
            if tk_var_ratio_to_use.get() == "modified_eye_aspect_ratio":
                if (
                    left_eye_aspect_ratio >= tk_var_modified_eye_aspect_ratio_left.get()
                    or right_eye_aspect_ratio
                    >= tk_var_modified_eye_aspect_ratio_right.get()
                ):
                    frame = drawing_utils.text_with_background(
                        frame,
                        "Eyes: OPEN",
                        (0, 46),
                        text_color=colors.BLACK,
                        background_color=colors.GREEN,
                        background_opacity=0.8,
                    )
                    eyes_closed_alarm.add_bounded_frame(
                        ok=True, fps=frames_per_second_value
                    )
                else:
                    frame = drawing_utils.text_with_background(
                        frame,
                        "Eyes: CLOSE",
                        (0, 46),
                        text_color=colors.WHITE,
                        background_color=colors.RED,
                        background_opacity=0.8,
                    )
                    eyes_closed_alarm.add_bounded_frame(
                        ok=False, fps=frames_per_second_value
                    )
            else:
                if (
                    left_eye_aspect_ratio >= tk_var_eye_aspect_ratio.get()
                    or right_eye_aspect_ratio >= tk_var_eye_aspect_ratio.get()
                ):
                    frame = drawing_utils.text_with_background(
                        frame,
                        "Eyes: OPEN",
                        (0, 46),
                        text_color=colors.BLACK,
                        background_color=colors.GREEN,
                        background_opacity=0.8,
                    )
                    eyes_closed_alarm.add_bounded_frame(
                        ok=True, fps=frames_per_second_value
                    )
                    # eyes_closed_alarm.reset()
                else:
                    frame = drawing_utils.text_with_background(
                        frame,
                        "Eyes: CLOSE",
                        (0, 46),
                        text_color=colors.WHITE,
                        background_color=colors.RED,
                        background_opacity=0.8,
                    )
                    eyes_closed_alarm.add_bounded_frame(
                        ok=False, fps=frames_per_second_value
                    )

            # Deciding mouth yawning or normal
            if mouth_aspect_ratio <= tk_var_mouth_aspect_ratio.get():
                frame = drawing_utils.text_with_background(
                    frame,
                    "Mouth: NORMAL",
                    (0, 69),
                    text_color=colors.BLACK,
                    background_color=colors.GREEN,
                    background_opacity=0.8,
                )
                yawn_alarm.add_bounded_frame(ok=True, fps=frames_per_second_value)
            else:
                frame = drawing_utils.text_with_background(
                    frame,
                    "Mouth: YAWNING",
                    (0, 69),
                    text_color=colors.WHITE,
                    background_color=colors.RED,
                    background_opacity=0.8,
                )
                yawn_alarm.add_bounded_frame(ok=False, fps=frames_per_second_value)

        if not tk_var_deamonize_processing_thread.get():
            cv.imshow("Drowsy Driver", frame)
            cv.waitKey(1)
        else:
            cv.destroyAllWindows()

    # Cleaning up resources used
    cv.destroyAllWindows()
    camera.release()


worker_thread = threading.Thread(target=process, args=(), daemon=True)
worker_thread.start()


def handle_window_close_event():
    quit_processing = True
    app_window.destroy()


app_window.protocol(name="WM_DELETE_WINDOW", func=handle_window_close_event)
app_window.mainloop()
