from utilities.device_search import DeviceSearch

class Controller:
    def __init__(self, gui):
        self.gui = gui
        self.device_search = DeviceSearch()
    
    def populate_dropdown(self):
        # populate the dropdown with available input devices
        
        devices = self.device_search.get_input_devices()
        
        print(f"Available devices: {devices}")
        if not devices:
            devices = ["No input devices found"]
        
        #repace the dropdown values
        self.gui.dropdown['values'] = devices
        if devices:
            self.gui.dropdown.current(0)
    
    def start(self):
        sel = self.gui.get_selected_device()
        print(f"Controller started: selected device is {sel}")
        
    def stop(self):
        print("Controller stopped")