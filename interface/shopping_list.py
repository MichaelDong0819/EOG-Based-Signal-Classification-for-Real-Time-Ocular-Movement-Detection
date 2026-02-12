import tkinter as tk
import customtkinter
import random

class ShoppingListFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack_propagate(False)

        self.all_groceries = ["Apples", "Bananas", "Carrots", "Dairy Milk", "Eggs", 
                              "Flour", "Grapes", "Honey", "Ice Cream", "Jam", 
                              "Kale", "Lettuce", "Mangoes", "Nuts", "Oranges", 
                              "Peppers", "Quinoa", "Rice", "Spinach", "Tomatoes"]
        
        self.current_list = random.sample(self.all_groceries, 5)
        list_text = "\n".join(f"• {item}" for item in self.current_list)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.header = customtkinter.CTkLabel(self, text="Remember the following items", font=("Arial", 22))
        self.header.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        self.label = customtkinter.CTkLabel(self, text=f"{list_text}", font=("Arial", 18))
        self.label.grid(row=0, column=1, sticky="ew")

    def video_started(self):
        self.header.destroy()
        self.label.destroy()
        self.label = customtkinter.CTkLabel(self, text="List hidden while video is playing", font=("Arial", 22))
        self.label.grid(row=0, column=1, sticky="ew")
    
    def video_ended(self):
        self.header.destroy()
        self.label.destroy()

        self.header = customtkinter.CTkLabel(self, text="Select the items you remember", font=("Arial", 22))
        self.header.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        # Reset grid configurations and set a uniform row weight
        self.grid_rowconfigure(0, weight=1)  # For header
        for i in range(1, len(self.all_groceries) + 2):  # Reset row configure for all potential rows
            self.grid_rowconfigure(i, weight=0)  # Set zero weight to all initially

        row = 1
        self.checkboxes = []  # Ensure this is initialized here to avoid reference errors
        for item in self.all_groceries:
            var = tk.BooleanVar(value=False)
            cb = customtkinter.CTkCheckBox(self, text=item, variable=var, font=("Arial", 18))
            cb.grid(row=row, column=1, sticky="ew")
            self.checkboxes.append((cb, var, item))
            row += 1

        # Set row weight for the last row where the button is placed
        self.grid_rowconfigure(row, weight=1)

        self.submit_button = customtkinter.CTkButton(self, text="Submit", command=self.collect_results, font=("Arial", 18), border_spacing=8)
        self.submit_button.grid(row=row, column=1, pady=20, sticky="ew")

    def collect_results(self):
        selected_items = [item for _, var, item in self.checkboxes if var.get()]
        correct = len(set(self.current_list).intersection(selected_items))
        incorrect = len((set(selected_items)).difference(set(self.current_list)))
        total = len(self.current_list)
        percentage = max(((correct - incorrect) / total) * 100,0)

        self.master.master.shown_distractions.append("Shopping List")
        self.master.master.expected_inputs.append(self.current_list)
        self.master.master.given_inputs.append(selected_items)
        self.master.master.accuracy.append(percentage)

        self.master.master.next_game()