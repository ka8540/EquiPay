from utilities.swen_344_db_utils import exec_get_one, exec_get_all
def get_firstname_by_id(friend_id):
    print("User_id:",friend_id)
    query = '''SELECT firstname FROM "user" WHERE user_id = %s;'''
    friend_name = exec_get_one(query, (friend_id,))
    return friend_name[0]

def get_items_for_activity(user_id):
    query = '''SELECT ActionType, Details, Timestamp FROM ActivityLog WHERE UserID = %s ORDER BY Timestamp DESC;'''
    result = exec_get_all(query, (user_id,)) 
    return result