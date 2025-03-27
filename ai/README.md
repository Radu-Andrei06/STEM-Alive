# STEM-Alive
![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Gemini](https://img.shields.io/badge/Gemini-1.5+-orange.svg)

## 1 . AI Content Generation _(text-generator.py)_

Core functions:

| Function          | Description |
|:-----------------:|:------------|
| get_ai_response(-) | Processes user prompts and returns raw AI-generated text. Accepts model selection (e.g., "gemini-1.5-pro"), response constraints, and persona customization for tailored outputs. |
| ai_to_json(-)      | Delivers identical functionality but structures responses as JSON objects containing the AI's answer, original prompt, model used, and configuration parameters. |

Both functions feature automatic API key management through environment variables, comprehensive error handling that returns structured error messages, and support for multiple Gemini model versions. The system maintains consistent response formatting while allowing customization of output style and length through configuration parameters.

- [Installation](#installation)
- [Usage](#usage)
- [Functions](#functions)
- [Requirements](../README.md#shipit-requirements)

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

<div align="right">
    <a href="https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExbGhpcnUxanJsZmV6czliNXJuMnVkajZ1Znp1Z2F6cnJnaDl4OGh1MCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/DHAa1UQA95eWTZMOxQ/giphy.gif">
        <img src="https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExbGhpcnUxanJsZmV6czliNXJuMnVkajZ1Znp1Z2F6cnJnaDl4OGh1MCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/DHAa1UQA95eWTZMOxQ/giphy.gif" alt="Animated duck GIF" width="300" />
    </a>
</div>