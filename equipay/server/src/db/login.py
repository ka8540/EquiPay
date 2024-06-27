import os
import pandas as pd
from psycopg2 import connect  # Import psycopg2 if you need it for database operations, otherwise remove it
try:
    from src.utilities.swen_344_db_utils import exec_get_all, exec_get_one, exec_commit
    from src.model.user import generate_session_key
except ImportError:
    from utilities.swen_344_db_utils import exec_get_all, exec_get_one, exec_commit
    from model.user import generate_session_key

def list_info_items():
    """Fetches all records from the User table."""
    result = exec_get_all('''SELECT * FROM "user" ''')
    return result

def check_user_credentials(bcrypt, username, password):
    query_user = '''SELECT username, password FROM "user" WHERE username = %s;'''
    user = exec_get_one(query_user, (username,))
    
    if user and bcrypt.check_password_hash(user[1], password):  # Accessing password using index 1
        session_key = generate_session_key()
        update_session_key_query = '''UPDATE "user" SET session_key = %s WHERE username = %s;'''
        exec_commit(update_session_key_query, (session_key, username))
        return {"message": "Login Creds are Correct", "sessionKey": session_key}, 200
    elif user and not bcrypt.check_password_hash(user[1], password):  # Accessing password using index 1
        return {"message": "Password Invalid", "sessionKey": None}, 211
    else:
        return {"message": "Login Creds are Incorrect", "sessionKey": None}, 201
