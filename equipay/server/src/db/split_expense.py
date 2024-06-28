from utilities.swen_344_db_utils import exec_commit, exec_get_one, exec_fetch

def split_expense_(usercreds, amount, friend_ids, include_self, description):
    print("Inside the Split Expense N DB!!")
    try:
        username = usercreds
        print("User credentials:", usercreds)
        UserID_query = '''SELECT user_id FROM "user" WHERE username = %s;'''
        user_id_results = exec_get_one(UserID_query, (username,))
        print("User_ID:", user_id_results)
        if not user_id_results:
            print("No user found with username:", username)
            return False
        user_id = user_id_results[0]
        print("user_id:", user_id)
        print("Friend_ids",friend_ids)
        divisor = len(friend_ids) + (1 if include_self else 0)
        each_share = amount / divisor
        print("Each share calculated:", each_share)

        # Create an expense entry and get its ID
        expense_id = create_expense(user_id, amount, description)
        if not expense_id:
            print("Failed to create expense.")
            return False

        # Insert expense participation for each friend
        query = "INSERT INTO Debts (ExpenseID, OwedToUserID, OwedByUserID, AmountOwed) VALUES (%s, %s, %s, %s)"
        for friend_id in friend_ids:
            print("Processing friend_id:", friend_id)
            exec_commit(query, (expense_id, user_id, friend_id, each_share))

        # Optionally, record the payer's part of the expense
        if include_self:
            print("Recording payer's share")
            exec_commit(query, (expense_id, user_id, user_id, each_share))
        
        return True
    except Exception as e:
        print("Failed to split expense:", e)
        return False

def create_expense(payer_id, amount, description):
    print("Creating an expense entry in the database")
    query = """
    INSERT INTO Expenses (PayerID, Amount, Description, Date)
    VALUES (%s, %s, %s, NOW()) RETURNING ExpenseID;
    """
    expense_id = exec_fetch(query, (payer_id, amount, description))
    if expense_id:
        print("Expense ID created:", expense_id[0])
        return expense_id[0]
    else:
        print("No Expense ID retrieved")
        return None
