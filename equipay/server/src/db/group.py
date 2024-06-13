from utilities.swen_344_db_utils import exec_get_all, exec_get_one, exec_commit, exec_fetch

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

def split_group_expense(username, group_id, amount, friend_ids, include_self, description):
    print("Inside the Split Expense in DB!!")
    try:
        print("User credentials:", username)
        UserID_query = '''SELECT user_id FROM "user" WHERE username = %s;'''
        user_id_results = exec_get_one(UserID_query, (username,))
        print("User_ID:", user_id_results)
        if not user_id_results:
            print("No user found with username:", username)
            return False
        user_id = user_id_results[0]
        print("user_id:", user_id)
        print("Friend_ids", friend_ids)
        divisor = len(friend_ids) + (1 if include_self else 0)
        each_share = amount / divisor
        print("Each share calculated:", each_share)

        # Create a group expense entry and get its ID
        expense_id = create_group_expense(group_id, user_id, amount, description)
        if not expense_id:
            print("Failed to create group expense.")
            return False

        # Insert group debt for each group member
        debt_insert_query = "INSERT INTO GroupDebts (ExpenseID, OwedToUserID, OwedByUserID, AmountOwed) VALUES (%s, %s, %s, %s)"
        for friend_id in friend_ids:
            print("Processing friend_id:", friend_id)
            exec_commit(debt_insert_query, (expense_id, user_id, friend_id, each_share))

        # Optionally, record the payer's part of the expense
        if include_self:
            print("Recording payer's share")
            exec_commit(debt_insert_query, (expense_id, user_id, user_id, each_share))

        return True
    except Exception as e:
        print("Failed to split expense:", e)
        return False

def create_group_expense(group_id, payer_id, amount, description):
    print("Creating a group expense entry in the database")
    expense_insert_query = """
    INSERT INTO GroupExpenses (GroupID, PayerID, Amount, Description, Date)
    VALUES (%s, %s, %s, %s, NOW()) RETURNING ExpenseID;
    """
    expense_id = exec_fetch(expense_insert_query, (group_id, payer_id, amount, description))
    if expense_id:
        print("Group Expense ID created:", expense_id[0])
        return expense_id[0]
    else:
        print("No Group Expense ID retrieved")
        return None
