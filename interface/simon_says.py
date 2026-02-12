import tkinter as tk
import customtkinter
import random

class SimonSaysFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.pack_propagate(False)
        self.label = customtkinter.CTkLabel(self, text="Press \"Start\" to begin", font=("Arial", 22))
        self.label.pack(expand=True)
        self.grid_rowconfigure(0, weight=3)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=3)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        self.grid_columnconfigure(3, weight=1)
        self.generate_sequences()
        self.sequence_index = 0
        self.inputs = []
        
    def generate_sequences(self):
        choices = ["top_left", "top_right", "bottom_left", "bottom_right"]
        first_tuple = tuple(random.choices(choices, k=2))
        second_tuple = tuple(first_tuple + tuple(random.choices(choices, k=1)))
        third_tuple = tuple(second_tuple + tuple(random.choices(choices, k=1)))
        self.sequence = [first_tuple, second_tuple, third_tuple]
    
    def flash_sequence(self):
        self.disable_buttons()
        if self.sequence_index < len(self.sequence):
            sequence = self.sequence[self.sequence_index]
            total_flash_duration = 0
            for i, action in enumerate(sequence):
                self.after(500 * i, self.flash_button, action)
                total_flash_duration = 500 * i

            self.after(total_flash_duration + 500, self.enable_buttons)
    
    def flash_button(self, button):
        button_map = {
            "top_left": self.top_left_button,
            "top_right": self.top_right_button,
            "bottom_left": self.bottom_left_button,
            "bottom_right": self.bottom_right_button
        }
        original_color = button_map[button].cget("fg_color")
        highlight_color = "#FFFFFF"
        button_map[button].configure(fg_color=highlight_color)
        self.after(250, lambda: button_map[button].configure(fg_color=original_color))

    def video_started(self):
        self.label.pack_forget()
        self.inputs = [() for _ in range(len(self.sequence))]

        self.top_left_button = customtkinter.CTkButton(self, text="", font=("Arial", 22), command=lambda: self.append("top_left"), border_spacing=8, fg_color="#FFFF00", hover_color="#FFFF00", width=100, height=100)
        self.top_left_button.grid(row=1, column=1, padx=20, pady=20)
        self.top_right_button = customtkinter.CTkButton(self, text="", font=("Arial", 22), command=lambda: self.append("top_right"), border_spacing=8, fg_color="#0000FF", hover_color="#0000FF", width=100, height=100)
        self.top_right_button.grid(row=1, column=2, padx=20, pady=20)
        self.bottom_left_button = customtkinter.CTkButton(self, text="", font=("Arial", 22), command=lambda: self.append("bottom_left"), border_spacing=8, fg_color="#FF0000", hover_color="#FF0000", width=100, height=100)
        self.bottom_left_button.grid(row=2, column=1, padx=20, pady=20)
        self.bottom_right_button = customtkinter.CTkButton(self, text="", font=("Arial", 22), command=lambda: self.append("bottom_right"), border_spacing=8, fg_color="#00FF00", hover_color="#00FF00", width=100, height=100)
        self.bottom_right_button.grid(row=2, column=2, padx=20, pady=20)

        self.disable_buttons()
        self.after(1000, self.flash_sequence)

    def disable_buttons(self):
        self.top_left_button.configure(state="disabled")
        self.top_right_button.configure(state="disabled")
        self.bottom_left_button.configure(state="disabled")
        self.bottom_right_button.configure(state="disabled")

    def enable_buttons(self):
        self.top_left_button.configure(state="normal")
        self.top_right_button.configure(state="normal")
        self.bottom_left_button.configure(state="normal")
        self.bottom_right_button.configure(state="normal")

    def append(self, button):
        current_sequence = self.sequence[self.sequence_index]
        inputs_length = len(self.inputs[self.sequence_index]) if self.inputs and self.sequence_index < len(self.inputs) else 0

        if inputs_length < len(current_sequence):
            self.inputs[self.sequence_index] += (button,)

            if button != current_sequence[inputs_length]:
                self.top_left_button.destroy()
                self.top_right_button.destroy()
                self.bottom_left_button.destroy()
                self.bottom_right_button.destroy()

                self.label = customtkinter.CTkLabel(self, text="Sequence Incorrect", font=("Arial", 22))
                self.label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

            if len(self.inputs[self.sequence_index]) == len(current_sequence):
                self.check_input()

    def check_input(self):
        if self.sequence_index + 1 < len(self.sequence):
            self.sequence_index += 1
            self.disable_buttons()
            self.after(1000, self.flash_sequence)
        else:
            self.disable_buttons()

    def video_ended(self):
        self.collect_results()
        
        self.master.master.next_game()
    
    def inputs_fill(self):
        expected_len = len(self.sequence)
        for i in range(len(self.inputs)):
            if len(self.inputs[i]) < len(self.sequence[i]):
                self.inputs[i] += tuple([None] * (len(self.sequence[i]) - len(self.inputs[i])))
        if len(self.inputs) < expected_len:
            for _ in range(expected_len - len(self.inputs)):
                self.inputs.append(tuple([None] * len(self.sequence[len(self.inputs)])))

    def collect_results(self):
        self.inputs_fill()

        correct = sum(1 for i in range(len(self.sequence)) if self.sequence[i] == self.inputs[i])
        percentage = (correct / len(self.sequence)) * 100

        self.master.master.shown_distractions.append("Simon Says")
        self.master.master.expected_inputs.append(self.sequence)
        self.master.master.given_inputs.append(self.inputs)
        self.master.master.accuracy.append(percentage)