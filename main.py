import tkinter as tk
from tkinter import ttk
from controller.controller import Controller

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("simple gui")
        self.geometry("300x200")
        
        
        #drop down combobox
        self.dropdown = ttk.Combobox(self, state="readonly")
        #self.dropdown.current(0)  # Set default selection
        self.dropdown.pack(pady=10)
        
        
        #start and stop buttons
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)
        
        #self.controller = Controller()
        
        start_btb = tk.Button(button_frame, text="Start", command= lambda: self.controller.start())
        start_btb.pack(side=tk.LEFT, padx=5)
        
 
        
        self.controller = Controller(self)
        self.controller.populate_dropdown()
        
    def get_selected_device(self):
        """Get the currently selected device from the dropdown."""
        return self.dropdown.get()
        
if __name__ == "__main__":
    app = App()
    app.mainloop()