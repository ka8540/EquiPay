from utilities.swen_344_db_utils import exec_get_all, exec_get_one, exec_commit

def get_groups_by_user_id(user_id):
    query = """
    SELECT g.GroupID, g.GroupName, gm.IsAdmin
    FROM Groups g
    JOIN GroupMembers gm ON g.GroupID = gm.GroupID
    WHERE gm.UserID = %s;
    """
    groups = exec_get_all(query, (user_id,))
    print(groups)
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

def get_group_members_by_group_id(group_id):
    query = """
    SELECT u.user_id, u.firstname, gm.IsAdmin
    FROM "user" u
    JOIN GroupMembers gm ON u.user_id = gm.UserID
    WHERE gm.GroupID = %s;
    """
    members = exec_get_all(query, (group_id,))
    return [{'user_id': member[0], 'first_name': member[1], 'is_admin': member[2]} for member in members]


def get_groups_by_group_id(group_id):
    query = """
    SELECT GroupName FROM Groups WHERE GroupID = %s;
    """
    group_name = exec_get_all(query, (group_id,))
    print(group_name)
    return group_name