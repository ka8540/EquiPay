from utilities.swen_344_db_utils import exec_get_one, exec_get_all

def calculate_amount_owed(payer_id, receiver_id):
    print("Calculating amount owed")
    query = """
    SELECT COALESCE(SUM(AmountOwed), 0) FROM Debts
    WHERE OwedToUserID = %s AND OwedByUserID = %s;
    """
    amount = exec_get_one(query, (receiver_id, payer_id))
    return amount[0] if amount else 0


def get_user_id(username):
    user_id_query = '''SELECT user_id FROM "user" WHERE username = %s;'''
    user_id_result = exec_get_one(user_id_query, (username,))
    return user_id_result[0] if user_id_result else None

def get_user_debts(user_id):
    debts_query = """
    SELECT 
        CASE 
            WHEN d.OwedToUserID = %s THEN d.OwedByUserID  -- If current user is the creditor, get debtor's ID
            ELSE d.OwedToUserID  -- If current user is the debtor, get creditor's ID
        END AS friend_id,
        CASE 
            WHEN d.OwedToUserID = %s THEN u.firstname  -- If current user is the creditor, get debtor's name
            ELSE u.firstname  -- If current user is the debtor, get creditor's name
        END AS friend_name,
        SUM(CASE 
            WHEN d.OwedToUserID = %s THEN d.AmountOwed  -- Sum amounts owed to user by friends
            ELSE -d.AmountOwed  -- Sum amounts user owes to friends
        END) AS net_amount
    FROM Debts d
    JOIN "user" u ON u.user_id = CASE WHEN d.OwedToUserID = %s THEN d.OwedByUserID ELSE d.OwedToUserID END
    WHERE %s IN (d.OwedToUserID, d.OwedByUserID) AND d.OwedToUserID != d.OwedByUserID
    GROUP BY friend_id, friend_name
    """
    return exec_get_all(debts_query, (user_id, user_id, user_id, user_id, user_id))


