import os
import json
from dotenv import load_dotenv
from google import genai

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize the Gemini AI client
client = genai.Client(api_key=GEMINI_API_KEY)

def get_ai_response(
        prompt: str,
        model: str,
        config: str,
        name: str
    ) -> str:

    """

    Get AI response with customizable settings by querying the Gemini AI model.
    Returns the raw text response from the AI.

    """

    try:
        full_prompt = f"{config} {prompt}\nYou are {name}"
        response = client.models.generate_content(
            model=model,
            contents=full_prompt,
        )
        return response.text
    except Exception as e:
        raise Exception(f"Failed to get AI response: {str(e)}")


def ai_to_json(
        prompt: str = "How was the weather when I died?",
        model: str = "gemini-1.5-flash",
        config: str = "Maximum of 100 chars.",
        name: str = "Albert Einstein"
    ) -> str:

    """

    Get AI response formatted as a JSON string with metadata.

    Returns:
        str: A JSON string containing:
            - name: The persona name
            - response: AI-generated content
            - settings: Dictionary of input parameters

    """

    try:
        # Get the AI response
        ai_response = get_ai_response(
            prompt=prompt,
            model=model,
            config=config,
            name=name
        )

        # Create the dictionary structure
        response_dict = {
            "name": name,
            "response": ai_response,
            "settings": {
                "prompt": prompt,
                "model": model,
                "config": config
            }
        }

        # Convert to JSON string with ensure_ascii=False for proper Unicode handling
        return json.dumps(response_dict, ensure_ascii=False)

    except Exception as e:
        # Return error information as JSON string
        error_dict = {
            "name": name,
            "response": f"Error: {str(e)}",
            "settings": {
                "prompt": prompt,
                "model": model,
                "config": config
            }
        }
        return json.dumps(error_dict, ensure_ascii=False)

# Example usage ###
#
# if __name__ == "__main__":
#
#     # Get response
#     json = ai_to_json(
#         prompt="How did you die?",
#         model="gemini-1.5-pro",
#         config="Use simple analogies",
#         name="Nikola Tesla"
#     )
#
#     print("\nJSON Response:")
#     print(json)