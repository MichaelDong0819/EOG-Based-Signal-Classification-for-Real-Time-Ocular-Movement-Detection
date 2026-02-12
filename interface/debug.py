print("Debug System Modules - Starting to Import")
import tkinter as tk
import customtkinter
print("Debug System Modules - Finished Importing")

class DebugFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.header = customtkinter.CTkLabel(self, text="Debug", font=("Arial", 22))
        self.header.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        self.label_eyeAction = customtkinter.CTkLabel(self, font=("Arial", 18))
        self.label_eyeAction.place(relx=0.5, rely=0.45, anchor=tk.CENTER)

        self.label_dfAmplitudeAvg = customtkinter.CTkLabel(self, font=("Arial", 18))
        self.label_dfAmplitudeAvg.place(relx=0.5, rely=0.50, anchor=tk.CENTER)

        self.label_numLookLeft = customtkinter.CTkLabel(self, font=("Arial", 18))
        self.label_numLookLeft.place(relx=0.5, rely=0.55, anchor=tk.CENTER)

        self.update_labels()

    def update_labels(self):
        self.label_eyeAction.configure(text=f"Action: {self.master.master.eyeAction}")
        self.label_dfAmplitudeAvg.configure(text=f"DF Amplitude (Avg): {self.master.master.dfAmplitudeAvg}")
        self.label_numLookLeft.configure(text=f"Number of Look Lefts: {self.master.master.numLookLeft}")
        self.after(1, self.update_labels)
    
    def video_ended(self):
        self.collect_results()
    
    def collect_results(self):
        self.master.master.shown_distractions.append("Debug")
        self.master.master.expected_inputs.append(None)
        self.master.master.given_inputs.append(None)
        self.master.master.accuracy.append(None)

        self.master.master.next_game()