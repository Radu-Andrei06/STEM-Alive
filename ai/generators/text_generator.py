import os
from datetime import datetime
from dotenv import load_dotenv
from google import genai
from collections import defaultdict
from functools import wraps

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize the Gemini AI client
client = genai.Client(api_key=GEMINI_API_KEY)

# In-memory conversation history storage
# Structure: {user_id: {character: [messages]}}
conversation_history = defaultdict(lambda: defaultdict(list))

def ai_response_decorator(func):

    """

    Decorator that transforms the raw AI response into structured dict output
    with metadata and conversation history management.

    """

    @wraps(func)
    def wrapper(
            prompt: str,
            model: str = "gemini-1.5-flash",
            config: str = "Maximum of 100 chars.",
            character: str = "Albert Einstein",
            user_id: int = 0,
            use_history: bool = True
    ) -> dict:

        start_time = datetime.now()

        try:
            # Call the original function
            ai_response = func(
                prompt=prompt,
                model=model,
                config=config,
                character=character,
                user_id=user_id,
                use_history=use_history
            )

            response_time = (datetime.now() - start_time).total_seconds() * 1000

            # Build the structured response
            response_dict = {
                "question": prompt,
                "response": {
                    "character": character,
                    "answer": ai_response
                },
                "config": {
                    "model": model,
                    "max_length": int(config.split()[2]) if "max" in config.lower() else None,
                    "context_used": use_history
                },
                "metadata": {
                    "timestamp": datetime.now().isoformat(),
                    "response_time_ms": round(response_time),
                    "user_id": user_id
                }
            }

            # Store in conversation history
            conversation_history[user_id][character].append(response_dict)

            return response_dict

        except Exception as e:
            error_dict = {
                "question": prompt,
                "response": {
                    "character": character,
                    "answer": f"Error: {str(e)}"
                },
                "config": {
                    "model": model,
                    "max_length": None,
                    "context_used": False
                },
                "metadata": {
                    "timestamp": datetime.now().isoformat(),
                    "response_time_ms": 0,
                    "user_id": user_id
                }
            }
            return error_dict
    return wrapper


@ai_response_decorator
def get_ai_response(
        prompt: str,
        model: str,
        config: str,
        character: str,
        user_id: int = 0,
        use_history: bool = True
    ) -> str:

    """

    Core function that handles the AI interaction

    """

    try:
        # Build context from history
        context_parts = []
        if use_history:
            for interaction in conversation_history[user_id][character][-3:]:
                context_parts.append(f"Previous Q: {interaction['question']}")
                context_parts.append(f"Previous A: {interaction['response']['answer']}")

        # Construct full prompt
        full_prompt = f"{config}\n"
        if context_parts:
            full_prompt += "\n".join(context_parts) + "\n\n"
        full_prompt += f"{prompt}\nRespond as {character}"

        # Get response
        response = client.models.generate_content(
            model=model,
            contents=full_prompt,
        )
        return response.text
    except Exception as e:
        raise Exception(f"Failed to get AI response: {str(e)}")

def clear_conversation_history(
        user_id: int,
        character: str = None
    ) -> dict:

    """

    Clear history for a user/character

    Returns:
        Dictionary with status message

    """

    try:
        if character:
            if user_id in conversation_history and character in conversation_history[user_id]:
                del conversation_history[user_id][character]
                result = {"status": f"Cleared history for character {character}"}
            else:
                result = {"status": f"No history found for character {character}"}
        else:
            if user_id in conversation_history:
                del conversation_history[user_id]
                result = {"status": "Cleared all history for user"}
            else:
                result = {"status": "No history found for this user"}
    except Exception as e:
        result = {"status": f"Error clearing history: {str(e)}"}

    return result


def get_conversation_history(
        user_id: int,
        character: str = None
    ) -> dict:

    """

    Get conversation history

    Returns:
        Dictionary with either:
        - Full conversation history
        - Filtered history for specific character
        - Error message if not found

    """

    try:
        if user_id not in conversation_history:
            result = {"status": "No history found for this user"}
        elif character:
            history = conversation_history[user_id].get(character, [])
            result = {
                "user_id": user_id,
                "character": character,
                "history": history,
                "count": len(history)
            }
        else:
            full_history = dict(conversation_history[user_id])
            result = {
                "user_id": user_id,
                "history": full_history,
                "character_count": len(full_history),
                "total_messages": sum(len(msgs) for msgs in full_history.values())
            }
    except Exception as e:
        result = {"status": f"Error retrieving history: {str(e)}"}

    return result


def clear_history(
        user_id: int,
        character: str = None
    ) -> dict:

    """

    Clear conversation history with dict response

    Returns:
        Dictionary with operation status

    """

    try:
        if user_id not in conversation_history:
            result = {"status": "No history found for this user"}
        elif character:
            if character in conversation_history[user_id]:
                del conversation_history[user_id][character]
                result = {
                    "status": "success",
                    "message": f"Cleared history for {character}",
                    "user_id": user_id,
                    "character": character
                }
            else:
                result = {
                    "status": "not_found",
                    "message": f"No history found for {character}",
                    "user_id": user_id,
                    "character": character
                }
        else:
            del conversation_history[user_id]
            result = {
                "status": "success",
                "message": "Cleared all history for user",
                "user_id": user_id
            }
    except Exception as e:
        result = {
            "status": f"error",
            "message": str(e),
            "user_id": user_id,
            "character": character if character else None
        }
    return result

# ## Example usage:
# if __name__ == "__main__":
#     # First interaction (user 1001)
#     print("First question to Einstein:")
#     print(get_ai_response(
#         prompt="What's your view on quantum mechanics?",
#         character="Albert Einstein",
#         user_id=1001
#     ))
#
#     # Follow-up with context (user 1001)
#     print("\nFollow-up question:")
#     print(get_ai_response(
#         prompt="Can you explain that further?",
#         character="Albert Einstein",
#         user_id=1001
#     ))
#
#     # Different character conversation (user 1001)
#     print("\nQuestion to Tesla:")
#     print(get_ai_response(
#         prompt="Tell me about your wireless electricity ideas",
#         character="Nikola Tesla",
#         user_id=1001
#     ))
#
#     # Different user conversation (user 2002)
#     print("\nDifferent user's question:")
#     print(get_ai_response(
#         prompt="Explain E=mc² simply",
#         character="Albert Einstein",
#         user_id=2002
#     ))
#
#     # Inspect history examples:
#     print("\nUser 1001's Einstein History:")
#     print(json.dumps(get_conversation_history(1001, "Albert Einstein"), indent=2))
#
#     print("\nFull User 1001 History:")
#     print(json.dumps(get_conversation_history(1001), indent=2))
#
#     # Clearing examples:
#     print("\nClearing Einstein history for user 1001:")
#     print(clear_history(1001, "Albert Einstein"))
#
#     print("\nClearing all history for user 1001:")
#     print(clear_history(1001))