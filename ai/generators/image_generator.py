from base64 import b64decode
from pathlib import Path
import requests
import sys

def generate_image(
        prompt: str,
        api_key: str,
        name: str,
        output_dir: str = None,
        negative_prompt: str = None,
        language: str = None,
        image_format: str = "JPEG",
        seed: int = None,
        storage_days: int = 0,
        endpoint: str = "https://api.imagepig.com/"
) -> dict:
    """
    Generate an image using the ImagePig API with all available parameters.

    Args:
        prompt (str): Text guiding image generation
        api_key (str): Your API key for authentication
        name (str): Full Name of the scientist
        output_dir (str): Directory to save the image. Defaults to script directory/outputs/
        negative_prompt (str): What you don't want to see
        language (str): ISO 639-1 language code
        image_format (str): Output format (JPEG or PNG)
        seed (int): Seed for deterministic results
        storage_days (int): Days to store image on server (0 for direct download)
        endpoint (str): API endpoint URL

    Returns:
        dict: Complete response from API including metadata
    """
    # Set default outputs directory relative to script location
    if output_dir is None:
        script_dir = Path(sys.argv[0]).parent
        output_dir = script_dir / "outputs"
    else:
        output_dir = Path(output_dir)

    headers = {
        "Content-Type": "application/json",
        "Api-Key": api_key
    }

    # Build payload
    payload = {
        "prompt": f"{name}. {prompt}",
        "format": image_format.upper(),
        "storage_days": storage_days,
        **({"negative_prompt": negative_prompt} if negative_prompt else {}),
        **({"language": language} if language else {}),
        **({"seed": seed} if seed is not None else {}),
    }

    try:
        response = requests.post(endpoint, headers=headers, json=payload)
        response.raise_for_status()
        response_data = response.json()

        print(f"Image generation completed at {response_data.get('completed_at')}")

        if "image_url" in response_data:
            print(f"Image stored at: {response_data['image_url']}")
        elif "image_data" in response_data:
            output_dir.mkdir(parents=True, exist_ok=True)

            filename_base = name.strip().lower().replace(" ", "-")
            filename = f"{filename_base}.{image_format.lower()}"

            filepath = output_dir / filename

            with filepath.open("wb") as f:
                f.write(b64decode(response_data["image_data"]))
            print(f"Image saved to: {filepath.resolve()}")

        return response_data

    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        raise
    except ValueError as e:
        print(f"Failed to parse response: {e}")
        raise


def generate_mouth_variations(
        name: str,
        base_prompt: str,
        api_key: str,
        output_dir: str = None,
        negative_prompt: str = None,
        language: str = None,
        image_format: str = "JPEG",
        seed: int = None,
        storage_days: int = 0,
        endpoint: str = "https://api.imagepig.com/"
) -> list:
    """
    Generate 3 images with different mouth states using the generate_image function.

    Args:
        name (str): Name of the person
        base_prompt (str): Base prompt for all images
        api_key (str): API key for authentication
        output_dir (str): Directory to save images
        negative_prompt (str): Negative prompt for all images
        language (str): Language code
        image_format (str): Output format
        seed (int): Base seed (incremented for each variation)
        storage_days (int): Days to store on server
        endpoint (str): API endpoint

    Returns:
        list: List of tuples (state, response_data) for each variation
    """
    mouth_states = [
        ("closed", "mouth closed, lips together"),
        ("half-open", "mouth slightly open, lips parted"),
        ("open", "mouth fully open")
    ]

    results = []

    for state, desc in mouth_states:
        print(f"\nGenerating {state} mouth version...")
        full_prompt = f"{base_prompt} Realistic portrait, {desc}. With white background."
        variation_name = f"{name} ({state} mouth)"

        # Use different seeds for each variation if a base seed was provided
        variation_seed = seed + hash(state) if seed is not None else None

        result = generate_image(
            prompt=full_prompt,
            api_key=api_key,
            name=variation_name,
            output_dir=output_dir,
            negative_prompt=negative_prompt,
            language=language,
            image_format=image_format,
            seed=variation_seed,
            storage_days=storage_days,
            endpoint=endpoint
        )
        results.append((state, result))

    return results


if __name__ == "__main__":
    # Example usage
    name = "Albert Einstein"
    base_prompt = "High-quality realistic portrait"

    print(f"Generating 3 mouth variations for {name}...")
    variations = generate_mouth_variations(
        name=name,
        base_prompt=base_prompt,
        api_key="ee974eb2-7ebd-44da-9825-fcab85afea71",
        output_dir="einstein_variations",
        image_format="JPEG",
        seed=42
    )

    print("\nGeneration complete. Summary:")
    for state, result in variations:
        print(f"\n{state.replace('-', ' ').title()} mouth version:")
        for key in ["seed", "started_at", "completed_at"]:
            print(f"- {key.replace('_', ' ').title()}: {result.get(key)}")
        if "image_url" in result:
            print(f"- Image URL: {result['image_url']}")
        elif "image_data" in result:
            print("- Image saved to local file")