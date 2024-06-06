from utilities.swen_344_db_utils import exec_get_all, exec_commit, exec_get_one

def existing_friend(username, friend_id):
    print("Inside the frieds DB!!")
    try:
        # Fetch the user ID from the database using the username
        query_user_id = '''SELECT user_id FROM "user" WHERE username = %s;'''
        user_id_tuple = exec_get_one(query_user_id, (username,))
        if user_id_tuple:
            user_id = user_id_tuple[0]  # Extract the user_id from the tuple
            print("User_id:", user_id)

            query = '''SELECT 1 FROM Friends WHERE (UserID = %s AND FriendUserID = %s);'''
            result = exec_get_all(query, (user_id, friend_id))
            if result:
                return True
            else:
                return False
    except Exception as e:
        print(f"Failed to retrieve friend request: {e}")
        return "Failed to retrieve friend request"       


def get_pending_friend_requests(username):
    print("Inside the Pending Request!!")
    query = '''
    SELECT  u.user_id, u.firstname
    FROM Friends f
    JOIN "user" u ON u.user_id = f.UserID 
    WHERE f.FriendUserID = (SELECT user_id FROM "user" WHERE username = %s) 
    AND f.Status = 'pending';
    '''
    result = exec_get_all(query, (username,))
    print("Lol")
    print("Result:", result)
    # Transform the result to just return names if that's all you need
    return result

def get_friend_requests(username):
    print("Fetching accepted friends for:", username)
    query = '''
    SELECT u.user_id, u.firstname
    FROM Friends f
    JOIN "user" u ON u.user_id = f.FriendUserID
    WHERE f.UserID = (SELECT user_id FROM "user" WHERE username = %s)
    AND f.Status = 'accepted'
    UNION
    SELECT u.user_id, u.firstname
    FROM Friends f
    JOIN "user" u ON u.user_id = f.UserID
    WHERE f.FriendUserID = (SELECT user_id FROM "user" WHERE username = %s)
    AND f.Status = 'accepted';
    '''
    result = exec_get_all(query, (username, username))
    print("Result:", result)
    return result

def update_friend_request_status(username, friend_id, action):
    print("Inside the DB!!")
    print("Username:",username)
    try:
        user_id = exec_get_all("SELECT user_id FROM \"user\" WHERE username = %s", (username,))
        print("user_id:",user_id)
        print("Friend id :", friend_id)
        if user_id:
            user_id = user_id[0]
            print("action:",action)
            status = 'accepted' if action == 'accept' else 'rejected'
            exec_commit("UPDATE Friends SET Status = %s WHERE FriendUserID = %s", (status,user_id))
            return True
        return False
    except Exception as e:
        print(f"Failed to update friend request: {e}")
        return False


def add_friend_request(username, friend_id):
    try:
        # Fetch the user ID from the database using the username
        query_user_id = '''SELECT user_id FROM "user" WHERE username = %s;'''
        user_id_tuple = exec_get_one(query_user_id, (username,))
        
        if user_id_tuple:
            user_id = user_id_tuple[0]  # Extract the user_id from the tuple
            print("User_id:", user_id)

            # Insert the friend request
            exec_commit("INSERT INTO Friends (UserID, FriendUserID, Status) VALUES (%s, %s, 'pending')",
                        (user_id, friend_id))
            return True
        else:
            print("No user found with username:", username)
            return False
    except Exception as e:
        print(f"Failed to insert friend request: {e}")
        return False
