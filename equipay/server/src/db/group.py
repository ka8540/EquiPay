from utilities.swen_344_db_utils import exec_get_all, exec_get_one, exec_commit

def get_groups_by_user_id(user_id):
    query = """
    SELECT g.GroupID, g.GroupName, gm.IsAdmin
    FROM Groups g
    JOIN GroupMembers gm ON g.GroupID = gm.GroupID
    WHERE gm.UserID = %s;
    """
    groups = exec_get_all(query, (user_id,))
    return [{'group_id': group[0], 'group_name': group[1], 'is_admin': group[2]} for group in groups]

def create_group(group_name, user_id, profile_picture_url):
    print("Inside the create froup db")
    insert_group_query = """
    INSERT INTO Groups (GroupName, CreatedBy, profile_picture)
    VALUES (%s, %s, %s) RETURNING GroupID;
    """
    result = exec_commit(insert_group_query, (group_name, user_id, profile_picture_url))
    query = '''SELECT GroupID FROM Groups WHERE GroupName = %s;'''
    group_id = exec_get_one(query, (group_name,))
    print("Group ID:",group_id)
    return group_id

def add_group_member(group_id, user_id, is_admin):
    print("Inside ADD Group Members")
    print("Group ID:",group_id)
    insert_member_query = """
    INSERT INTO GroupMembers (GroupID, UserID, IsAdmin)
    VALUES (%s, %s, %s);
    """
    exec_commit(insert_member_query, (group_id, user_id, is_admin))