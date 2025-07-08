import os
import time
import threading
import logging
from RealtimeTTS import TextToAudioStream, CoquiEngine
from typing import Optional

class TTSWrapper:
    """
    Text-to-Speech wrapper using RealtimeTTS with real-time playback
    """

    def __init__(self,
                 
                 gpu: bool = False,
                 voice_reference: Optional[str] = None):
        """
        Initialize the TTS engine.
        
        :param model_name: TTS model to use
        :param gpu: Whether to use GPU acceleration
        :param voice_reference: Path to reference audio for voice cloning
        """
        # Verify voice file exists if provided
        if voice_reference and not os.path.exists(voice_reference):
            raise FileNotFoundError(f"Voice file not found: {voice_reference}")
        
        # Initialize the TTS engine
        self.engine = CoquiEngine(use_deepspeed=True, voice=voice_reference)
        
        # Create the audio stream
        self.stream = TextToAudioStream(self.engine)
        
        # Warm up the engine to avoid first-run delays
        self._warm_up()
        
        # State tracking
        self.is_speaking = False
        self.lock = threading.Lock()
        
       # print(f"TTS initialized with model: {model_name}")
        if voice_reference:
            print(f"Using custom voice: {voice_reference}")

    def _warm_up(self):
        """Warm up the TTS engine to avoid first-run delays"""
        print("Warming up TTS engine...")
        self.stream.feed("System warmup").play(muted=True)
        print("Warmup complete")

    def speak(self, text: str, speed_ratio: float = 1.0):
        """
        Speak the given text with real-time playback.
        
        :param text: Text to speak
        :param speed_ratio: Speed adjustment (1.0 = normal speed)
        """
        
        # Clear any existing text in the stream
        self.stream.stop()
        
        # Feed text to the stream and play asynchronously
        self.stream.feed(text)
        
        with self.lock:
            self.is_speaking = True
        
        start_time = time.time()
        self.stream.play_async()
        
        
        
        end_time = time.time()
        duration = end_time - start_time
        print(f"Speech duration: {duration:.2f} seconds")
        
        with self.lock:
            self.is_speaking = False

    def stop(self):
        """Stop any ongoing speech playback."""
        if hasattr(self, 'stream') and self.stream:
            self.stream.stop()
            with self.lock:
                self.is_speaking = False
            print("TTS playback stopped")

    def shutdown(self):
        """Clean up resources and shut down the engine"""
        self.stop()
        if hasattr(self, 'engine') and self.engine:
            self.engine.shutdown()
            print("TTS engine shut down")