import tkinter as tk
from tkinter import ttk
from controller.controller import Controller

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("simple gui")
        self.geometry("300x200")
        
        
        #drop down combobox
        options = ["Option 1", "Option 2", "Option 3"]
        self.dropdown = ttk.Combobox(self, values=options)
        self.dropdown.current(0)  # Set default selection
        self.dropdown.pack(pady=10)
        
        
        #start and stop buttons
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)
        
        self.controller = Controller()
        
        start_btb = tk.Button(button_frame, text="Start", command=self.controller.start)
        start_btb.pack(side=tk.LEFT, padx=5)
        
        stop_btn = tk.Button(button_frame, text="Stop", command=self.controller.stop)
        stop_btn.pack(side=tk.LEFT, padx=5)
        
if __name__ == "__main__":
    app = App()
    app.mainloop()