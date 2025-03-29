import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

def text_to_speech_json(
        text: str,
        model: str = "aura-asteria-en",
        **params
    ) -> str:

    """

    Returns JSON string with raw audio bytes (Latin1 encoded for efficiency).
    Usage:
        json_output = text_to_speech_json("Hello world")
        print(json_output)  # Ready for API response

    """

    api_key = os.getenv("DEEPGRAM_API_KEY")
    result = {
        "success": False,
        "model": model,
        "text": text,
        "audio_bytes": None,
        "content_type": "audio/mpeg",
        "error": None
    }

    try:
        # Validate input
        if not api_key:
            raise ValueError("DEEPGRAM_API_KEY not set in .env")
        if not isinstance(text, str) or not text.strip():
            raise ValueError("Text must be a non-empty string")

        # Call Deepgram API
        response = requests.post(
            f"https://api.deepgram.com/v1/speak?model={model}",
            json={"text": text, **params},
            headers={
                "Authorization": f"Token {api_key}",
                "Content-Type": "application/json",
                "Accept": "audio/mpeg"
            },
            timeout=15
        )
        response.raise_for_status()

        # Convert binary audio to JSON-safe string (Latin1 trick)
        result.update({
            "success": True,
            "audio_bytes": response.content.decode('latin1'),  # Raw bytes as string
            "content_type": response.headers.get("Content-Type", "audio/mpeg"),
            "size_bytes": len(response.content)
        })

    except requests.exceptions.RequestException as e:
        result["error"] = f"API Error: {str(e)}"
    except Exception as e:
        result["error"] = f"Processing Error: {str(e)}"

    return json.dumps(result)

# ## Example usage
# if __name__ == "__main__":
#     # Get JSON response (ready for APIs)
#     json_response = text_to_speech_json(
#         text="Pondering relativity, sipped coffee...",
#         model="aura-stella-en"
#     )
#     print(json_response)
#
#     # To reconstruct audio bytes from JSON:
#     # data = json.loads(json_response)
#     # audio_bytes = data["audio_bytes"].encode('latin1')