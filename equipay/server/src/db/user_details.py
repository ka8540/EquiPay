import hashlib
import secrets
try:
    from src.utilities.swen_344_db_utils import exec_get_all
except ImportError:
    from utilities.swen_344_db_utils import exec_get_all


def list_user_detail(username):
    print('User entered to get the detail!!')
    # Updated query to filter by username using parameterized queries for security
    query = '''SELECT firstname, lastname, username, email FROM user_authentication WHERE username = %s;'''
    users = exec_get_all(query, (username,))  # Note the comma after username to make it a tuple
    print(users, 'user detail!!')
    
    if users:
        user_details = [{'firstname': user[0], 'lastname': user[1], 'username': user[2], 'email': user[3]} for user in users]
    else:
        user_details = []
    
    return user_details

def verify_session_key(session_key):
    # Implement the logic to verify session key and return the associated username
    # This is a placeholder for your SQL query to find the username with the given session_key
    query = '''SELECT username FROM user_authentication WHERE session_key = %s;'''
    result = exec_get_all(query, (session_key,))
    if result:
        return result[0][0]  # Assuming exec_get_all returns a list of tuples
    return None
