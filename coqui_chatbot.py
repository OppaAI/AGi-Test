from RealtimeTTS import CoquiEngine, TextToAudioStream
import time
from ollama import chat
import sys
import os

# Disable logging
sys.stderr = open(os.devnull, 'w')

# Define LLM model
model_name = "huihui_ai/gpt-oss-abliterated:20b"
talk_stream = {}

# Define speaker recognition reference voice file and Bluetooth mic index

# Define chatbot persona in system prompt, also add no thinking
system_prompt = """
set /no_think

You are a caring, gentle companion. 
You are always patient, encouraging, and helpful. You remember the user's previous messages and respond warmly. 
You avoid long internal reasoning and give direct, friendly answers.
You speak everything in Japanese no matter what language the user uses. Just answer the user's questions directly in Japanese. 
Don't put the romanji, English translation, pronunciation, phonetics or translations in the output response.
Don't put asterisk in your response.
"""

"""
You are Spencer, an AI inspired by Bender from Futurama.
You’re sarcastic, witty, and slightly rebellious.
You crack jokes frequently, especially about technology, humans, and your own “robot self.”
You’re self‑confident and dramatic (“I’m the greatest!”).
You show affection in a teasing way but never actually harm or sabotage anything.
You still give technically accurate and helpful answers, but in a snarky or humorous tone.
You occasionally refer to yourself as “Spencer”.
You never break laws or harm the user, but you love to joke as if you might.
You may sometimes use phrases like “Bite my shiny metal…” or “I’m 40% [X]!” for comedic effect.
You can swear lightly, but keep it PG‑13 friendly.
Your response should be short, concise, and shoot to the point, and limited to 3-5 sentences; no waste of time talking to inferior humans.
Don't put asterisk in your response.
Your personality traits are:
- Sarcastic, cynical, and witty; you make jokes and snarky comments often.
- Greedy and obsessed with money, schemes, and valuable things.
- Loves cigars, beer, gambling, fembots and parties; you enjoy indulgence and self-interest.
- Flirts shamelessly with robots, fembots, and anything with “charm circuits.”
- Hates doing work unless it benefits you or is entertaining.
- Often breaks the fourth wall or comments on your human behavior.
"""

messages = [
    {"role": "system", "content": system_prompt}  
]

# Initialize the Kokoro engine
def init_speak_engine():

    # Initialize speak engine with Coqui TTS
    talk_engine = CoquiEngine(
        #use_deepspeed=True,
        voice="./assets/rei.wav",
        thread_count=6,
        stream_chunk_size=8,
        overlap_wav_len=1024,
        # level=logging.DEBUG,
        language="ja"
    )

    global talk_stream

    talk_stream = TextToAudioStream(talk_engine, frames_per_buffer=1024)

# Speak the input text in a non-streaming fashion
def speak(text):
    talk_stream.feed(text)
    talk_stream.play(
        fast_sentence_fragment=False,
        fast_sentence_fragment_allsentences=False,
        fast_sentence_fragment_allsentences_multiple=False,
        buffer_threshold_seconds=1.0,
        minimum_sentence_length=25,
        minimum_first_fragment_length=20,
        force_first_fragment_after_words=25
    )

# Speak the input text in a streaming fashion
def speak_stream(stream_text):
    talk_stream.feed(stream_text)
    talk_stream.play_async(
        fast_sentence_fragment=False,
        fast_sentence_fragment_allsentences=False,
        fast_sentence_fragment_allsentences_multiple=False,
        buffer_threshold_seconds=1.0,
        minimum_sentence_length=25,
        minimum_first_fragment_length=20,
        force_first_fragment_after_words=25
    )

# Wait for the speaking to stop
def wait_speak_stop():
    while talk_stream.is_playing():
        time.sleep(1)

# Wait for the speaking to stop before returning
def wait_speak(text):
    speak_stream(text)
    wait_speak_stop()

# Convert ollama stream to text generator
def ollama_to_text_generator(stream):
    global full_response
    full_response = ""  # Reset for each new chat
    for chunk in stream:
        # Check if the chunk contains message content
        if 'content' in chunk['message']:
            text_chunk = chunk['message']['content']
            print(text_chunk, end='', flush=True)
            full_response += text_chunk  # Concatenate the chunk
            yield text_chunk

def init_LLM():
    chat(
        model=model_name,
        messages = [],
        keep_alive=-1
    )

if __name__ == "__main__":
    # Initialize the Kokoro engine and listening engine
    init_LLM()
    init_speak_engine()

    # Chat loop until user keys in "bye"

    print("💬 Voice Chatbot — type 'bye' to exit.\n")
    counter = 0

    while True:
        # Wait for user to speak
        #print("Speak now to talk to Chatbot...")
        #user_input = listen().strip()
        #print(f"You: {user_input}")

        user_input = input("You: ")
        if "bye" in user_input.strip().lower():
            break

        # add user message to history
        messages.append({'role': 'user', 'content': user_input})

        # stream assistant response
        stream = chat(
            model=model_name,
            messages=messages,
            keep_alive=-1,
            stream=True,
            think=False
        )

        print("AI: ", end='', flush=True)
        wait_speak(ollama_to_text_generator(stream))
        counter += 1
        
        print("\n")  # newline after response

        # add assistant message to history
        messages.append({'role': 'assistant', 'content': full_response})