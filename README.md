# STEM-Alive
![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![Gemini](https://img.shields.io/badge/Gemini-1.5+-orange.svg)

## Skills Integration (2024-2025)

### (Team 4)

| Name                                                         | Class    | GitHub Username                                         |R-number  |
|:-------------------------------------------------------------|:--------:|--------------------------------------------------------:|:--------:|
| [Tofail Tousif](mailto:r1013513@student.thomasmore.be)       | ???      | []() | r1013513 |
| [Kārlis Kalnakārklis](mailto:r1032928@student.thomasmore.be) | 1 ACS 02 | [karliskalnakarklis](https://github.com/karliskalnakarklis) | r1032928 |
| [Andrei Radu](mailto:r1037303@student.thomasmore.be)         | 1 ACS 02 | [Radu-Andrei06](https://github.com/Radu-Andrei06)       | r1037303 |
| [Denys Herasymchuk](mailto:r1018334@student.thomasmore.be)   | 1 ACS 02 | [DenysHerasymchuk](https://github.com/DenysHerasymchuk) | r1018334 |

### Installation
Install the required packages:
`pip install -r requirements.txt`

Insert Gemini API key into the .env file:
`GEMINI_API_KEY=api_key_here`

### 🍔 Project Structure:
``` yaml
STEM-Alive/
│── 📜 .env                     # Environment variables
│── 📜 .gitignore               # Git ignore rules
│── 📜 README.md                # Project documentation
│── 📜 requirements.txt         # Python dependencies
│
├───🧪 tests/                   # Test suite
│   │   📜 conftest.py          # Pytest fixtures
│   │   📜 __init__.py          # Package initialization
│   │
│   └───🔬 unit/                # Unit tests
│       ├───🖼️ generators/
│       │       📜 test_image.py
│       │       📜 test_text.py
│       │
│       └───🗣️ tts/
│               📜 test_core.py
│
└───🧠 ai/                      # Core AI functionality
    │── 📜 README.md            # Module documentation
    │── 📜 __init__.py          # Package initialization
    │
    ├───🎨 generators/          # Content generation
    │       📜 image_generator.py  # DALL·E/Stable Diffusion
    │       📜 text_generator.py   # Gemini/LLM text
    │       📜 __init__.py         # Subpackage init
    │
    ├───📂 outputs/             # Generated artifacts
    │       📄 .gitkeep         # Preserve directory structure
    │
    └───🔊 tts/                 # Text-to-speech
            📜 text_to_speech.py  # ElevenLabs/Google TTS
            📜 __init__.py        # Subpackage init
```

### :shipit: Requirements
- Python 3.8+
- python-dotenv
- google-generativeai
