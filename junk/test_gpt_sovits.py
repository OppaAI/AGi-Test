from gpt_sovits_python import TTS
import soundfile as sf

# Initialize the model
tts = TTS()

text = "你好，我是你的語音助手。"  # Cantonese

# Synthesize
audio, sr = tts.tts(text)

# Save to WAV
sf.write("yue_output.wav", audio, sr)

print("✅ Cantonese TTS audio saved to yue_output.wav")
