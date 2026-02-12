print("Inferface System Modules - Starting to Import")
import queue
import random
import customtkinter
import os
import shutil
import threading
print("Inferface System Modules - Finished Importing")
print("Interface Custom Modules - Starting")
from interface.header import HeaderFrame
from interface.main_menu import MainMenuFrame
from interface.game import GameFrame
from interface.feedback import FeedbackFrame
from utils.spiker import SpikerBox
print("Interface Custom Modules - Finished Importing")

def cleanup_pycache():
    pycache_paths = ['./interface/__pycache__', './utils/__pycache__']
    for path in pycache_paths:
        if os.path.exists(path):
            shutil.rmtree(path)

class Interface(customtkinter.CTk):
    def __init__(self, video_files):
        super().__init__()
        self.title("Capstone Program")
        self.wm_attributes("-fullscreen", True)
        self.state('normal')
        self.frame_history = []
        self.video_files = video_files
        self.game_index = -1
        self.data_queue = queue.Queue()
        self.spiker_box = SpikerBox(interface=self, data_queue=self.data_queue, simulate=False)
        self.games = 3

        if self.games < 1:
            print("Please enter a valid number of games")
            quit()

        self.video_list = random.sample(self.video_files, self.games)
        self.distractions_list = self.generate_distractions()

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.current_frame = None
        self.previous_frame = None
        self.video_playing = False

        self.hazard_times = []
        self.reaction_times = []
        self.shown_distractions = []
        self.expected_inputs = []
        self.given_inputs = []
        self.accuracy = []

        self.eyeAction = "Unknown"
        self.dfAmplitudeAvg = 0
        self.numLookLeft = 0

        self.header_frame = HeaderFrame(self, self.spiker_box)
        self.header_frame.grid(row=1, column=0, sticky="nwe", padx=20, pady=20)

        self.main_menu_frame = MainMenuFrame(self)
        self.game_frame = GameFrame(self, self.video_list[self.game_index], self.distractions_list[self.game_index])
        self.feedback_frame = FeedbackFrame(self)

        self.main_menu_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=20)
        self.game_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=20)
        self.feedback_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=20)
        self.main_menu_frame.grid_remove()
        self.game_frame.grid_remove()
        self.feedback_frame.grid_remove()

        self.show_frame(self.main_menu_frame)

        self.read_thread = None

        self.bind('<space>', self.spacebar_handler)
        self.bind('<Right>', self.next_handler)
        self.bind('<Left>', self.previous_handler)

    def show_frame(self, frame):
        if self.current_frame is not None:
            self.current_frame.grid_remove()
        if isinstance(frame, FeedbackFrame):
            frame.get_perception()
            frame.get_distraction_classification()
            frame.get_distraction_accuracies()
            frame.update_labels()
        frame.grid()
        self.current_frame = frame

    def next_game(self):
        print("hazard:",self.hazard_times)
        print("reaction:",self.reaction_times)
        if self.game_index == -1:
            ports = self.spiker_box.get_ports()
            port = None
            for p in ports:
                if p == self.header_frame.port_menu_var.get():
                    port = p
                    break
            if port:
                self.spiker_box.init_serial(port)
                if self.read_thread is None:
                    self.read_thread = threading.Thread(target=self.spiker_box.continuously_read)
                    self.read_thread.start()
            self.game_index = 0

        if self.game_index < self.games:
            self.game_index += 1
            self.game_frame = GameFrame(self, self.video_list[self.game_index - 1], self.distractions_list[self.game_index - 1])
            self.game_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=20)
            self.show_frame(self.game_frame)
        else:
            self.show_frame(self.feedback_frame)
            self.data_export()

    def generate_distractions(self):
        possible_distractions = ["Shopping List", "Math Problem", "Simon Says"]
        # possible_distractions = ["Debug"]
        
        distractions = []

        if self.games < 3:
            distractions = [random.choice(possible_distractions) for _ in range(self.games)]
        else:
            while len(distractions) < self.games:
                random.shuffle(possible_distractions)
                needed = self.games - len(distractions)
                distractions.extend(possible_distractions[:needed])
        
        return distractions
    
    def process_data_timer(self):
        try:
            while not self.data_queue.empty():
                data_frame = self.data_queue.get_nowait()
                print(data_frame)
        except queue.Empty:
            pass
        self.after(100, self.process_data_timer)
    
    def spacebar_handler(self, event):
        if self.current_frame == self.game_frame:
            frame = self.game_frame.video_frame.frame_count
            self.game_frame.video_frame.stop_video(end_time=frame)

    def next_handler(self, event):
        self.spacebar_handler()

    def previous_handler(self, event):
        self.spacebar_handler()

    def trigger_handler(self):
        if self.current_frame == self.game_frame:
            frame = self.game_frame.video_frame.frame_count
            self.game_frame.video_frame.stop_video(end_time=frame)
    
    def data_export(self):
        data = {
            "Game": list(range(1, self.games + 1)),
            "Distraction": self.shown_distractions,
            "Expected": self.expected_inputs,
            "Given": self.given_inputs,
            "Accuracy": self.accuracy,
            "Hazard Times": self.hazard_times,
            "Reaction Times": self.reaction_times
        }

        with open("./game_data.csv", "w") as file:
            file.write("Game,Distraction,Expected,Given,Accuracy,Hazard Times,Reaction Times\n")
            for i in range(self.games):
                file.write(f"{data['Game'][i]},{data['Distraction'][i]},{data['Expected'][i]},{data['Given'][i]},{data['Accuracy'][i]},{data['Hazard Times'][i]},{data['Reaction Times'][i]}\n")

    def close(self):
        if self.read_thread and self.read_thread.is_alive():
            self.spiker_box.stop_requested = True
            self.read_thread.join()
        self.quit()
        cleanup_pycache()