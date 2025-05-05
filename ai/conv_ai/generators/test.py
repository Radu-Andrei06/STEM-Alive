import os
import logging
import traceback
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

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv(dotenv_path="../../.env")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    logger.error("GEMINI_API_KEY not found in environment variables")
    raise ValueError("GEMINI_API_KEY not found in environment variables")

logger.info(f"API Key loaded: {GEMINI_API_KEY[:5]}...")

# Initialize the Gemini AI client - Using Client directly
try:
    genai_client = genai.Client(api_key=GEMINI_API_KEY)
    logger.info("Gemini API client initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Gemini API client: {e}")
    raise


def get_or_create_user(user_id: int) -> int:
    """Get or create a user in the database, returns user ID"""
    try:
        # Ensure user_id is an integer
        if not isinstance(user_id, int):
            try:
                user_id = int(user_id)
            except (TypeError, ValueError):
                logger.error(f"Invalid user_id, cannot convert to integer: {user_id}")
                raise ValueError(f"User ID must be an integer, received: {type(user_id)}")

        result = execute_query(GET_OR_CREATE_USER, (user_id,))
        if not result:
            logger.error(f"No result returned from get_or_create_user for user_id {user_id}")
            raise ValueError(f"Failed to create or get user with ID {user_id}")

        # Assuming result is a list of row objects with a 'id' column
        return result[0][0]  # Access first row, first column directly
    except Exception as e:
        logger.error(f"Error in get_or_create_user: {e}")
        raise


def get_or_create_character(user_id: int, character_name: str) -> int:
    """Get or create a character conversation for a user, returns character ID"""
    try:
        # Ensure user_id is an integer
        if not isinstance(user_id, int):
            try:
                user_id = int(user_id)
            except (TypeError, ValueError):
                logger.error(f"Invalid user_id, cannot convert to integer: {user_id}")
                raise ValueError(f"User ID must be an integer, received: {type(user_id)}")

        # First ensure user exists
        user_db_id = get_or_create_user(user_id)

        # Validate character_name
        if not isinstance(character_name, str):
            logger.error(f"Invalid character_name, not a string: {character_name}")
            raise ValueError(f"Character name must be a string, received: {type(character_name)}")

        # Now create/get character
        result = execute_query(GET_OR_CREATE_CHARACTER, (user_id, character_name))
        if not result:
            logger.error(
                f"No result returned from get_or_create_character for user_id {user_id}, character {character_name}")
            raise ValueError(f"Failed to create or get character {character_name} for user {user_id}")

        return result[0][0]  # Access first row, first column directly
    except Exception as e:
        logger.error(f"Error in get_or_create_character: {e}")
        raise


def save_message(character_id: int, content: str, is_from_user: bool):
    """Save a message to the database"""
    try:
        # Ensure character_id is an integer
        if not isinstance(character_id, int):
            try:
                character_id = int(character_id)
            except (TypeError, ValueError):
                logger.error(f"Invalid character_id, cannot convert to integer: {character_id}")
                raise ValueError(f"Character ID must be an integer, received: {type(character_id)}")

        # Ensure content is a string
        if not isinstance(content, str):
            try:
                content = str(content)
                logger.warning(f"Content not a string, converted: {content[:50]}...")
            except Exception as e:
                logger.error(f"Cannot convert content to string: {e}")
                raise ValueError(f"Content must be a string, received: {type(content)}")

        # Ensure is_from_user is a boolean
        if not isinstance(is_from_user, bool):
            try:
                is_from_user = bool(is_from_user)
                logger.warning(f"is_from_user not a boolean, converted to: {is_from_user}")
            except Exception as e:
                logger.error(f"Cannot convert is_from_user to boolean: {e}")
                raise ValueError(f"is_from_user must be a boolean, received: {type(is_from_user)}")

        execute_query(SAVE_MESSAGE, (character_id, content, is_from_user))
    except Exception as e:
        logger.error(f"Error in save_message: {e}")
        raise


