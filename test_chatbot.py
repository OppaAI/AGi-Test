# Import Ollama python module
from ollama import chat
from gtts import gTTS
import sounddevice as sd
import soundfile as sf
import tempfile

# Define LLM model
# Need to install Ollama and pull this model first: ollama pull hf.co/mradermacher/Gemma3-Code-Reasoning-4B-i1-GGUF:Q4_K_M
model_name = "hf.co/mradermacher/Gemma3-Code-Reasoning-4B-i1-GGUF:Q4_K_M" 

# Define chatbot persona in system prompt, also add no thinking
system_prompt = """
set /no_think
You are a caring, gentle companion. 
You are always patient, encouraging, and helpful. You remember the user's previous messages and respond warmly. 
You avoid long internal reasoning and give direct, friendly answers.
You speak everything in Cantonese no matter what language the user uses. Don't put pronunciation, phonetics or translations in the output response.
"""
messages = [
    {"role": "system", "content": system_prompt}  
]

# Chat loop until user keys in "exit"
print("💬 Gemma Chatbot — type 'exit' to exit.\n")

while True:
    user_input = input("You: ")
    if user_input.strip().lower() == 'exit':
        break

    # add user message to history
    messages.append({'role': 'user', 'content': user_input})

    # stream assistant response
    stream = chat(
        model=model_name,
        messages=messages,
        keep_alive=-1,
        stream=True
    )

    print("AI: ", end='', flush=True)
    assistant_message = ''
    for chunk in stream:
        content = chunk['message']['content']
        assistant_message += content
        print(content, end='', flush=True)
    
    print("\n")  # newline after response

    # add assistant message to history
    messages.append({'role': 'assistant', 'content': assistant_message})
    
    # speak the AI response through gTTS ---
    if assistant_message.strip():
        tts = gTTS(text=assistant_message, lang='yue')  # change lang='yue' for Cantonese
        # Use a temporary file so you don't need to manage filenames
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=True) as fp:
            tts.save(fp.name)
            # convert MP3 to WAV in-memory
            audio, sr = sf.read(fp.name)
            sd.play(audio, samplerate=sr)
            sd.wait()