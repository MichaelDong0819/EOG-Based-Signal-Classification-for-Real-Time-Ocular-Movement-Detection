print("Header System Modules - Starting to Import")
import customtkinter
print("Header System Modules - Finished Importing")

class HeaderFrame(customtkinter.CTkFrame):
    def __init__(self, master, spiker):
        super().__init__(master)
        self.spiker = spiker
        self.ports = spiker.get_ports()

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)

        self.quit_button = customtkinter.CTkButton(self, text="Quit", command=lambda: self.master.close(), font=("Arial", 18), border_spacing=8)
        self.quit_button.grid(row=0, column=0, sticky='w', padx=20, pady=20)

        if self.ports:
            self.port_menu_var = customtkinter.StringVar(value=self.ports[0])
            self.port_menu = customtkinter.CTkOptionMenu(self, values=[port for port in self.ports], variable=self.port_menu_var, font=("Arial", 18), height=self.quit_button.cget("height")+8)
            self.port_menu.grid(row=0, column=1, padx=20, pady=20)