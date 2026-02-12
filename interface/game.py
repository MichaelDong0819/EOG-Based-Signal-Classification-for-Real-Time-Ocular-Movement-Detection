print("Game System Modules - Starting to Import")
import customtkinter
print("Game System Modules - Finished Importing")
print("Game Custom Modules - Starting to Import")
from interface.video import VideoFrame
from interface.shopping_list import ShoppingListFrame
from interface.math_problem import MathProblemFrame
from interface.simon_says import SimonSaysFrame
from interface.debug import DebugFrame
print("Game Custom Modules - Finished Importing")

class GameFrame(customtkinter.CTkFrame):
    def __init__(self, master, video_file, distraction):
        super().__init__(master)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.video_file = video_file
        self.distraction = distraction

        self.video_frame = VideoFrame(self, video_file)
        self.video_frame.grid(row=0, column=2, columnspan=2, padx=20, pady=20, sticky="nsew")

        self.distraction_frame = None

        if self.distraction == "Shopping List":
            self.distraction_frame = ShoppingListFrame(self)
        elif self.distraction == "Math Problem":
            self.distraction_frame = MathProblemFrame(self)
        elif self.distraction == "Simon Says":
            self.distraction_frame = SimonSaysFrame(self)
        elif self.distraction == "Debug":
            self.distraction_frame = DebugFrame(self)
        
        try:
            self.distraction_frame.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")
        except AttributeError:
            pass