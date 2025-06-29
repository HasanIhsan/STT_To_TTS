 

from RealtimeSTT import AudioToTextRecorder
import sounddevice as sd
import logging
import threading

import torch
print(torch.__version__)
print(torch.cuda.is_available())

class STT:
    """Real-time speech to text using realtimestt library"""
    
    def __init__(self):
        self.recorder = None
        self.is_listening = False
        self.callback = None
        self.stop_event = threading.Event()
        self.thread = None
        
    def start_listening(self, device_name: str, callback: callable):
        """
        Start continuous listening on the given input device
        
        :param device_name: Name of the audio input device
        :param callback: Function to call with transcribed text
        :raises ValueError: if device_name not found
        """
        # Map device name to index
        devices = sd.query_devices()
        device_index = None
        for i, dev in enumerate(devices):
            if device_name in dev['name'] and dev['max_input_channels'] > 0:
                device_index = i
                break
                
        if device_index is None:
            available = [f"{dev['name']} (inputs: {dev['max_input_channels']})" 
                         for dev in devices if dev['max_input_channels'] > 0]
            raise ValueError(f"Device '{device_name}' not found. Available input devices:\n" +
                             "\n".join(available))
        
        print(f"Starting listening on device '{device_name}'...")
        self.callback = callback
        self.stop_event.clear()
        
        # Create recorder configuration
        recorder_config = {
            'spinner': False,
            'language': 'en',
            'use_microphone': True,
            'input_device_index': device_index,
            'enable_realtime_transcription': True,
            'realtime_processing_pause': 0.1,
            'level': logging.ERROR
        }
        
        # Start in a separate thread
        self.thread = threading.Thread(
            target=self._listen_loop,
            args=(recorder_config,),
            daemon=True
        )
        self.is_listening = True
        self.thread.start()
        
    def _listen_loop(self, recorder_config: dict):
        """The actual listening loop running in a separate thread"""
        with AudioToTextRecorder(**recorder_config) as recorder:
            self.recorder = recorder
            print("STT Ready")
            
            while not self.stop_event.is_set():
                # This processes audio and calls our callback when text is ready
                recorder.text(self._process_text)
                
    def _process_text(self, text: str):
        """Internal method to handle transcribed text"""
        if self.callback and text.strip():
            self.callback(text)
        
    def stop_listening(self):
        """Stop the active listening session"""
        if self.is_listening:
            self.stop_event.set()
            self.is_listening = False
            
            if self.recorder:
                self.recorder.stop()
                
            if self.thread and self.thread.is_alive():
                self.thread.join(timeout=1.0)
                
            print("STT stopped")