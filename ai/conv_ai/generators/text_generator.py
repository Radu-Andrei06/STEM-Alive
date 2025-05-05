import os
from datetime import datetime
from dotenv import load_dotenv
from google import genai
from functools import wraps

from database.database import execute_query
from database.queries import (
    GET_OR_CREATE_USER,
    GET_OR_CREATE_CHARACTER,
    SAVE_MESSAGE,
    GET_CONVERSATION_MESSAGES,
    CLEAR_CONVERSATION
)

# Load environment variables
load_dotenv(dotenv_path="../../.env")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize the Gemini AI client
client = genai.Client(api_key=GEMINI_API_KEY)


def get_or_create_user(user_id: int) -> int:
    """Get or create a user in the database, returns user ID"""
    result = execute_query(GET_OR_CREATE_USER, (user_id,))
    return result[0]['id']


def get_or_create_character(user_id: int, character_name: str) -> int:
    """Get or create a character conversation for a user, returns character ID"""
    get_or_create_user(user_id)  # Ensure user exists
    result = execute_query(GET_OR_CREATE_CHARACTER, (user_id, character_name))
    return result[0]['id']


def save_message(character_id: int, content: str, is_from_user: bool):
    """Save a message to the database"""
    execute_query(SAVE_MESSAGE, (character_id, content, is_from_user))


def get_conversation_messages(user_id: int, character_name: str, limit: int = None) -> list:
    """Retrieve conversation messages from the database"""
    query = GET_CONVERSATION_MESSAGES.format(
        limit=f"LIMIT {limit}" if limit else ""
    )
    result = execute_query(query, (user_id, character_name))
    return [dict(row) for row in result]


def clear_conversation(user_id: int, character_name: str = None):
    """Clear conversation history from the database"""
    query = CLEAR_CONVERSATION.format(
        character_condition=f"AND character_name = '{character_name}'" if character_name else ""
    )
    execute_query(query, (user_id,))


def ai_response_decorator(func):
    """Decorator for structured AI response handling"""

    @wraps(func)
    def wrapper(
            prompt: str,
            model: str = "gemini-1.5-flash",
            config: str = "Maximum of 100 chars.",
            character: str = "Albert Einstein",
            user_id: int = 0,
            use_history: bool = False
    ) -> dict:
        start_time = datetime.now()

        try:
            ai_response = func(
                prompt=prompt,
                model=model,
                config=config,
                character=character,
                user_id=user_id,
                use_history=use_history
            )

            response_time = (datetime.now() - start_time).total_seconds() * 1000

            # Store in database
            character_id = get_or_create_character(user_id, character)
            save_message(character_id, prompt, True)
            save_message(character_id, ai_response, False)

            return {
                "question": prompt,
                "response": {"character": character, "answer": ai_response},
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

        except Exception as e:
            return {
                "question": prompt,
                "response": {"character": character, "answer": f"Error: {str(e)}"},
                "config": {"model": model, "max_length": None, "context_used": False},
                "metadata": {
                    "timestamp": datetime.now().isoformat(),
                    "response_time_ms": 0,
                    "user_id": user_id
                }
            }

    return wrapper


@ai_response_decorator
def get_ai_response(
        prompt: str,
        model: str,
        config: str,
        character: str,
        user_id: int = 0,
        use_history: bool = False
    ) -> str:
    """Core AI interaction function"""
    try:
        context_parts = []
        if use_history:
            messages = get_conversation_messages(user_id, character, limit=6)
            for i in range(0, len(messages), 2):
                if i + 1 < len(messages):
                    context_parts.append(f"User: {messages[i + 1]['content']}")
                    context_parts.append(f"{character}: {messages[i]['content']}")

        full_prompt = f"{config}\n"
        if context_parts:
            full_prompt += "\n".join(context_parts) + "\n\n"
        full_prompt += f"User: {prompt}\nRespond as {character}"

        # Updated Gemini API call
        response = client.models.generate_content(
            model=model,
            contents=full_prompt
        )
        return response.text

    except Exception as e:
        raise Exception(f"Failed to get AI response: {str(e)}")


def get_conversation_history(
        user_id: int,
        character: str = None
) -> dict:
    """Get conversation history from database"""
    try:
        if character:
            messages = get_conversation_messages(user_id, character)
            if not messages:
                return {"status": f"No history found for character {character}"}

            history = []
            for i in range(0, len(messages), 2):
                if i + 1 < len(messages):
                    history.append({
                        "question": messages[i + 1]['content'],
                        "answer": messages[i]['content'],
                        "timestamp": messages[i]['timestamp'].isoformat()
                    })

            return {
                "user_id": user_id,
                "character": character,
                "history": history,
                "count": len(history)
            }
        else:
            # Get all characters for user
            characters = execute_query(
                "SELECT character_name FROM characters WHERE user_id = %s",
                (user_id,)
            )

            if not characters:
                return {"status": "No history found for this user"}

            full_history = {}
            for char in characters:
                char_name = char['character_name']
                messages = get_conversation_messages(user_id, char_name)
                char_history = []
                for i in range(0, len(messages), 2):
                    if i + 1 < len(messages):
                        char_history.append({
                            "question": messages[i + 1]['content'],
                            "answer": messages[i]['content'],
                            "timestamp": messages[i]['timestamp'].isoformat()
                        })
                full_history[char_name] = char_history

            return {
                "user_id": user_id,
                "history": full_history,
                "character_count": len(full_history),
                "total_messages": sum(len(msgs) for msgs in full_history.values())
            }
    except Exception as e:
        return {"status": f"Error retrieving history: {str(e)}"}


def clear_history(
        user_id: int,
        character: str = None
) -> dict:
    """Clear conversation history with dict response"""
    try:
        if character:
            clear_conversation(user_id, character)
            return {
                "status": "success",
                "message": f"Cleared history for {character}",
                "user_id": user_id,
                "character": character
            }
        else:
            clear_conversation(user_id)
            return {
                "status": "success",
                "message": "Cleared all history for user",
                "user_id": user_id
            }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "user_id": user_id,
            "character": character if character else None
        }


### Example 1

# Test conversation
try:
    # First question
    response = get_ai_response(
        prompt="Explain quantum physics basics",
        character="Albert Einstein",
        user_id=1001,
        model="gemini-1.5-flash",
        config="Keep response under 200 words"
    )
    print("Response:", response)

    # Verify storage
    history = get_conversation_history(user_id=1001)
    print("Stored history:", history)

except Exception as e:
    print("Failed:", str(e))