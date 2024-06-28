import hashlib
import secrets
from flask_bcrypt import Bcrypt
try:
    from src.utilities.swen_344_db_utils import exec_get_all, exec_commit
except ImportError:
    from utilities.swen_344_db_utils import exec_get_all, exec_commit

bcrypt = Bcrypt()

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
    query = '''SELECT firstname, lastname, username, email FROM "user" WHERE username = %s;'''
    users = exec_get_all(query, (username,))
    print(users, 'user detail!!')
    
    if users:
        user_details = [{'firstname': user[0], 'lastname': user[1], 'username': user[2], 'email': user[3]} for user in users]
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
    print("Got here in the user_update_detail")
    print("Username:", username)
    print("Update parameters:", kwargs)  # Correct usage of print with kwargs
    
    # Creating the SQL SET clause dynamically based on provided kwargs
    set_clause = ', '.join([f"{key} = %s" for key in kwargs.keys()])
    values = list(kwargs.values())
    values.append(username)  # Add username at the end for the WHERE clause
    
    # Construct the SQL query
    query = f"UPDATE \"user\" SET {set_clause} WHERE username = %s;"
    
    try:
        # Execute the query
        exec_commit(query, tuple(values))  
        return True
    except Exception as e:
        print("Failed to update user details:", str(e))
        return False


def get_password(username, old_password):
    print("reached get_password!!")
    print("Username:", username)
    print("Password Attempt:", old_password)
    
    query = '''SELECT password FROM "user" WHERE username = %s;'''
    result = exec_get_all(query, (username,))  # Assuming this returns a list of tuples
    
    if result:
        stored_password_hash = result[0][0]  # Assuming password is the first element of the first tuple
        print("Stored Hash:", stored_password_hash)
        
        # Use bcrypt to check if the provided password matches the stored hash
        if bcrypt.check_password_hash(stored_password_hash, old_password):
            print("Password is correct!")
            return True
        else:
            print("Password is incorrect.")
    else:
        print("No user found with that username.")
    
    return False

def update_passord(hashed_password,username):
    query = '''UPDATE "user" SET password = %s WHERE username = %s'''
    result = exec_commit(query,(hashed_password,username))


def update_user_image_url(user_id, url):
    query = '''UPDATE "user" SET profile_pic = %s WHERE username = %s;'''
    try:
        exec_commit(query, (url, user_id))
        return "Image URL updated successfully"
    except Exception as e:
        print(f"Database Error: {e}")
        return "Failed to update image URL"
    
def update_group_image_url(group_id, url):
    query = '''UPDATE Groups SET profile_picture = %s WHERE GroupID = %s;'''
    try:
        exec_commit(query, (url, group_id))
        return "Image URL updated successfully"
    except Exception as e:
        print(f"Database Error: {e}")
        return "Failed to update image URL"    

def profile_picture(username):
    print("Inside the profile picture def")
    query = '''SELECT profile_pic FROM "user" WHERE username = %s;'''
    # Ensure parameters are passed as a tuple, `(username,)` ensures it's a tuple even with one item
    result = exec_get_all(query, (username,))
    print("Result:", result)
    if result:
        # Assuming `result` is the full row, extract the profile_pic URL
        return result[0]  # Modify based on how your data is structured
    else:
        return None
    
def group_profile_picture(group_id):
    print("Inside the Group profile Picture")
    query = '''SELECT profile_picture FROM Groups WHERE GroupID = %s'''
    result = exec_get_all(query,(group_id,))
    print("Result:",result)
    if result:
        return result[0]
    else:
        return None


def check_friendship_and_get_profile_pic(user_id, friend_id):
    query = '''
    SELECT u.profile_pic 
    FROM "user" u
    JOIN Friends f ON (u.user_id = f.FriendUserID OR u.user_id = f.UserID)
    WHERE ((f.UserID = %s AND f.FriendUserID = %s) OR (f.UserID = %s AND f.FriendUserID = %s))
      AND f.Status = 'accepted';
    '''
    params = (user_id, friend_id, friend_id, user_id)
    result = exec_get_all(query, params)
    if result:
        return result[0][0]  # Assuming the first column of the first row is the profile_pic URL.
    else:
        return None
    
def delete_account(username):
    print("Attempting to delete account for username:", username)
    # Check if user exists
    user_exists = exec_get_all('SELECT 1 FROM "user" WHERE username = %s', (username,))
    if not user_exists:
        print("No account found for username:", username)
        return False
    
    # Attempt to delete user
    exec_commit('DELETE FROM "user" WHERE username = %s', (username,))
    # Verify deletion
    user_still_exists = exec_get_all('SELECT 1 FROM "user" WHERE username = %s', (username,))
    if not user_still_exists:
        print("Account successfully deleted for username:", username)
        return True
    else:
        print("Failed to delete account for username:", username)
        return False
    
    