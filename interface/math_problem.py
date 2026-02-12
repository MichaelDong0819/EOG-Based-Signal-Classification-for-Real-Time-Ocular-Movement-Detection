import tkinter
import customtkinter
import random

class MathProblemFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.label = customtkinter.CTkLabel(self, text="Press \"Start Video\" to begin", font=("Arial", 22))
        self.label.pack(expand=True)
        self.generate_problem()

    def generate_problem(self):
        option = random.choice(["Addition/Subtraction", "Multiplication/Division", "Basic Algebra"])
        if option == "Addition/Subtraction":
            num1 = random.randint(1, 100)
            num2 = random.randint(1, 100)
            if random.choice([True, False]):
                self.problem = f"{num1} + {num2}"
                self.expected = num1 + num2
            else:
                self.problem = f"{num1} - {num2}"
                self.expected = num1 - num2
        elif option == "Multiplication/Division":
            num1 = random.randint(1, 50)
            num2 = random.randint(1, 50)
            if random.choice([True, False]):
                self.problem = f"{num1} * {num2}"
                self.expected = num1 * num2
            else:
                while num1 % num2 != 0:
                    num2 = random.randint(1, num1)
                self.problem = f"{num1} / {num2}"
                self.expected = num1 // num2
        elif option == "Basic Algebra":
            num1 = random.randint(1, 50)
            num2 = random.randint(1, 50)
            self.problem = f"x + {num1} = {num2}"
            self.expected = num2 - num1

    def video_started(self):
        self.label.pack_forget()
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.header = customtkinter.CTkLabel(self, text="Solve the following problem", font=("Arial", 22))
        self.header.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)

        self.label = customtkinter.CTkLabel(self, text=self.problem, font=("Arial", 18))
        self.label.grid(row=1, column=1, padx=20, pady=20)
        self.answer_entry = customtkinter.CTkEntry(self, placeholder_text="Answer Here", font=("Arial", 18), width=300)
        self.answer_entry.grid(row=2, column=1, padx=20, pady=20)

    def video_ended(self):
        self.collect_results()
    
    def collect_results(self):
        try:
            user_answer = self.answer_entry.get()
        except:
            user_answer = float('inf')
        
        if user_answer == str(self.expected):
            percentage = 100
        else:
            percentage = 0
        
        self.master.master.shown_distractions.append("Math Problem")
        self.master.master.expected_inputs.append(self.expected)
        self.master.master.given_inputs.append(user_answer)
        self.master.master.accuracy.append(percentage)

        self.master.master.next_game()