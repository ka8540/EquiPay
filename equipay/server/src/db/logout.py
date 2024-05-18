import secrets  # Include only if you're generating new session keys or similar
from psycopg2 import connect  # Include this only if you're directly using psycopg2 for connections in other parts of your script

# Import only necessary functions from your utilities and models
try:
    from src.utilities.swen_344_db_utils import exec_commit
except ImportError:
    from utilities.swen_344_db_utils import exec_commit


def user_logout(kwargs):
    session_key = kwargs.get('session_key')
    logout_query = '''UPDATE user_authentication SET session_key = NULL WHERE session_key = %s;'''
    exec_commit(logout_query, (session_key,))
    return {"message":"User Logout Successfully!"},200
