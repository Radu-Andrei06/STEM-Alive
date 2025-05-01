from base64 import b64decode
from pathlib import Path
import requests

from os import getenv
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

API_KEY = getenv("IMAGEPIG_API_KEY")
if not API_KEY:
    raise ValueError("IMAGEPIG_API_KEY not found in environment variables")


def generate_image(
        prompt: str,
        output_path: str = None,
        negative_prompt: str = None,
        image_format: str = "JPEG",
        seed: int = None,
        endpoint: str = "https://api.imagepig.com/"
    ) -> dict:

    """

    Generate a single image using the ImagePig API.

    Args:
        prompt (str): Text guiding image generation
        output_path (str): Full path to save the image (including filename)
        negative_prompt (str): What you don't want to see
        image_format (str): Output format (JPEG or PNG)
        seed (int): Seed for deterministic results
        endpoint (str): API endpoint URL

    Returns:
        dict: Complete response from API including metadata

    """

    # Set default output path if not provided
    if output_path is None:
        output_path = Path("../outputs") / f"generated_image.{image_format.lower()}"
    else:
        output_path = Path(output_path)

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    headers = {
        "Content-Type": "application/json",
        "Api-Key": API_KEY
    }

    payload = {
        "prompt": prompt,
        "format": image_format.upper(),
        **({"negative_prompt": negative_prompt} if negative_prompt else {}),
        **({"seed": seed} if seed is not None else {}),
    }

    try:
        response = requests.post(endpoint, headers=headers, json=payload)
        response.raise_for_status()
        response_data = response.json()

        # Save the image if we got image data
        if "image_data" in response_data:
            with open(output_path, "wb") as f:
                f.write(b64decode(response_data["image_data"]))
            print(f"Image successfully saved to: {output_path.resolve()}")
        elif "image_url" in response_data:
            print(f"Image stored at: {response_data['image_url']}")

        return response_data

    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        raise
    except ValueError as e:
        print(f"Failed to parse response: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise


if __name__ == "__main__":
    # Example usage
    try:
        result = generate_image(
            prompt="A realistic portrait of a scientist in a lab",
            negative_prompt="blurry, distorted, low quality",
            image_format="JPEG",
            seed=42
        )

        print("\nGeneration results:")
        print(f"Status: {result.get('status', 'unknown')}")
        print(f"Generation ID: {result.get('id', 'N/A')}")
    except Exception as e:
        print(f"Image generation failed: {e}")