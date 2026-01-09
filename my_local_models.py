import aiohttp
import pyttsx3
import wave
import tempfile
import json
from vosk import Model, KaldiRecognizer
from livekit.agents.stt import STT

# --- STT: Vosk ---
class VoskSTT(STT):
    def __init__(self, model_path):
        # define capabilities
        capabilities = type("c", (), {"streaming": False})()
        super().__init__(capabilities=capabilities)

        # store vosk model in a private attribute
        self._vosk_model = Model(model_path)
        self._listeners = {}

    def on(self, event_name, callback):
        self._listeners.setdefault(event_name, []).append(callback)

    async def _recognize_impl(self, audio_frame, **kwargs) -> str:
        # audio_frame is a LiveKit AudioFrame 
        pcm_bytes = audio_frame.data.tobytes() 
        rec = KaldiRecognizer(self._vosk_model, audio_frame.sample_rate) 
        rec.AcceptWaveform(pcm_bytes) 
        result = rec.Result() 
        text = json.loads(result).get("text", "") # fire metrics event if listeners exist 
        for cb in self._listeners.get("metrics_collected", []): 
            cb({"length": len(pcm_bytes)}) 
        return text
vosk_stt = VoskSTT("/home/smitha/outbound-caller-python/inbound/models/vosk-model-small-en-us-0.15")

# --- LLM: Ollama REST ---
class OllamaLLM:
    async def generate(self, text: str) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "http://localhost:11434/v1/chat/completions",
                json={"model": "mistral", "messages": [{"role": "user", "content": text}]},
            ) as resp:
                result = await resp.json()
                return result["choices"][0]["message"]["content"]

ollama_llm = OllamaLLM()

# --- TTS: pyttsx3 ---
class Pyttsx3TTS:
    def __init__(self):
        self.engine = pyttsx3.init()

    async def speak(self, text: str) -> bytes:
        # Save speech to a temporary WAV file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            self.engine.save_to_file(text, tmp.name)
            self.engine.runAndWait()
            tmp.seek(0)
            audio_bytes = tmp.read()
        return audio_bytes

pyttsx3_tts = Pyttsx3TTS()

