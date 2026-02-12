print("Feedback System Modules - Starting to Import")
import tkinter as tk
import customtkinter
print("Feedback System Modules - Finished Importing")

class FeedbackFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_rowconfigure(0, weight=2)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=0)
        self.grid_rowconfigure(4, weight=0)
        self.grid_rowconfigure(5, weight=0)
        self.grid_rowconfigure(6, weight=3)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        self.grid_columnconfigure(3, weight=0)
        self.grid_columnconfigure(4, weight=1)

        self.perception_category = None
        self.perception_count = 0
        self.perception_total = 0
        self.distraction_classification = None
        self.math_accuracy = None
        self.shopping_accuracy = None
        self.memory_accuracy = None

        self.title_label = customtkinter.CTkLabel(self, text="Feedback", font=("Arial", 32))
        self.title_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        self.overall_label = customtkinter.CTkLabel(self, text="Overall Performance", font=("Arial", 24))
        self.overall_label.grid(row=1, column=2, sticky="ew", pady=(0, 20))

        self.perception_label = customtkinter.CTkLabel(self, text=f"Hazard Perception: {self.perception_category} ({self.perception_count}/{self.perception_total} Passed)", font=("Arial", 18))
        self.perception_label.grid(row=2, column=2, sticky="ew")

        self.distraction_label = customtkinter.CTkLabel(self, text=f"You were {self.distraction_classification} (focus switched {self.master.numLookLeft} times)", font=("Arial", 18))
        self.distraction_label.grid(row=3, column=2, sticky="ew")

        self.accuracy_label = customtkinter.CTkLabel(self, text="Game Accuracy", font=("Arial", 24))
        self.accuracy_label.grid(row=4, column=2, sticky="ew", pady=(40, 20))

        self.math_label = customtkinter.CTkLabel(self, text="", font=("Arial", 18))
        self.math_label.grid(row=5, column=1, sticky="ew", padx=20)

        self.shopping_label = customtkinter.CTkLabel(self, text="", font=("Arial", 18))
        self.shopping_label.grid(row=5, column=2, sticky="ew", padx=20)

        self.simon_label = customtkinter.CTkLabel(self, text="", font=("Arial", 18))
        self.simon_label.grid(row=5, column=3, sticky="ew", padx=20)

        self.play_button = customtkinter.CTkButton(self, text="Close", command=lambda: self.master.close(), font=("Arial", 18), border_spacing=8)
        self.play_button.place(relx=0.5, rely=0.9, anchor=tk.CENTER)
    
    def get_perception(self):
        for i in range(self.master.games):
            self.perception_total = self.perception_total + 1
            if self.master.reaction_times[i] >= self.master.hazard_times[i][0] and self.master.reaction_times[i] <= self.master.hazard_times[i][1]:
                self.perception_count = self.perception_count + 1
        
        if self.perception_count / self.perception_total >= 0.8:
            self.perception_category = "Pass"
        else:
            self.perception_category = "Fail"

    def get_distraction_classification(self):
        if self.master.numLookLeft <= 1:
            self.distraction_classification = "not distracted"
        elif self.master.numLookLeft <= 3:
            self.distraction_classification = "slightly distracted"
        elif self.master.numLookLeft <= 5:
            self.distraction_classification = "moderately distracted"
        else:
            self.distraction_classification = "extremely distracted"

    def get_distraction_accuracies(self):
        self.math_accuracy = self.get_distraction_accuracy("Math Problem")
        self.shopping_accuracy = self.get_distraction_accuracy("Shopping List")
        self.memory_accuracy = self.get_distraction_accuracy("Simon Says")

    def get_distraction_accuracy(self, distraction):
        matched_accuracies = []
        for index, shown_distraction in enumerate(self.master.shown_distractions):
            if shown_distraction == distraction:
                matched_accuracies.append(self.master.accuracy[index])
        
        if matched_accuracies:
            average = sum(matched_accuracies) / len(matched_accuracies)
        else:
            average = None

        return average

    def update_labels(self):
        self.perception_label.configure(text=f"Hazard Perception: {self.perception_category} ({self.perception_count}/{self.perception_total} Passed)")
        self.distraction_label.configure(text=f"You were {self.distraction_classification} (focus moved {self.master.numLookLeft} times)")
        
        if self.math_accuracy is not None:
            formatted_math_accuracy = f"{self.math_accuracy:.2f}%"
            self.math_label.configure(text=f"Math Problems: {formatted_math_accuracy}")
        else:
            self.math_label.configure(text="Math Problems: Not Played")
        
        if self.shopping_accuracy is not None:
            formatted_shopping_accuracy = f"{self.shopping_accuracy:.2f}%"
            self.shopping_label.configure(text=f"Shopping List: {formatted_shopping_accuracy}")
        else:
            self.shopping_label.configure(text="Shopping List: Not Played")

        if self.memory_accuracy is not None:
            formatted_memory_accuracy = f"{self.memory_accuracy:.2f}%"
            self.simon_label.configure(text=f"Simon Says: {formatted_memory_accuracy}")
        else:
            self.simon_label.configure(text="Simon Says: Not Played")