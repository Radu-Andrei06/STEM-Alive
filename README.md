# STEM-Alive
## Skills Integration (2024-2025)

### (Team 4)

| Name                                                         | Class   | GitHub Username                                         |R-number  |
|:-------------------------------------------------------------|:-------:|--------------------------------------------------------:|:--------:|
| [Tofail Tousif](mailto:r1013513@student.thomasmore.be)       | ???     | []() | r1013513 |
| [Kārlis Kalnakārklis](mailto:r1032928@student.thomasmore.be) | 1ACS 02 | []() | r1032928 |
| [Andrei Radu](mailto:r1037303@student.thomasmore.be)         | 1ACS 02 | [Radu-Andrei06](https://github.com/Radu-Andrei06)       | r1037303 |
| [Denys Herasymchuk](mailto:r1018334@student.thomasmore.be)   | 1ACS 02 | [DenysHerasymchuk](https://github.com/DenysHerasymchuk) | r1018334 |


## Gemini AI Client Documentation
![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Gemini](https://img.shields.io/badge/Gemini-1.5+-orange.svg)

Core functions:

| Function          | Description |
|:-----------------:|:------------|
| get_ai_response() | Processes user prompts and returns raw AI-generated text. Accepts model selection (e.g., "gemini-1.5-pro"), response constraints, and persona customization for tailored outputs. |
| ai_to_json()      | Delivers identical functionality but structures responses as JSON objects containing the AI's answer, original prompt, model used, and configuration parameters. |

Both functions feature automatic API key management through environment variables, comprehensive error handling that returns structured error messages, and support for multiple Gemini model versions. The system maintains consistent response formatting while allowing customization of output style and length through configuration parameters.

- [Installation](#installation)
- [Usage](#usage)
- [Functions](#functions)
- [Requirements](#requirements)

### Installation
Install the required packages:
`pip install python-dotenv google-generativeai`

Insert Gemini API key into the .env file:
`GEMINI_API_KEY=api_key_here`

### Usage

#### Getting a Raw AI Response:

``` python
response = get_ai_response(
    prompt="Explain quantum physics simply",
    model="gemini-1.5-pro",
    config="Keep it under 200 characters",
    name="Richard Feynman"
)
```

#### Getting a JSON Formatted Response:
``` python
json_response = ai_to_json(
    prompt="How would you describe the internet?",
    model="gemini-1.5-flash",
    config="Use a metaphor",
    name="Tim Berners-Lee"
)
```

> [!NOTE]
> (Basically the same, but the output really differs)

## Functions
1 ) `get_ai_response(prompt, model, config, name)`
---
> Returns a raw text response from the Gemini AI model.

### Parameters:
- __prompt:__ The input prompt/question
- __model:__ Gemini model to use (e.g., "gemini-1.5-pro")
- __config:__ Configuration instructions for the AI
- __name:__ Persona name the AI should adopt

2 ) `ai_to_json(prompt, model, config, name)`
---
> Returns a JSON formatted response with metadata.

### Parameters:
- __prompt:__ The input prompt/question
- __model:__ Gemini model to use (e.g., "gemini-1.5-pro")
- __config:__ Configuration instructions for the AI
- __name:__ Persona name the AI should adopt

> [!NOTE]
> JSON string with structure:

``` json
{
    "name": "Persona name",
    "response": "AI generated content",
    "settings": {
        "prompt": "Original prompt",
        "model": "Model used",
        "config": "Configuration used"
    }
}
```

### ✅ Example Output

``` json
{
    "name": "Albert Einstein",
    "response": "The weather was irrelevant compared to the cosmic mysteries you discovered.",
    "settings": {
        "prompt": "How was the weather when you died?",
        "model": "gemini-1.5-flash",
        "config": "Maximum of 100 chars."
    }
}
```

### ❌ Error Handling

The functions return error information in JSON format when exceptions occur:

``` json
{
    "name": "Persona name",
    "response": "Error: Error message here",
    "settings": {
        "prompt": "Original prompt",
        "model": "Model used",
        "config": "Configuration used"
    }
}
```

### Tasks:
- [x] Content generation
- [ ] Image Generation
- [ ] Text-To-Speach

### :shipit: Requirements:
- Python 3.8+
- python-dotenv
- google-generativeai

:scroll: __License: MIT__