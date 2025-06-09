import speech_recognition as sr


class STT:
    """ a simple speech to text wrapper using the SpeechRecognition library """
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        
    def transcribe(self, device_name: str, timeout: float = 5.0, phrase_time_limit: float = 10.0) -> str:
        """
            Listen on the given input device and return the recognized text.

            :param device_name: Name of the audio input device (must exactly match one from sr.Microphone.list_microphone_names()).
            :param timeout: maximum seconds to wait for phrase to start.
            :param phrase_time_limit: maximum seconds of audio to record once phrase starts.
            :returns: Transcribed text.
            :raises ValueError: if device_name not found.
            :raises sr.RequestError, sr.UnknownValueError: for recognition errors.
        """
        #map device name to index
        mic_list = sr.Microphone.list_microphone_names()
        try:
            device_index = mic_list.index(device_name)
        except ValueError:
            raise ValueError(f"Device '{device_name}' not found. Available devices:\n" +
                             "\n".join(f"{i}: {name}" for i, name in enumerate(mic_list)))
        
        
        with sr.Microphone(device_index=device_index) as source:
            #option to adjust for ambient noise
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
            print(f"Listening on device '{device_name}'...")
            
            audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            
        # sned to google wev speec API
        
        print("Transcribing...")
        text = self.recognizer.recognize_google(audio)
        print(f"Transcribed text: {text}")
        return text