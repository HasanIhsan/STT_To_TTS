
import os
import numpy as np
from TTS.api import TTS
import sounddevice as sd
import soundfile as sf

class TTSWrapper:
    """
    Text-to-Speech wrapper using Coqui TTS with real-time playback
    plus a save-to-file utility.
    """

    def __init__(self,
                 model_name: str = "tts_models/en/vctk/vits",
                 gpu: bool = False):
        # load the model
        self.tts = TTS(model_name=model_name, progress_bar=False, gpu=gpu)

        # grab and clean multi-speaker names if available
        raw = getattr(self.tts, "speakers", None)
        if raw:
            self.speakers = [s.strip() for s in raw]
            print("Available speakers:", self.speakers)
        else:
            self.speakers = None

        # sample rate for playback & saving
        if hasattr(self.tts, "synthesizer") and self.tts.synthesizer is not None and hasattr(self.tts.synthesizer, "output_sample_rate"):
            self.sample_rate = self.tts.synthesizer.output_sample_rate
        elif hasattr(self.tts, "output_sample_rate"):
            self.sample_rate = self.tts.output_sample_rate
        else:
            raise AttributeError("Could not determine output_sample_rate from TTS model.")

    def _get_speaker_name(self, speaker_idx):
        """
        Return the chosen speaker name (string) for a multi-speaker model.
        Defaults to index 0 if None.
        """
        if not self.speakers:
            return None

        if speaker_idx is None:
            speaker_idx = 0
            print(f"[TTS] No speaker_idx given; defaulting to '{self.speakers[0]}'")
        if not (0 <= speaker_idx < len(self.speakers)):
            raise IndexError(f"speaker_idx {speaker_idx} out of range")
        return self.speakers[speaker_idx]

    def speak(self,
              text: str,
              speaker_idx: int = 0,
              speaker_wav: str = "",
              pitch_shift: float = 1.0,
              speed_ratio: float = 1.0):
        """
        Synthesize speech and play it immediately.
        """
        # Only include pitch_shift and speed_ratio if supported by the model
        kwargs = {}
        tts_args = self.tts.tts.__code__.co_varnames
        if "pitch_shift" in tts_args:
            kwargs["pitch_shift"] = pitch_shift
        if "speed_ratio" in tts_args:
            kwargs["speed_ratio"] = speed_ratio

        # voice‑clone vs. built‑in speaker
        if speaker_wav:
            kwargs["speaker_wav"] = speaker_wav
        else:
            # multi‑speaker: translate idx → name
            name = self._get_speaker_name(speaker_idx)
            if name:
                kwargs["speaker"] = name

        print(f"[TTS] Calling tts.tts with: {kwargs}")
        wav = self.tts.tts(text=text, **kwargs)

        sd.play(wav, self.sample_rate)
        sd.wait()

    def save(self,
             text: str,
             output_path: str = "output.wav",
             speaker_idx: int = 0,
             speaker_wav: str = "",
             pitch_shift: float = 1.0,
             speed_ratio: float = 1.0) -> str:
        # Only include pitch_shift and speed_ratio if supported by the model
        kwargs = {}
        tts_args = self.tts.tts.__code__.co_varnames
        if "pitch_shift" in tts_args:
            kwargs["pitch_shift"] = pitch_shift
        if "speed_ratio" in tts_args:
            kwargs["speed_ratio"] = speed_ratio
        if speaker_wav:
            kwargs["speaker_wav"] = speaker_wav
        else:
            name = self._get_speaker_name(speaker_idx)
            if name:
                kwargs["speaker"] = name

        print(f"[TTS] Saving with: {kwargs}")
        wav = self.tts.tts(text=text, **kwargs)
        name = self._get_speaker_name(speaker_idx)
        if name:
            kwargs["speaker"] = name

        print(f"[TTS] Saving with: {kwargs}")
        wav = self.tts.tts(text=text, **kwargs)
        sf.write(output_path, wav, self.sample_rate)
        print(f"[TTS] Saved to '{output_path}'")
        return output_path