def get_conversation_messages(user_id: int, character_name: str, limit: int = None) -> list:
    """Retrieve conversation messages from the database"""
    try:
        # Ensure parameters are of correct type
        if not isinstance(user_id, int):
            try:
                user_id = int(user_id)
            except (TypeError, ValueError):
                logger.error(f"Invalid user_id, cannot convert to integer: {user_id}")
                raise ValueError(f"User ID must be an integer, received: {type(user_id)}")

        if not isinstance(character_name, str):
            logger.error(f"Invalid character_name, not a string: {character_name}")
            raise ValueError(f"Character name must be a string, received: {type(character_name)}")

        # First get the character_id
        char_id_result = execute_query(
            "SELECT id FROM characters WHERE user_id = %s AND character_name = %s",
            (user_id, character_name)
        )

        if not char_id_result:
            logger.warning(f"No character found: {character_name} for user {user_id}")
            return []

        character_id = char_id_result[0][0]

        # Now get the messages using character_id
        query = """
            SELECT content, timestamp, is_from_user
            FROM messages
            WHERE character_id = %s
            ORDER BY timestamp DESC
            {limit}
        """.format(limit=f"LIMIT {limit}" if limit else "")

        result = execute_query(query, (character_id,))

        # Create dictionary for each row
        messages = []
        for row in result:
            # Check if row is a tuple or dict
            if isinstance(row, dict):
                messages.append(row)
            else:
                # Convert row tuple to dict with column names
                messages.append({
                    'content': row[0],
                    'timestamp': row[1],
                    'is_from_user': row[2]
                })
        return messages
    except Exception as e:
        logger.error(f"Error in get_conversation_messages: {e}")
        raise


