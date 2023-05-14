import tkinter as tk
from tkinter import ttk
import sv_ttk
import tomli

config_file = open("config.toml", mode="rb")
config = tomli.load(config_file)

app_window = tk.Tk()
app_window.title("Drowsy Driver - Options & Configurations")
app_window.geometry("1080x720")

# Draw info Tkinter variables
tk_var_draw_resolution = tk.BooleanVar(master=app_window, value=config["draw_info"]["resolution"])
tk_var_draw_fps = tk.BooleanVar(master=app_window, value=config["draw_info"]["fps"])

# Draw landmarks Tkinter variables
tk_var_draw_face_landmarks = tk.BooleanVar(master=app_window, value=config["draw_landmarks"]["face"])
tk_var_draw_eye_landmarks = tk.BooleanVar(master=app_window, value=config["draw_landmarks"]["eye"])
tk_var_draw_mouth_landmarks = tk.BooleanVar(master=app_window, value=config["draw_landmarks"]["mouth"])

# Threshold ratio Tkinter variables
tk_var_eye_aspect_ratio = tk.DoubleVar(master=app_window, value=config["ratio_thresholds"]["eye_aspect_ratio"])
tk_var_magic_ratio = tk.DoubleVar(master=app_window, value=config["ratio_thresholds"]["magic_ratio"])
tk_var_mouth_aspect_ratio = tk.DoubleVar(master=app_window, value=config["ratio_thresholds"]["mouth_aspect_ratio"])

# Draw ratio thresholds Tkinter variables
tk_var_draw_eye_aspect_ratio = tk.BooleanVar(master=app_window, value=config["show_ratios"]["eye_aspect_ratio"])
tk_var_draw_magic_ratio = tk.BooleanVar(master=app_window, value=config["show_ratios"]["magic_ratio"])
tk_var_draw_mouth_aspect_ratio = tk.BooleanVar(master=app_window, value=config["show_ratios"]["mouth_aspect_ratio"])

# Threshold time Tkinter variables
tk_var_eyes_closed = tk.IntVar(master=app_window, value=config["time_thresholds"]["eyes_closed"])
tk_var_yawn = tk.IntVar(master=app_window, value=config["time_thresholds"]["yawn"])

# Info, Landmarks, Ratios holder frame
info_landmarks_ratios_wrapper_frame = ttk.Frame(master=app_window, padding=10)
info_landmarks_ratios_wrapper_frame.pack(side="top", anchor="w")

# Info Frame
info_frame = ttk.LabelFrame(master=info_landmarks_ratios_wrapper_frame, labelwidget=ttk.Label(text="Info", font="SansSerif 13"), padding=10)
info_frame_resolution_checkbutton = ttk.Checkbutton(master=info_frame, text="Show video resolution", variable=tk_var_draw_resolution)
info_frame_fps_checkbutton = ttk.Checkbutton(master=info_frame, text="Show FPS", variable=tk_var_draw_fps)
info_frame_resolution_checkbutton.pack(side="top", anchor="w")
info_frame_fps_checkbutton.pack(side="top", anchor="w")
info_frame.pack(side="left", anchor="nw")

# Landmarks Frame
landmarks_frame = ttk.LabelFrame(master=info_landmarks_ratios_wrapper_frame, labelwidget=ttk.Label(text="Landmarks", font="SansSerif 13"), padding=10)
landmarks_frame_face_checkbutton = ttk.Checkbutton(master=landmarks_frame, text="Show face landmarks", variable=tk_var_draw_face_landmarks)
landmarks_frame_eye_checkbutton = ttk.Checkbutton(master=landmarks_frame, text="Show eye landmarks", variable=tk_var_draw_eye_landmarks)
landmarks_frame_mouth_checkbutton = ttk.Checkbutton(master=landmarks_frame, text="Show mouth landmarks", variable=tk_var_draw_mouth_landmarks)
landmarks_frame_face_checkbutton.pack(side="top", anchor="w")
landmarks_frame_eye_checkbutton.pack(side="top", anchor="w")
landmarks_frame_mouth_checkbutton.pack(side="top", anchor="w")
landmarks_frame.pack(side="left", anchor="nw", padx=10)

