# AGi-Test

A testbed for the **Amazing GRACE Infrastructure**, enabling rapid prototyping and validation of advanced AI agent capabilities. Part of the [OppaAI](https://github.com/OppaAI) ecosystem.

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)
![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue)

## 🎯 Overview

AGi-Test is a sandbox environment for developing and testing cutting-edge AI agent features, with a focus on:

- **Voice-Enabled AI** - Japanese-speaking companions with neural TTS and voice blending
- **Function-Calling Agents** - LLM-powered chatbots with external tool integration
- **Multimodal AI** - Computer vision and real-time visual understanding
- **Local LLM Inference** - Privacy-first AI using Ollama and open-source models

## ✨ Features

### 🎤 Voice Chatbot (`kokoro_chatbot.py` / `coqui_chatbot.py`)

Interactive voice-based AI companion with advanced speech synthesis:

- **LLM Backend**: Ollama with Gemma3-Code-Reasoning-4B
- **TTS Engine**: Kokoro or Coqui with neural voice blending
- **Persona**: Customizable Japanese-speaking companion
- **Voice Profiles**: Neutral and ASMR voice blending using PyTorch
- **Features**:
  - Real-time streaming responses
  - Session-based chat history
  - Japanese-only output mode
  - Multi-voice synthesis and blending
  - Interactive chat loop (type "exit" to quit)

**Requirements**:
- Ollama with Gemma3-Code-Reasoning-4B model
- Kokoro/Coqui TTS models in `/models`
- CUDA-compatible GPU (recommended for voice blending)

### 🔧 Function-Calling Chatbot (`archive/agi_v202.py`)

Async chatbot with integrated external tools:

- **Tools**: DuckDuckGo search, weather lookup, aurora forecasts, date/time
- **Architecture**: Async chat loop with tool-call handling
- **Memory**: Persistent chat history per session

### 👁️ Multimodal AI (`archive/agi_v203.py`)

Computer vision integration for real-time scene understanding:

- **Vision Model**: Moondream2
- **Input**: Webcam or image files
- **Capabilities**: Object detection, scene analysis, visual reasoning
- **Interaction**: Combined text and image-based queries

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- [Ollama](https://ollama.ai) installed and running
- NVIDIA GPU with CUDA support (optional but recommended)

### Installation

```bash
# Clone the repository
git clone https://github.com/OppaAI/AGi-Test.git
cd AGi-Test

# Install dependencies
pip install -r requirements.txt

# Or use uv for faster installation
pip install uv
uv sync
```

### Running the Chatbots

```bash
# Voice chatbot with Kokoro TTS
python kokoro_chatbot.py

# Voice chatbot with Coqui TTS
python coqui_chatbot.py

# Function-calling chatbot (archived)
python archive/agi_v202.py

# Multimodal AI with webcam (archived)
python archive/agi_v203.py
```

## 📁 Project Structure

```
AGi-Test/
├── kokoro_chatbot.py          # Main voice chatbot (Kokoro TTS)
├── coqui_chatbot.py           # Alternative voice chatbot (Coqui TTS)
├── requirements.txt           # Python dependencies
├── models/                    # Pre-trained voice models
│   ├── neutral_voice.pt
│   ├── ASMR_voice.pt
│   └── [other voice models]
├── assets/                    # Sample audio and metadata
│   ├── sample.wav
│   ├── bender.wav
│   └── *.json
└── archive/                   # Previous implementations
    ├── agi_v202.py           # Function-calling chatbot
    ├── agi_v203.py           # Multimodal AI
    └── eye.py                # Vision system
```

## 🔧 Key Dependencies

| Package | Purpose |
|---------|---------|
| `ollama` | Local LLM inference |
| `kokoro` / `coqui-tts` | Neural text-to-speech |
| `torch` | Deep learning framework |
| `transformers` | Pre-trained models |
| `opencv-python` | Computer vision |
| `realtimetts` | Real-time audio streaming |
| `duckduckgo-search` | Web search integration |

See `requirements.txt` for the complete dependency list.

## 🎓 Use Cases

- **AI Companion Development** - Build and test voice-based AI assistants
- **Voice Synthesis Research** - Experiment with neural TTS and voice blending
- **Agent Prototyping** - Rapidly develop and validate new agent capabilities
- **Multimodal AI** - Combine language and vision for richer interactions
- **Privacy-First AI** - Run everything locally without cloud dependencies

## 🔮 Future Roadmap

- [ ] Comprehensive error handling and logging
- [ ] Database storage for conversation history
- [ ] Dynamic model selection and switching
- [ ] Flexible persona management system
- [ ] Extended tool ecosystem
- [ ] Web UI for easier interaction
- [ ] Model fine-tuning capabilities

## 📚 Related Projects

- [OppaAI/AGi](https://github.com/OppaAI/AGi) — Main AGi project
- [OppaAI/MCP-Client](https://github.com/OppaAI/MCP-Client) — MCP Client implementation

## ⚖️ License & Legal

This project is licensed under the **GNU General Public License v3.0**. See [LICENSE](LICENSE) for details.

### ⚠️ Important Notice

The voice cloning and synthesis features are strictly for **personal, educational, and hobby purposes only**. Any use for inappropriate, criminal, or unauthorized commercial activities is strictly prohibited.

## 🙏 Acknowledgments

Special thanks to:
- [RealtimeTTS](https://github.com/KoljaB/RealtimeTTS) - Real-time audio streaming library
- [Kokoro](https://github.com/remsky/Kokoro-JVSX) - Neural TTS framework
- [Coqui TTS](https://github.com/coqui-ai/TTS) - Open-source text-to-speech
- [Ollama](https://ollama.ai) - Local LLM inference
- [Moondream](https://github.com/vikhyat/moondream) - Vision model
- [DuckDuckGo Search](https://github.com/duckduckgo) - Web search API
- [OpenCV](https://github.com/opencv/opencv) - Computer vision library
- [Transformers](https://github.com/huggingface/transformers) - Pre-trained models
- The open-source AI community

---

**Questions or contributions?** Visit the [OppaAI GitHub](https://github.com/OppaAI) or open an issue!
