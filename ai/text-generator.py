from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)


def get_ai_response(prompt, model="gemini-1.5-flash"):
    """
    Get AI response with customizable settings

    Args:
        prompt (str): Your question/input
        model (str): Model version to use
    Returns:
        str: AI generated response
    """
    response = client.models.generate_content(
        model=model,
        contents=prompt,
    )
    return response.text


name = "Albert Einstein"
config = f"Maximum of 100 chars. You are {name}. "
question = "How was the weather when you died?"

response = get_ai_response(
    f"{config} {question}",
    model="gemini-1.5-flash",
)

print(response)