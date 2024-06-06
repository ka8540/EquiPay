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

            query = '''SELECT 1 FROM Friends WHERE (UserID = %s AND FriendUserID = %s) OR (UserID = %s AND FriendUserID = %s);'''
            result = exec_get_all(query, (user_id, friend_id, friend_id, user_id ))
            if result:
                return True
            else:
                return False
    except Exception as e:
        print(f"Failed to retrieve friend request: {e}")
        return "Failed to retrieve friend request"            




    
    print("Result:",result)
    return result

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
