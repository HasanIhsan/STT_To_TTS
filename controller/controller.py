
from utilities.device_search import DeviceSearch
from STT.stt import STT
#from STT.stt_realtime import STT
#from text_to_speech.tts import TTSWrapper

from text_to_speech.tts_realtime import TTSWrapper

import threading
import time

class Controller:
    def __init__(self, gui):
        self.gui = gui
        self.device_search = DeviceSearch()
        self.stt = STT()
        self.active = False
        self.lock = threading.Lock()
        
        
    
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
    
    """def stt_callback(self, text: str):
       #Handle transcribed text from STT
        with self.lock:
            if not self.active:
                return
                
        # Only process non-empty results
        if text.strip():
            print(f"Transcribed: {text}")
            
            # Handle stop command
            if "sleep" in text.lower():
                print("Sleep command detected, stopping...")
                self.stop()"""
       
    # a fuction for the tts_btn
    def tts_test(self):
        """Test TTS functionality"""
        try:
            input_txt = self.gui.Entry.get("1.0", "end-1c").strip()
            
            tts = TTSWrapper(
                #model_name="tts_models/multilingual/multi-dataset/xtts_v2",
                gpu=False,
                voice_reference="voices/mother.wav"
            )
            tts.speak(input_txt, speed_ratio=1.2)
            
            print(f"TTS speaking: {input_txt}")
        except Exception as e:
            print(f"TTS error: {e}")
    
         
    def start(self):
        sel = self.gui.get_selected_device()
        #print(f"Controller started: selected device is {sel}")
        
        with self.lock:
            if self.active:
                return
            self.active = True
            
        try:
            tts = TTSWrapper(
                #model_name="tts_models/multilingual/multi-dataset/xtts_v2",
                gpu=False,
                voice_reference="voices/mother.wav"
            )
            
            while True:
                #tts = TTSWrapper( model_name="tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)
                
                #custom_voice = "voices/mother.wav"
                
                text = self.stt.transcribe(sel)

                if text == "sleep":
                    print("Stopping transcription...")
                    break
                
                #tts.speak("Hello world", speaker_idx=1, speaker_wav=custom_voice, pitch_shift=1.0, speed_ratio=1.0)

                print(f"Transcribed text: {text}") 

         
            
          
            
                tts.speak(text, speed_ratio=1.2)
                
                # Update GUI state
                #self.gui.set_ui_state(active=True)
                print("Controller started")
            
        except Exception as e:
            #self.gui.show_error(str(e))
            self.stop()
            
        """ while True:
                #tts = TTSWrapper( model_name="tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)
                
                #custom_voice = "voices/mother.wav"
                
                text = self.stt.transcribe(sel)

                if text == "sleep":
                    print("Stopping transcription...")
                    break
                
                #tts.speak("Hello world", speaker_idx=1, speaker_wav=custom_voice, pitch_shift=1.0, speed_ratio=1.0)

                print(f"Transcribed text: {text}") 

        except Exception as e:
            print(f"Error: {e}")"""
        
    def stop(self):
        print("Controller stopped")