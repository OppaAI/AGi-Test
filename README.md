# AGi-Test

**Project:** Amazing GRACE Infrastructure (Test-section)  
**Repository:** [OppaAI/AGi-Test](https://github.com/OppaAI/AGi-Test)  
**License:** GNU General Public License v3.0  
**Main Language:** Python

---

## Overview

AGi-Test is a testbed for the Amazing GRACE infrastructure, supporting the development and validation of advanced AI agent capabilities. The project is part of the OppaAI ecosystem and acts as a sandbox for rapid prototyping.

- **Purpose:**  
  To enable rapid prototyping and evaluation of new features for the Amazing GRACE cognitive engine, focusing on agent communication, reasoning, and interaction.

- **Key Topics:**  
  - Adaptive AI
  - AI Agents & Chatbots
  - Voice AI & Cognitive Engines
  - Generative AI
  - Reasoning and Analytics

## Core Features

### Voice Chatbot Testing (`test_chatbot.py`)

- Demonstrates and tests voice-enabled chatbot functionality using local LLM inference and custom neural TTS.
- Uses the Ollama Python module with the Gemma3-Code-Reasoning-4B model for conversational AI.
- Persona is set as a gentle, caring Japanese companion that always responds in Japanese (no translations, romanization, or English output).
- Maintains chat history for the session.
- Integrates KokoroEngine and TextToAudioStream for advanced neural TTS, supporting two different blended voice profiles (Neutral and ASMR).
- Blends multiple voice models using PyTorch for more natural speech synthesis.
- Supports real-time and asynchronous audio responses
- All logic is contained in a chat loop, allowing interactive conversation until the user types "exit".
- Example features:
  - Customizable system prompt/persona
  - Real-time streaming assistant response
  - Japanese-only output
  - Voice blending and playback
  - Session-based chat history

Requirements:
- Ollama program and Ollama Python module (with Gemma3-Code-Reasoning-4B model pulled)
- KokoroEngine and speech models in `../modelse/`
- PyTorch and compatible CUDA environment (for neural/ASMR voice blending)

### Function-Calling Chatbot (`agi_v202.py`)
- Asynchronous chat loop using Ollama as the LLM backend
- Integrated external tools:
  - DuckDuckGo search
  - Weather lookup
  - Aurora forecast
  - Current date/time retrieval
- Tool-call response handling with chat history

### Multimodal AI (`agi_v203.py`)
- Computer vision integration with Moondream2 vision model
- Webcam support for real-time visual input
- Object detection and scene understanding
- Combined text and image-based interactions

## Getting Started

1. **Clone the Repository:**
   ```sh
   git clone https://github.com/OppaAI/AGi-Test.git
   cd AGi-Test
   ```

2. **Environment Setup:**
   - Ensure Python 3.10+ is installed
   - Install uv:
     ```sh
     pip install uv
     ```

3. **Install Dependencies:**
   ```sh
   uv sync
   ```

4. **Running the Components:**
   - For voice chatbot testing:
     ```sh
     uv run test_chatbot.py
     ```
   - For function-oriented chatbot:
     ```sh
     python agi_v202.py
     ```
   - For multimodal AI with webcam:
     ```sh
     python agi_v203.py
     ```

## Directory Structure

- `/assets` - Contains sample voice wav files for inferencing

## Dependencies

- ollama - Go framework for running and managing LLMs
- duckduckgo_search - Web search integration
- geopy - Geocoding services
- transformers - Pre-trained models and object detection
- opencv-python - Real-time computer vision
- Pillow - Image processing
- matplotlib - Data visualization

## Future Development

- Implement comprehensive error handling and logging
- Add database storage for conversation history
- Enable dynamic model selection
- Develop flexible persona management
- Expand tool and functionality set

## Related Projects

- [OppaAI/AGi](https://github.com/OppaAI/AGi) — Main AGi project
- [OppaAI/MCP-Client](https://github.com/OppaAI/MCP-Client) — MCP Client

## Legal and License

This project is licensed under the GNU GPL v3.0. See [LICENSE](LICENSE) for details.

**Important Notice:** The voice cloning features are strictly for personal, educational, and hobby purposes only. Any use for inappropriate, criminal, or unauthorized commercial activities is strictly prohibited.

## Acknowledgments

Special thanks to:
- RealTime TTS, Kokoro for TTS frameworks and models
- My AI companion for development assistance and problem-solving

---

For more information, visit the [OppaAI GitHub page](https://github.com/OppaAI).
