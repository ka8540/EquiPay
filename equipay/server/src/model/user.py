import secrets
def check_username_and_password(result_username, result_credentials,session_key):
    if result_credentials:
        # If the username and password combination is correct
        return {"message": "Login Creds are Correct", "sessionKey": session_key}, 200
    elif result_username and not result_credentials:
        # Username exists but the combination is incorrect, indicating password issue
        return "Password Invalid", 411
    else: 
        # Username does not exist
        return "Login Creds are Incorrect", 410


def check_password(username):
    print(username)
    if len(username)!=0:
        return "Password Invalid",411
    return "Login Creds are Correct",200

def check_username(username):
    if username:
        # If user exists, return immediately with an appropriate message and status
        return {"message": "User already exists"}, 409  # HTTP 409 Conflict
    return None

def generate_session_key():
    print("reached here in model")
    # Generate a 16-byte (128-bit) hex string
    return secrets.token_hex(16)

