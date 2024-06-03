import hashlib
import secrets
try:
    from src.utilities.swen_344_db_utils import exec_get_all
except ImportError:
    from utilities.swen_344_db_utils import exec_get_all

def list_info_items(username):
    print("Username:", username)
    query = '''
    SELECT * FROM "user"
    WHERE username != %s
    '''
    result = exec_get_all(query, (username,))
    return result

def list_user_detail(username):
    print('User entered to get the detail!!')
    query = '''SELECT firstname, lastname, username, email, profile_pic_url FROM "user" WHERE username = %s;'''
    users = exec_get_all(query, (username,)) 
    print(users, 'user detail!!')
    
    if users:
        user_details = [{'firstname': user[0], 'lastname': user[1], 'username': user[2], 'email': user[3], 'profile_pic_url': user[4]} for user in users]
    else:
        user_details = []
    
    return user_details

def verify_session_key(session_key):
    query = '''SELECT username FROM user_authentication WHERE session_key = %s;'''
    result = exec_get_all(query, (session_key,))
    if result:
        return result[0][0]  
    return None

def update_user_detail(username, **kwargs):
    set_clause = ', '.join([f"{key} = %s" for key in kwargs.keys()])
    values = list(kwargs.values())
    values.append(username)  
    query = f'''UPDATE "user" SET {set_clause} WHERE username = %s;'''
    try:
        exec_get_all(query, tuple(values))  
        return True
    except Exception as e:
        print("Failed to update user details:", str(e))
        return False
