print("Video System Modules - Starting to Import (expected to take around 15 seconds)")
import customtkinter
import tkinter as tk
import cv2
from PIL import Image, ImageTk
print("Video System Modules - Finished Importing")
print("Video Custom Modules - Starting to Import")
from utils.file_operations import get_hazard_times
print("Video Custom Modules - Finished Importing")

class VideoFrame(customtkinter.CTkFrame):
    def __init__(self, master, video_path, video_width=835, video_height=470):
        super().__init__(master)
        self.video_path = video_path
        self.vid = cv2.VideoCapture(self.video_path)
        self.video_playing = False
        self.video_width = video_width
        self.video_height = video_height
        self.frame_count = 0
        self.latency = 0

        self.start_time = None
        self.end_time = None

        self.canvas = tk.Canvas(self, width=video_width, height=video_height)
        self.canvas.pack(expand=True, padx=20, pady=20)
        self.start_button = customtkinter.CTkButton(self, text="Start Video", command=self.start_video, font=("Arial", 18), border_spacing=8)
        self.start_button.pack(padx=20, pady=20)

        self.frame_delay = int(1000 / 24)

    def start_video(self):
        if not self.video_playing:
            self.start_time = self.frame_count
            self.master.master.hazard_times.append(get_hazard_times(self.video_path))
            
            self.video_playing = True
            self.master.master.video_playing = True
            
            if hasattr(self.master.distraction_frame, 'video_started'):
                self.master.distraction_frame.video_started()

            self.start_button.pack_forget()
            self.update_video()

    def update_video(self):
        if not self.vid.isOpened():
            return

        ret, frame = self.vid.read()
        if ret:
            self.frame_count += 1
            frame = cv2.resize(frame, (self.video_width, self.video_height))
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
            self.after(self.frame_delay, self.update_video)
        else:
            self.end_time = self.frame_count - self.latency
            self.stop_video()

    def stop_video(self, event=None, **kwargs):
        if self.video_playing:
            end_time = kwargs.get('end_time', 0)
            if end_time:
                self.end_time = end_time
            else:
                self.end_time = self.frame_count
            self.master.master.reaction_times.append((self.end_time / 30) - (self.start_time / 30))
            if self.vid.isOpened():
                self.vid.release()
            self.video_playing = False
            self.master.master.video_playing = False
            
            if hasattr(self.master.distraction_frame, 'video_ended'):
                self.master.distraction_frame.video_ended()