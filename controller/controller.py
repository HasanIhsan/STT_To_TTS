from utilities.device_search import DeviceSearch
from STT.stt import STT
from text_to_speech.tts import TTSWrapper
class Controller:
    def __init__(self, gui):
        self.gui = gui
        self.device_search = DeviceSearch()
        self.stt = STT()
    
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
        #print(f"Controller started: selected device is {sel}")
        
        try:
            tts = TTSWrapper(model_name="tts_models/en/vctk/vits", gpu=False)
            text = self.stt.transcribe(sel)
            
            tts.speak(text, speaker_idx=1)
             
            
            
            print(f"Transcribed text: {text}")

        except Exception as e:
            print(f"Error: {e}")
        
    def stop(self):
        print("Controller stopped")