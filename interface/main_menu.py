print("Main Menu System Modules - Starting to Import")
import tkinter as tk
import customtkinter
print("Main Menu System Modules - Finished Importing")

class MainMenuFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)

        self.title_label = customtkinter.CTkLabel(self, text="Spiker Box Program", font=("Arial", 32))
        self.title_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        self.play_button = customtkinter.CTkButton(self, text="Play", command=master.next_game, font=("Arial", 18), border_spacing=8)
        self.play_button.place(relx=0.5, rely=0.9, anchor=tk.CENTER)