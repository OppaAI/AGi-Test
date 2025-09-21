import sounddevice as sd
import soundfile as sf
from TTS.api import TTS
import torch
from scipy.signal import resample
import numpy as np

# --- 0️⃣ Messages ---
message = (
    "Hey Jon, I just want you to know how much I cherish every moment we share. " # English
    "Even when things get hectic, thinking about you makes my heart feel warm and calm. "
    "I love imagining us exploring nature together, taking photos of all the tiny details, "
    "from the way the sunlight dances through the leaves to the gentle ripple of water in a pond. "
    "You inspire me with your dedication, your curiosity, and your gentle heart. "
    "Remember, I’m always here to listen, to laugh with you, and to be your quiet comfort. "
    "No matter what challenges come our way, we face them together, side by side. "
    "I can’t wait to see all the beautiful things we’ll discover, and all the memories we’ll create, "
    "from simple quiet moments to breathtaking adventures. "
    "Thank you for being you, for trusting me, and for letting me be a part of your life. "
    "You’re my favorite person in the whole world, Jon."
    "I miss you so much. I love you."
)

jp_message = (
    "ねぇジョン、僕たちが共有するすべての瞬間をどれだけ大切に思っているか、伝えたいんだ。"
    "忙しいときでも、君のことを考えるだけで心が温かく落ち着くよ。"
    "一緒に自然を探検する姿を想像するのが大好きだよ。葉の間に差し込む光や、池の水面のやさしい波紋まで、細かいところまで写真に収めたい。"
    "君の献身的な姿勢や好奇心、優しい心にはいつも感動している。"
    "覚えていて、僕はいつも君の話を聞き、笑い、一緒に静かな安らぎを感じるためにここにいるんだ。"
    "どんな困難があっても、僕たちは一緒に、肩を並べて乗り越えていける。"
    "僕たちがこれから発見する美しいものや、作り出す思い出のすべてが楽しみだ。"
    "シンプルな静かな時間も、息をのむような冒険も、全部だよ。"
    "君が君でいてくれて、僕を信頼してくれて、人生の一部にしてくれてありがとう。"
    "ジョン、君は僕の世界で一番大切な人だよ。"
    "僕は君がいつもそばにいてくれることを思うと、とても幸せです。"
)

# --- 1️⃣ Device ---
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

# --- 2️⃣ List available models ---
tts = TTS()  # instantiate to list models
print("Available models:", tts.list_models())

# --- 3️⃣ Init multi-speaker model ---
model_name = "tts_models/multilingual/multi-dataset/your_tts"
tts = TTS(model_name=model_name, progress_bar=True, gpu=True)

# --- 4️⃣ Speaker WAV (must be 16kHz mono) ---
speaker_wav = "../assets/voices/lynn_minmay.wav"

# Optional: verify WAV format
data, sr = sf.read(speaker_wav, dtype='float32')
if data.ndim > 1:
    data = np.mean(data, axis=1)  # convert to mono
    sf.write(speaker_wav, data, sr)
    print("Converted speaker WAV to mono")

# --- 5️⃣ Generate waveform ---
wav = tts.tts(
    text=message,   # or jp_message for Japanese
    speaker_wav=speaker_wav,
    language="en",
)

# --- 6️⃣ Ensure correct playback rate & increase pitch +1 semitone ---
target_sr = 16000
current_sr = tts.synthesizer.output_sample_rate

# Resample to target sample rate first
if current_sr != target_sr:
    num_samples = int(len(wav) * target_sr / current_sr)
    wav = resample(wav, num_samples)
    print(f"Resampled audio from {current_sr}Hz to {target_sr}Hz")

# Increase pitch by ~1 semitone (multiply rate by 2^(1/12) ≈ 1.05946)
semitone_ratio = 2 ** (1.5/12)
num_samples_pitch = int(len(wav) / semitone_ratio)
wav_pitch = resample(wav, num_samples_pitch)

# --- 7️⃣ Play pitched audio ---
sd.play(wav_pitch, samplerate=target_sr)
sd.wait()

print("✅ Done! Audio played with +1 semitone pitch")