# Ratios Frame
show_ratios_frame = ttk.LabelFrame(master=info_landmarks_ratios_wrapper_frame, labelwidget=ttk.Label(text="Ratios", font="SansSerif 13"), padding=10)
show_ratios_frame_eye_aspect_ratio_checkbutton = ttk.Checkbutton(master=show_ratios_frame, text="Show eye aspect ratios", variable=tk_var_draw_eye_aspect_ratio)
show_ratios_frame_mouth_aspect_ratio_checkbutton = ttk.Checkbutton(master=show_ratios_frame, text="Show mouth aspect ratios", variable=tk_var_draw_mouth_aspect_ratio)
show_ratios_frame_eye_aspect_ratio_checkbutton.pack(side="top", anchor="w")
show_ratios_frame_mouth_aspect_ratio_checkbutton.pack(side="top", anchor="w")
show_ratios_frame.pack(side="left", anchor="nw")

# Ratio Thresholds Frame
ratios_frame = ttk.LabelFrame(master=app_window, labelwidget=ttk.Label(text="Ratio Thresholds", font="SansSerif 13"), padding=10)
ratios_frame_eye_aspect_frame = ttk.LabelFrame(master=ratios_frame, labelwidget=ttk.Label(text="Eye Aspect Ratio (EAR)", font="SansSerif 13"), padding=10)
ratios_frame_eye_aspect_frame_ratio_scale = ttk.Scale(master=ratios_frame_eye_aspect_frame, from_=0.0, to=1.0, variable=tk_var_eye_aspect_ratio, length=400)
ratios_frame_eye_aspect_frame_ratio_label = ttk.Label(master=ratios_frame_eye_aspect_frame, textvariable=tk_var_eye_aspect_ratio)
ratios_frame_mouth_aspect_frame = ttk.LabelFrame(master=ratios_frame, labelwidget=ttk.Label(text="Mouth Aspect Ratio", font="SansSerif 13"), padding=10)
ratios_frame_mouth_aspect_frame_ratio_scale = ttk.Scale(master=ratios_frame_mouth_aspect_frame, from_=0.0, to=1.0, variable=tk_var_mouth_aspect_ratio, length=400)
ratios_frame_mouth_aspect_frame_ratio_label = ttk.Label(master=ratios_frame_mouth_aspect_frame, textvariable=tk_var_mouth_aspect_ratio)
ratios_frame_eye_aspect_frame_ratio_scale.pack()
ratios_frame_eye_aspect_frame_ratio_label.pack()
ratios_frame_eye_aspect_frame.pack(side="top", anchor="w")
ratios_frame_mouth_aspect_frame_ratio_scale.pack()
ratios_frame_mouth_aspect_frame_ratio_label.pack()
ratios_frame_mouth_aspect_frame.pack(side="top", anchor="w", pady=5)
ratios_frame.pack(side="top", anchor="w", padx=20)

# Time Thresholds Frame
times_frame = ttk.LabelFrame(master=app_window, labelwidget=ttk.Label(text="Time Thresholds", font="SansSerif 13"), padding=10)
times_frame_eyes_closed_frame = ttk.LabelFrame(master=times_frame, labelwidget=ttk.Label(text="Eyes closed time", font="SansSerif 13"), padding=10)
def update_eyes_closed_label(*args):
	times_frame_eyes_closed_frame_label.configure(text="{:.0f}".format(tk_var_eyes_closed.get()))
times_frame_eyes_closed_frame_scale = ttk.Scale(master=times_frame_eyes_closed_frame, from_=1, to=10, variable=tk_var_eyes_closed, length=400, command=update_eyes_closed_label)
times_frame_eyes_closed_frame_label = ttk.Label(master=times_frame_eyes_closed_frame, text="{:.0f}".format(tk_var_eyes_closed.get()))
times_frame_yawn_frame = ttk.LabelFrame(master=times_frame, labelwidget=ttk.Label(text="Yawn time", font="SansSerif 13"), padding=10)
def update_yawn_label(*args):
	times_frame_yawn_frame_label.configure(text="{:.0f}".format(tk_var_yawn.get()))
times_frame_yawn_frame_scale = ttk.Scale(master=times_frame_yawn_frame, from_=1, to=10, variable=tk_var_yawn, length=400, command=update_yawn_label)
times_frame_yawn_frame_label = ttk.Label(master=times_frame_yawn_frame, text="{:.0f}".format(tk_var_yawn.get()))
times_frame_eyes_closed_frame_scale.pack()
times_frame_eyes_closed_frame_label.pack()
times_frame_eyes_closed_frame.pack(side="top", anchor="w")
times_frame_yawn_frame_scale.pack()
times_frame_yawn_frame_label.pack()
times_frame_yawn_frame.pack(side="top", anchor="w", pady=5)
times_frame.pack(side="top", anchor="w", padx=20, pady=10)

# Sun Valley Theme
sv_ttk.set_theme("dark")

app_window.mainloop()