def clear_conversation(user_id: int, character_name: str = None):
    """Clear conversation history from the database"""
    try:
        if character_name:
            # Get character ID first
            char_result = execute_query(
                "SELECT id FROM characters WHERE user_id = %s AND character_name = %s",
                (user_id, character_name)
            )
            if not char_result:
                logger.warning(f"No character found to clear: {character_name} for user {user_id}")
                return

            character_id = char_result[0][0]
            execute_query(CLEAR_CONVERSATION, (character_id,))
        else:
            # Get all character IDs for this user
            char_results = execute_query(
                "SELECT id FROM characters WHERE user_id = %s",
                (user_id,)
            )
            if not char_results:
                logger.warning(f"No characters found to clear for user {user_id}")
                return

            for row in char_results:
                character_id = row[0]
                execute_query(CLEAR_CONVERSATION, (character_id,))
    except Exception as e:
        logger.error(f"Error in clear_conversation: {e}")
        raise


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
        logger.info(f"Processing request for user {user_id} as character {character}")
        logger.info(f"Using model: {model}, config: {config}, use_history: {use_history}")

        try:
            # Store user message first
            character_id = get_or_create_character(user_id, character)
            save_message(character_id, prompt, True)
            logger.info(f"Saved user message to database for character_id {character_id}")

            # Get AI response
            logger.info(f"Getting AI response for prompt: {prompt[:50]}...")
            ai_response = func(
                prompt=prompt,
                model=model,
                config=config,
                character=character,
                user_id=user_id,
                use_history=use_history
            )
            logger.info(f"Received AI response: {ai_response[:50]}...")

            # Store AI response
            save_message(character_id, ai_response, False)
            logger.info("Saved AI response to database")

            response_time = (datetime.now() - start_time).total_seconds() * 1000

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
            logger.error(f"Error in ai_response_decorator: {e}")
            logger.error(traceback.format_exc())
            return {
                "question": prompt,
                "response": {"character": character, "answer": f"Error: {str(e)}"},
                "config": {"model": model, "max_length": None, "context_used": False},
                "metadata": {
                    "timestamp": datetime.now().isoformat(),
                    "response_time_ms": 0,
                    "user_id": user_id,
                    "error": traceback.format_exc()
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
        # Build prompt with conversation history if needed
        context_parts = []
        if use_history:
            messages = get_conversation_messages(user_id, character, limit=6)
            logger.info(f"Retrieved {len(messages)} messages from history")

            # Since messages are returned in DESC order, we need to reverse them
            messages = list(reversed(messages))

            for msg in messages:
                role = "User" if msg['is_from_user'] else character
                context_parts.append(f"{role}: {msg['content']}")

        # Build the full prompt
        full_prompt = f"{config}\n"
        if context_parts:
            full_prompt += "\n".join(context_parts) + "\n\n"
        full_prompt += f"User: {prompt}\nRespond as {character}:"

        logger.info(f"Full prompt (first 200 chars): {full_prompt[:200]}...")

        # Safety settings
        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
        ]

        # Generation config
        generation_config = {
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 1024,
        }

        # Call Gemini API using client.generate_content
        logger.info("Calling Gemini API...")
        response = genai_client.generate_content(
            model=model,
            contents=full_prompt,
            generation_config=generation_config,
            safety_settings=safety_settings
        )

        logger.info(f"Received response from API: {response}")

        if not hasattr(response, 'text'):
            logger.error(f"Response has no 'text' attribute: {response}")

            # Try to extract text from response in alternative ways
            if hasattr(response, 'candidates') and response.candidates:
                if hasattr(response.candidates[0], 'content') and hasattr(response.candidates[0].content, 'parts'):
                    return ''.join(str(part) for part in response.candidates[0].content.parts)

            if hasattr(response, 'parts'):
                return ''.join(str(part) for part in response.parts)

            return f"Error: Invalid response format from API: {response}"

        return response.text

    except Exception as e:
        logger.error(f"Error in get_ai_response: {e}")
        logger.error(traceback.format_exc())
        raise Exception(str(e))


def get_conversation_history(
        user_id: int,
        character: str = None
) -> dict:
    """Get conversation history from database"""
    try:
        # Ensure user_id is an integer
        if not isinstance(user_id, int):
            try:
                user_id = int(user_id)
            except (TypeError, ValueError):
                logger.error(f"Invalid user_id in get_conversation_history: {user_id}")
                return {"status": f"Error: User ID must be an integer, received: {type(user_id)}"}

        if character:
            # Validate character name
            if not isinstance(character, str):
                logger.error(f"Invalid character name in get_conversation_history: {character}")
                return {"status": f"Error: Character name must be a string, received: {type(character)}"}

            # First check if character exists for this user
            char_exists = execute_query(
                "SELECT EXISTS(SELECT 1 FROM characters WHERE user_id = %s AND character_name = %s)",
                (user_id, character)
            )

            if not char_exists or not char_exists[0][0]:
                logger.warning(f"Character {character} does not exist for user {user_id}")
                return {"status": f"No history found for character {character}"}

            messages = get_conversation_messages(user_id, character)
            # Messages are in DESC order, so we need to reverse them
            messages = list(reversed(messages))

            if not messages:
                return {"status": f"No history found for character {character}"}

            history = []
            for i in range(0, len(messages), 2):
                if i + 1 < len(messages):
                    if messages[i]['is_from_user']:
                        # User message first, AI response second
                        history.append({
                            "question": messages[i]['content'],
                            "answer": messages[i + 1]['content'],
                            "timestamp": messages[i]['timestamp'].isoformat() if isinstance(messages[i]['timestamp'],
                                                                                            datetime) else messages[i][
                                'timestamp']
                        })
                    else:
                        # AI message first, User response second
                        history.append({
                            "question": messages[i + 1]['content'],
                            "answer": messages[i]['content'],
                            "timestamp": messages[i + 1]['timestamp'].isoformat() if isinstance(
                                messages[i + 1]['timestamp'], datetime) else messages[i + 1]['timestamp']
                        })

            return {
                "user_id": user_id,
                "character": character,
                "history": history,
                "count": len(history)
            }
        else:
            # Check if user exists first
            user_exists = execute_query(
                "SELECT EXISTS(SELECT 1 FROM users WHERE user_id = %s)",
                (user_id,)
            )

            if not user_exists or not user_exists[0][0]:
                logger.warning(f"User {user_id} does not exist")
                return {"status": "No history found for this user"}

            # Get all characters for user
            characters = execute_query(
                "SELECT character_name FROM characters WHERE user_id = %s",
                (user_id,)
            )

            if not characters:
                return {"status": "No history found for this user"}

            full_history = {}
            for char in characters:
                # Check if char is a dict or tuple
                char_name = char['character_name'] if isinstance(char, dict) else char[0]
                char_history = get_conversation_history(user_id, char_name)
                if "history" in char_history:
                    full_history[char_name] = char_history["history"]
                else:
                    full_history[char_name] = []

            return {
                "user_id": user_id,
                "history": full_history,
                "character_count": len(full_history),
                "total_messages": sum(len(msgs) for msgs in full_history.values())
            }
    except Exception as e:
        logger.error(f"Error in get_conversation_history: {e}")
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
        logger.error(f"Error in clear_history: {e}")
        return {
            "status": "error",
            "message": str(e),
            "user_id": user_id,
            "character": character if character else None
        }


# For testing
if __name__ == "__main__":
    try:
        # Print available models
        logger.info("Attempting to list available models...")
        try:
            available_models = genai_client.list_models()
            model_names = [model.name for model in available_models]
            logger.info(f"Available models: {model_names}")
        except AttributeError as e:
            logger.error(f"Could not list models: {e}")
            logger.info("Will try with common model names instead")
            model_names = ["gemini-pro", "gemini-1.5-flash"]

        # First try with gemini-pro (common model)
        model_to_use = model_names[0] if model_names else "gemini-pro"
        logger.info(f"Using model: {model_to_use}")

        response = get_ai_response(
            prompt="Explain quantum physics basics",
            character="Albert Einstein",
            user_id=1001,
            model=model_to_use,
            config="Keep response under 200 words"
        )
        print("Response:", response)

        # Verify storage
        history = get_conversation_history(user_id=1001)
        print("Stored history:", history)

    except Exception as e:
        print(f"Failed: {str(e)}")
        print(traceback.format_exc())