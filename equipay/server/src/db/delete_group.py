from utilities.swen_344_db_utils import exec_commit, exec_get_all, exec_get_one
def delete_group1(user_id, group_id):
    print("Entered the DB")
    delete_query = '''DELETE FROM Groups
            WHERE CreatedBy = %s
            AND GroupID = %s
            AND GroupID IN (
                SELECT GroupID
                FROM GroupMembers
                WHERE UserID = %s
                AND GroupID = %s
                AND IsAdmin = TRUE
            );'''
    delete = exec_commit(delete_query, (user_id, group_id, user_id, group_id))
    print("Delete Query result!!",delete)
    check_query = '''SELECT * FROM Groups
                     WHERE GroupID = %s;'''
    result = exec_get_all(check_query, (group_id,))
    print("Result:",result)
    if not result:
        print("Group successfully deleted.")
        return True
    else:
        print("Group still exists:", result)
        return False

def leave_group(user_id, group_id):
    update_query = '''DELETE FROM GroupMembers WHERE GroupID = %s AND UserID = %s;'''
    result = exec_commit(update_query, (group_id, user_id))
    check_query = '''SELECT MemberID FROM GroupMembers WHERE GroupID = %s and UserID = %s;'''
    check_result = exec_get_all(check_query, (group_id, user_id))
    if check_result:
        return False 
    else:
        return True

def add_member_in_group(group_id, friend_id):
    update_group_query = '''INSERT INTO GroupMembers (GroupID, UserID) VALUES (%s, %s);'''
    result = exec_commit(update_group_query, (group_id, friend_id))

    check_query = '''SELECT MemberID FROM GroupMembers WHERE GroupID = %s AND UserID = %s'''
    checking_result = exec_get_one(check_query, (group_id,friend_id))
    if checking_result:
        print("Member added successfully")
        return True
    else:
        print("Failed to add member")
        return False

def check_total_members(group_id):
    count_query = '''SELECT UserID FROM GroupMembers WHERE GroupID = %s;'''
    result = exec_get_all(count_query, (group_id,))
    print("Count Result:", result)
    
    if result:
        member_count = len(result)
        print("Actual Member Count:", member_count)
        if 0 < member_count <5:
            return True
        else:
            print("Member count exceeds limit or no members found.")
    else:
        print("Failed to retrieve count.")

    return False

def check_member(group_id,friend_id):
    check_query = '''SELECT MemberID FROM GroupMembers WHERE GroupID = %s AND UserID = %s;'''
    try:
        result = exec_get_one(check_query, (group_id, friend_id))
        print("Checking Result:",result)
        if result:
            return False  
        else:
            return True  
    except Exception as e:
        print(f"An error occurred: {e}") 
        return False  

   

