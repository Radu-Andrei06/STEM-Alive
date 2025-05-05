# Database queries for conversation management

GET_OR_CREATE_USER = """
    INSERT INTO users (user_id) 
    VALUES (%s) 
    ON CONFLICT (user_id) DO UPDATE SET user_id = EXCLUDED.user_id 
    RETURNING id
"""

GET_OR_CREATE_CHARACTER = """
    INSERT INTO characters (user_id, character_name) 
    VALUES (%s, %s) 
    ON CONFLICT (user_id, character_name) DO UPDATE SET character_name = EXCLUDED.character_name 
    RETURNING id
"""

SAVE_MESSAGE = """
    INSERT INTO messages (character_id, content, is_from_user) 
    VALUES (%s, %s, %s)
"""

# Note: We're not using this complex query anymore - see simplified version in code
GET_CONVERSATION_MESSAGES = """
    SELECT m.content, m.timestamp, m.is_from_user
    FROM messages m
    JOIN characters c ON m.character_id = c.id
    JOIN users u ON c.user_id = u.user_id
    WHERE u.user_id = %s AND c.character_name = %s
    ORDER BY m.timestamp DESC
    {limit}
"""

# Note: We're not using this complex query anymore - see simplified version in code
CLEAR_CONVERSATION = """
    DELETE FROM messages
    WHERE character_id = %s
"""