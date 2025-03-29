# STEM-Alive
![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![Gemini](https://img.shields.io/badge/Gemini-1.5+-orange.svg)

## 1 ) AI Content Generation _(text_generator.py)_

Advanced conversation handler with memory and persona support.

Maintains contextual dialogues with Gemini AI while tracking metadata and performance metrics.

🍔 **Core functions:**

|          Function           | Description |
|:---------------------------:|:------------|
|      `get_ai_response()`      | Decorated function that handles AI interactions with JSON formatting |
| `get_conversation_history()`  | Retrieves conversation logs with message counts |
|       `clear_history()`       | Manages conversation data lifecycle |

- [Installation](../README.md#installation)
- [Usage](#usage-examples)
- [Functions](#-function-specifications)
- [Requirements](../README.md#shipit-requirements)

### Usage examples
#### 1. Basic Interaction
```python
response = get_ai_response(
    prompt="Explain quantum entanglement",
    character="Richard Feynman",
    user_id=1001,
    config="Limit to 150 words"
)
```
#### 2. Contextual Follow-up
```python
# First question
get_ai_response(
    prompt="What's special about 1947?",
    character="Albert Einstein",
    user_id=1001
)

# Follow-up (automatically includes previous exchange)
get_ai_response(
    prompt="How did that influence your work?",
    character="Albert Einstein", 
    user_id=1001
)
```
#### 3. History Management
```python
# Get full conversation log
history = get_conversation_history(user_id=1001)

# Clear specific character history
clear_history(user_id=1001, character="Nikola Tesla")
```
`clear_history()` is responsible for conversation data lifecycle management, this function offers precise control over history deletion. It supports both bulk removal of all user conversations and targeted deletion of specific character dialogues. The operation returns a detailed status message indicating success or failure, including cases where requested data doesn't exist. The function maintains strict data isolation between users and preserves atomicity of operations, ensuring clean state management.

### 📋 Function Specifications
`get_ai_response(prompt, model, config, character, user_id, use_history)`
---
The primary interface for interacting with the Gemini AI, this function processes user prompts and generates contextual responses while maintaining conversation state. It accepts parameters for model selection, response constraints, and persona customization, returning a structured JSON object containing the AI's response along with metadata including timestamps, response times, and configuration details. The function automatically manages conversation history, keeping track of the last three interactions when context is enabled, and provides comprehensive error handling that maintains consistent output formatting even during failures.

> [!NOTE]
> Returns: JSON string with complete interaction record

> Parameters:

| Param | Type | Default | Description |
|:-----:|:-----|:--------|:------------|
| `prompt` | str | Required | User's input question |
| `model` | str | gemini-1.5-flash | Gemini model variant |
| `config` | str | "Max 100 chars" | Response constraints |
| `character`	| str | "Albert Einstein" | AI persona |
| `user_id` | int | 0 | Conversation isolation key |
| `use_history` | bool | True | Contextual memory toggle |

> Response structure:

```json
{
  "question": "Original prompt",
  "response": {
    "character": "Persona name",
    "answer": "Generated content"
  },
  "config": {
    "model": "gemini-1.5-flash",
    "max_length": 100,
    "context_used": true
  },
  "metadata": {
    "timestamp": "ISO-8601",
    "response_time_ms": 1250,
    "user_id": 1001
  }
}
```

`get_conversation_history(user_id, character=None)`
---
This retrieval function provides access to stored conversation logs, offering both comprehensive user histories and character-specific filtering capabilities. It returns a JSON-formatted structure containing the complete message history along with analytical metadata such as message counts and timestamps. The function verifies existence of requested data and returns appropriate status messages when no history is found, ensuring reliable integration with frontend systems. Output maintains the original message structure including questions, responses, and generation parameters.

> [!NOTE]
> Returns: JSON-formatted conversation log

> Example output:

```json
{
  "user_id": 1001,
  "character": "Albert Einstein",
  "history": [
    /* Array of message objects */
  ],
  "count": 5,
  "last_updated": "2024-03-15T14:30:00Z"
}
```

### ⚠️ Error Handling
**Consistent error format across all functions:**
```json
{
  "status": "error",
  "message": "Detailed error description",
  "user_id": 1001,
  "character": "Albert Einstein",
  "timestamp": "2024-03-15T14:32:00Z"
}
```

<div align="right">
    <a href="https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExbGhpcnUxanJsZmV6czliNXJuMnVkajZ1Znp1Z2F6cnJnaDl4OGh1MCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/DHAa1UQA95eWTZMOxQ/giphy.gif">
        <img src="https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExbGhpcnUxanJsZmV6czliNXJuMnVkajZ1Znp1Z2F6cnJnaDl4OGh1MCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/DHAa1UQA95eWTZMOxQ/giphy.gif" alt="Animated duck GIF" width="300" />
    </a>
</div>
