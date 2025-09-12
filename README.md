# AGi-Test

**Project:** Amazing GRACE Infrastructure (Test-section)  
**Repository:** [OppaAI/AGi-Test](https://github.com/OppaAI/AGi-Test)  
**License:** GNU General Public License v3.0  
**Main Language:** Python

---

## Overview

AGi-Test is a testbed for the Amazing GRACE infrastructure, supporting the development and validation of advanced AI agent capabilities. The project is part of the OppaAI ecosystem and acts as a sandbox for experimenting with adaptive, reasoning, and generative AI technologies.

- **Purpose:**  
  To enable rapid prototyping and evaluation of new features for the Amazing GRACE cognitive engine, focusing on agent communication, reasoning, and interaction.

- **Key Topics:**  
  - Adaptive AI
  - AI Agents & Chatbots
  - Voice AI & Cognitive Engines
  - Generative AI
  - Reasoning and Analytics

---

## Features

- Modular testing environment for AI agents
- Support for conversational and voice-based agents
- Tools for experimenting with agent reasoning and analytics
- Integration points for social media and content analysis agents

---

## Key Python Files & Their Functionality

### `test_voice.py`

- **Functionality:**  
  Demonstrates advanced text-to-speech (TTS) and voice conversion capabilities.
  - Loads a TTS model to synthesize a spoken version of a monologue using a reference speaker’s voice.
  - Uses a voice conversion model to convert the audio to match another target speaker.
  - Includes audio processing: resampling, pitch and speed adjustment, and playback.
  - Useful for testing synthetic voice generation, speaker cloning, and real-time audio playback with customizations.

### `agi_v202.py`

- **Functionality:**  
  Main function-calling chatbot version.
  - Implements an asynchronous chat loop using Ollama as the LLM backend.
  - Integrates external tools via function calling: DuckDuckGo search, weather lookup, aurora forecast, and current date/time.
  - Handles tool-call responses, appends them to chat history, and returns a final AI response.
  - Designed for general-purpose agentic conversations with real-world information retrieval.

### `agi_v203.py`

- **Functionality:**  
  Advanced multimodal version, adding computer vision.
  - Integrates with a webcam and the Moondream2 vision model to allow the AI to “see” through the camera.
  - Can capture webcam images, run object detection, and send encoded images to the LLM for description or reasoning.
  - Supports both text and image-based conversations, enabling richer interactions (e.g., “look” or “see” commands).
  - Useful for experiments in multimodal AI, combining visual and textual understanding.

---

## Getting Started

1. **Clone the Repository:**
   ```sh
   git clone https://github.com/OppaAI/AGi-Test.git
   cd AGi-Test
   ```

2. **Environment Setup:**
   - Ensure you have Python 3.8+ installed.
   - (Optional) Create and activate a virtual environment:
     ```sh
     python -m venv venv
     source venv/bin/activate  # On Windows: venv\Scripts\activate
     ```

3. **Install Dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Run Tests or Example Agents:**
   - Check the `/tests` or `/examples` directories for available agent scripts and test cases.
   - Run agents or tests using:
     ```sh
     python path/to/your_agent_or_test.py
     ```

---

## Directory Structure

- `/tests` — Test cases for agent features and infrastructure components
- `/examples` — Sample agents and usage scenarios
- `/docs` — Documentation and architecture references
- `requirements.txt` — Python dependencies

---

## Usage

* To run the function-oriented version:
  ```sh
  python agi_v202.py
  ```

* To run the webcam integrated version:
  ```sh
  python agi_v203.py
  ```

Once the script is running, you can interact with the AI by typing in your input in the terminal. The AI will respond based on the available tools and the webcam input (if running `agi_v203.py`). Type `exit` or `quit` to end the conversation. For `agi_v203.py`, type `look` or `see` to enable the AI to see through the webcam.

---

## Contributing

Contributions and feedback are welcome! Please open issues or submit pull requests as needed.

---

## License

This project is licensed under the GNU GPL v3.0. See [LICENSE](LICENSE) for details.

---

## Related Projects

- [OppaAI/AGi](https://github.com/OppaAI/AGi) — Main AGi project
- [OppaAI/MCP-Client](https://github.com/OppaAI/MCP-Client) — MCP Client

---

## About

AGi-Test is a public, experimental repository for developing next-generation AI agent infrastructure. For more information, visit the [OppaAI GitHub page](https://github.com/OppaAI).

agi_v203.py - chatbot with computer vision using webcam using MoonDream2 vision model and Google Gemma3 LLM that is a multimodal LLM
agi_v202.py - chatbot with agentic tools (check weather, check aurora %) using Google Gemma3 LLM with added tool call capability

## Features

*   **Ollama Integration:** Uses Ollama directly for interacting with the language model.
*   **Function Calling:** Employs Ollama's function calling feature to utilize tools.
*   **DuckDuckGo Search:** Integrates a tool for searching the web using DuckDuckGo (`agi_v202.py`).
*   **Weather Information:** Includes a tool for fetching weather information for a given location (`agi_v202.py`).
*   **Aurora Checking:** Includes a tool for checking the probability of seeing the aurora at a given location (`agi_v202.py`).
*   **Current Date and Time:** Includes a tool for fetching the current date and time (`agi_v202.py`).
*   **Webcam Integration:** Integrates webcam to allow AI to see through the camera (`agi_v203.py`).
*   **Object Detection:** Implements object detection using the Moondream model (`agi_v203.py`, `eye.py`).

## Getting Started

### Prerequisites

*   Python 3.10+
*   Ollama

### Installation

1.  Clone the repository:

    ```bash
    git clone [https://github.com/OppaAI/AGi.git]
    cd AGi
    ```
2.  Create a virtual environment (recommended):

    ```bash
    python -m venv venv
    ```
3.  Activate the virtual environment:

    *   On Windows:

        ```bash
        .\venv\Scripts\activate
        ```
    *   On macOS/Linux:

        ```bash
        source venv/bin/activate
        ```
4.  Install the dependencies:

    ```bash
    pip install ollama duckduckgo_search geopy requests transformers pillow opencv-python matplotlib
    ```
5.  Set up Ollama:
    *   Download and install Ollama from [https://ollama.com/](https://ollama.com/).
    *   Pull a compatible model, e.g., `ollama pull fomenks/gemma3-tools:4b`

### Usage

*   To run the function-oriented version:

    ```bash
    python agi_v202.py
    ```

*   To run the webcam integrated version:

    ```bash
    python agi_v203.py
    ```

Once the script is running, you can interact with the AI by typing in your input in the terminal. The AI will respond based on the available tools and the webcam input (if running `agi_v203.py`). Type `exit` or `quit` to end the conversation. For `agi_v203.py`, type `look` or `see` to enable the AI to see through the webcam.

## Code Structure

*   [`agi_v202.py`](https://github.com/OppaAI/AGi/blob/main/agi_v202.py): Contains the main application logic for function calling, including:
    *   Tool definitions (DuckDuckGo Search, Weather Information, Aurora Checking, Current Date and Time)
    *   Skill definitions for function calling
    *   Asynchronous chat loop using `asyncio`
    *   Interaction with the Ollama model
*   [`agi_v203.py`](https://github.com/OppaAI/AGi/blob/main/agi_v203.py): Contains the main application logic for the webcam integrated version, including:
    *   Webcam initialization and frame capture.
    *   Integration with the `VisionSystem` in `eye.py`.
    *   Asynchronous chat loop using `asyncio`.
    *   Interaction with the Ollama model, sending image descriptions.
*   [`eye.py`](https://github.com/OppaAI/AGi/blob/main/eye.py): Contains the `VisionSystem` class for handling webcam and object detection, including:
    *   Model loading for object detection.
    *   Frame capture and processing.
    *   Object detection logic using the `transformers` library.
    *   Visualization of detection results.
*   [`assets/`](https://github.com/OppaAI/AGi/blob/main/assets/): Contains any assets used by the application.

## Dependencies

*   [ollama](https://github.com/jmorganca/ollama): Go framework for run and manage LLMs.
*   [duckduckgo_search](https://github.com/deedy5/duckduckgo_search): Library for searching DuckDuckGo.
*   [geopy](https://geopy.readthedocs.io/en/stable/): Library for geocoding.
*   [requests](https://requests.readthedocs.io/en/latest/): Library for making HTTP requests.
*   [transformers](https://huggingface.co/docs/transformers/index): Provides pre-trained models and tools for object detection.
*   [Pillow](https://pillow.readthedocs.io/en/stable/): Python Imaging Library for image processing.
*   [opencv-python](https://opencv.org/): Library for real-time computer vision.
*   [matplotlib](https://matplotlib.org/): Comprehensive library for creating static, animated, and interactive visualizations in Python.

## Limitations

*   The project lacks a comprehensive error handling and logging mechanism.
*   The project does not store conversation history in a database.
*   The webcam integrated version (`agi_v203.py`) relies on a specific object detection model and revision (`vikhyatk/moondream2`, `2025-04-14`).
*   The persona in `agi_v203.py` is hardcoded.

## Future Work

*   Implement more comprehensive error handling and logging.
*   Incorporate a database for storing conversation history.
*   Allow dynamic selection of object detection models and revisions.
*   Implement a more flexible persona management system.
*   Add more tools and functionalities to enhance the AI's capabilities.

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](https://github.com/OppaAI/AGi/blob/main/LICENSE) file for details.

## Acknowledgments

*   My AI companion (in GPT) for helping me generate the Python code and think of solutions to solve problems and bugs.
