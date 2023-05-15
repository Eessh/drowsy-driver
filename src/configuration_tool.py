import threading
import tkinter as tk
import sv_ttk
import tomli
from tkinter import ttk


class ConfigurationTool:
	def __init__(self) -> None:
		# loading config
		self.config = tomli.load(open("config.toml", mode="rb"))
		# creating window
		self.window = tk.Tk()
		# setting window properties
		self.window.title("Drowsy Driver - Configuration Tool")
		self.window.geometry("660x700")
		self.window.resizable(False, False)
		# initializing Tkinter variables
		# ratio to use Tkinter variable
		self.tk_var_ratio_to_use = tk.StringVar(
			master=self.window, value=self.config["ratio_to_use"]
		)
		# draw info Tkinter variables
		self.tk_var_draw_resolution = tk.BooleanVar(
			master=self.window, value=self.config["draw_info"]["resolution"]
		)
		self.tk_var_draw_fps = tk.BooleanVar(
			master=self.window, value=self.config["draw_info"]["fps"]
		)
		# draw landmarks Tkinter variables
		self.tk_var_draw_face_landmarks = tk.BooleanVar(
			master=self.window, value=self.config["draw_landmarks"]["face"]
		)
		self.tk_var_draw_eye_landmarks = tk.BooleanVar(
			master=self.window, value=self.config["draw_landmarks"]["eye"]
		)
		self.tk_var_draw_mouth_landmarks = tk.BooleanVar(
			master=self.window, value=self.config["draw_landmarks"]["mouth"]
		)
		# threshold ratio Tkinter variables
		self.tk_var_eye_aspect_ratio = tk.DoubleVar(
			master=self.window,
			value=self.config["ratio_thresholds"]["eye_aspect_ratio"],
		)
		self.tk_var_magic_ratio = tk.DoubleVar(
			master=self.window, value=self.config["ratio_thresholds"]["magic_ratio"]
		)
		self.tk_var_mouth_aspect_ratio = tk.DoubleVar(
			master=self.window,
			value=self.config["ratio_thresholds"]["mouth_aspect_ratio"],
		)
		self.tk_var_modified_eye_aspect_ratio = tk.DoubleVar(
			master=self.window,
			value=self.config["ratio_thresholds"]["modified_eye_aspect_ratio"],
		)
		# draw ratio thresholds Tkinter variables
		self.tk_var_draw_eye_aspect_ratio = tk.BooleanVar(
			master=self.window, value=self.config["show_ratios"]["eye_aspect_ratio"]
		)
		self.tk_var_draw_magic_ratio = tk.BooleanVar(
			master=self.window, value=self.config["show_ratios"]["magic_ratio"]
		)
		self.tk_var_draw_mouth_aspect_ratio = tk.BooleanVar(
			master=self.window, value=self.config["show_ratios"]["mouth_aspect_ratio"]
		)
		self.tk_var_draw_modified_eye_aspect_ratio = tk.BooleanVar(
			master=self.window,
			value=self.config["show_ratios"]["modified_eye_aspect_ratio"],
		)
		# threshold time Tkinter variables
		self.tk_var_eyes_closed = tk.IntVar(
			master=self.window, value=self.config["time_thresholds"]["eyes_closed"]
		)
		self.tk_var_yawn = tk.IntVar(
			master=self.window, value=self.config["time_thresholds"]["yawn"]
		)
		# window thread
		self.thread = None

	def get_ratio_to_use(self) -> str:
		return self.tk_var_ratio_to_use.get()

	def get_draw_resolution(self) -> bool:
		return self.get_draw_resolution.get()

	def get_draw_fps(self) -> bool:
		return self.get_draw_fps.get()

	def get_draw_face_landmarks(self) -> bool:
		return self.get_draw_face_landmarks.get()

	def get_draw_eye_landmarks(self) -> bool:
		return self.get_draw_eye_landmarks.get()

	def get_draw_mouth_landmarks(self) -> bool:
		return self.tk_var_draw_mouth_landmarks.get()

	def get_eye_aspect_ratio(self) -> float:
		return self.get_eye_aspect_ratio.get()

	def get_magic_ratio(self) -> float:
		return self.tk_var_magic_ratio.get()

	def get_mouth_aspect_ratio(self) -> float:
		return self.tk_var_mouth_aspect_ratio.get()

	def get_modified_aspect_ratio(self) -> float:
		return self.tk_var_modified_eye_aspect_ratio.get()

	def get_draw_eye_aspect_ratio(self) -> bool:
		return self.tk_var_draw_eye_aspect_ratio.get()

	def get_draw_magic_ratio(self) -> bool:
		return self.tk_var_draw_magic_ratio.get()

	def get_draw_mouth_aspect_ratio(self) -> bool:
		return self.tk_var_draw_mouth_aspect_ratio.get()

	def get_draW_modified_eye_aspect_ratio(self) -> bool:
		return self.tk_var_draw_modified_eye_aspect_ratio.get()

	def get_eyes_closed_time(self) -> int:
		return self.tk_var_eyes_closed.get()

	def get_yawn_time(self) -> int:
		return self.tk_var_yawn.get()

	def intialize_widgets(self) -> None:
		# Info, Landmarks, Ratios holder frame
		info_landmarks_ratios_wrapper_frame = ttk.Frame(master=self.window, padding=10)
		info_landmarks_ratios_wrapper_frame.pack(side="top", anchor="w")

		# Info Frame
		info_frame = ttk.LabelFrame(
			master=info_landmarks_ratios_wrapper_frame,
			labelwidget=ttk.Label(text="Info", font="SansSerif 13"),
			padding=10,
		)
		info_frame_resolution_checkbutton = ttk.Checkbutton(
			master=info_frame, text="Show video resolution", variable=self.tk_var_draw_resolution
		)
		info_frame_fps_checkbutton = ttk.Checkbutton(
			master=info_frame, text="Show FPS", variable=self.tk_var_draw_fps
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
			variable=self.tk_var_draw_face_landmarks,
		)
		landmarks_frame_eye_checkbutton = ttk.Checkbutton(
			master=landmarks_frame,
			text="Show eye landmarks",
			variable=self.tk_var_draw_eye_landmarks,
		)
		landmarks_frame_mouth_checkbutton = ttk.Checkbutton(
			master=landmarks_frame,
			text="Show mouth landmarks",
			variable=self.tk_var_draw_mouth_landmarks,
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
			variable=self.tk_var_draw_eye_aspect_ratio,
		)
		show_ratios_frame_mouth_aspect_ratio_checkbutton = ttk.Checkbutton(
			master=show_ratios_frame,
			text="Show mouth aspect ratios",
			variable=self.tk_var_draw_mouth_aspect_ratio,
		)
		show_ratios_frame_modified_eye_aspect_ratio_checkbutton = ttk.Checkbutton(
			master=show_ratios_frame,
			text="Show modified aspect ratios",
			variable=self.tk_var_draw_modified_eye_aspect_ratio,
		)
		show_ratios_frame_eye_aspect_ratio_checkbutton.pack(side="top", anchor="w")
		show_ratios_frame_mouth_aspect_ratio_checkbutton.pack(side="top", anchor="w")
		show_ratios_frame_modified_eye_aspect_ratio_checkbutton.pack(side="top", anchor="w")
		show_ratios_frame.pack(side="left", anchor="nw")

		# Ratio Thresholds Frame
		ratios_frame = ttk.LabelFrame(
			master=self.window,
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
			variable=self.tk_var_eye_aspect_ratio,
			length=400,
		)
		ratios_frame_eye_aspect_frame_ratio_label = ttk.Label(
			master=ratios_frame_eye_aspect_frame, textvariable=self.tk_var_eye_aspect_ratio
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
			variable=self.tk_var_mouth_aspect_ratio,
			length=400,
		)
		ratios_frame_mouth_aspect_frame_ratio_label = ttk.Label(
			master=ratios_frame_mouth_aspect_frame, textvariable=self.tk_var_mouth_aspect_ratio
		)
		ratios_frame_modified_aspect_frame = ttk.LabelFrame(
			master=ratios_frame,
			labelwidget=ttk.Label(
				text="Modified Eye Aspect Ratio (Modified-EAR)", font="SansSerif 13"
			),
			padding=10,
		)
		ratios_frame_modified_aspect_frame_ratio_scale = ttk.Scale(
			master=ratios_frame_modified_aspect_frame,
			from_=0.0,
			to=1.0,
			variable=self.tk_var_modified_eye_aspect_ratio,
			length=400,
		)
		ratios_frame_modified_aspect_frame_ratio_label = ttk.Label(
			master=ratios_frame_modified_aspect_frame,
			textvariable=self.tk_var_modified_eye_aspect_ratio,
		)
		ratios_frame_modified_aspect_frame_ratio_calibrate_button = ttk.Button(
			master=ratios_frame_modified_aspect_frame, text="⚙️  Calibrate"
		)
		ratios_frame_modified_aspect_frame_ratio_toggle = ttk.Checkbutton(
			master=ratios_frame_modified_aspect_frame,
			text="Use Modified-EAR",
			variable=self.tk_var_ratio_to_use,
			onvalue="modified_eye_aspect_ratio",
			offvalue="eye_aspect_ratio",
		)
		ratios_frame_eye_aspect_frame_ratio_scale.pack()
		ratios_frame_eye_aspect_frame_ratio_label.pack()
		ratios_frame_eye_aspect_frame.pack(side="top", anchor="w")
		ratios_frame_mouth_aspect_frame_ratio_scale.pack()
		ratios_frame_mouth_aspect_frame_ratio_label.pack()
		ratios_frame_mouth_aspect_frame.pack(side="top", anchor="w", pady=5)
		ratios_frame_modified_aspect_frame_ratio_scale.pack()
		ratios_frame_modified_aspect_frame_ratio_label.pack()
		ratios_frame_modified_aspect_frame_ratio_calibrate_button.pack(side="left")
		ratios_frame_modified_aspect_frame_ratio_toggle.pack(side="left", padx=10)
		ratios_frame_modified_aspect_frame.pack(side="top", anchor="w")
		ratios_frame.pack(side="top", anchor="w", padx=10)

		# Time Thresholds Frame
		times_frame = ttk.LabelFrame(
			master=self.window,
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
				text="{:.0f}".format(self.tk_var_eyes_closed.get())
			)
		times_frame_eyes_closed_frame_scale = ttk.Scale(
			master=times_frame_eyes_closed_frame,
			from_=1,
			to=10,
			variable=self.tk_var_eyes_closed,
			length=400,
			command=update_eyes_closed_label,
		)
		times_frame_eyes_closed_frame_label = ttk.Label(
			master=times_frame_eyes_closed_frame, text="{:.0f}".format(self.tk_var_eyes_closed.get())
		)
		times_frame_yawn_frame = ttk.LabelFrame(
			master=times_frame,
			labelwidget=ttk.Label(text="Yawn time", font="SansSerif 13"),
			padding=10,
		)
		def update_yawn_label(*args):
			times_frame_yawn_frame_label.configure(text="{:.0f}".format(self.tk_var_yawn.get()))
		times_frame_yawn_frame_scale = ttk.Scale(
			master=times_frame_yawn_frame,
			from_=1,
			to=10,
			variable=self.tk_var_yawn,
			length=400,
			command=update_yawn_label,
		)
		times_frame_yawn_frame_label = ttk.Label(
			master=times_frame_yawn_frame, text="{:.0f}".format(self.tk_var_yawn.get())
		)
		times_frame_eyes_closed_frame_scale.pack()
		times_frame_eyes_closed_frame_label.pack()
		times_frame_eyes_closed_frame.pack(side="top", anchor="w")
		times_frame_yawn_frame_scale.pack()
		times_frame_yawn_frame_label.pack()
		times_frame_yawn_frame.pack(side="top", anchor="w", pady=5)
		times_frame.pack(side="top", anchor="w", padx=10, pady=10)

		# Sun Valley Theme
		sv_ttk.set_theme("dark")

	def launch(self) -> None:
		self.thread = threading.Thread(target=self.window.mainloop, args=())
		self.thread.start()

	def close(self) -> None:
		self.window.quit()
		if self.thread:
			self.thread.join()

tool = ConfigurationTool()
tool.intialize_widgets()
tool.launch()

for _ in range(10000):
	pass

tool.close()