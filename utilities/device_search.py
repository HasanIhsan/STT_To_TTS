import sounddevice as sd

class DeviceSearch:
    
    def get_input_devices(self):
        """Get a list of available input devices."""
        devices = sd.query_devices()
        input_devices = [d['name'] for d in devices if d['max_input_channels'] > 0]
        return input_devices