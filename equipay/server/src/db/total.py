from utilities.swen_344_db_utils import exec_get_one

def calculate_individual_total_owed(user_id):
    query = """
    SELECT 
    SUM(
        CASE 
            WHEN d.OwedToUserID = %s AND d.OwedByUserID != %s THEN d.AmountOwed
            WHEN d.OwedByUserID = %s AND d.OwedToUserID != %s THEN -d.AmountOwed
            ELSE 0
        END
    ) AS NetAmountCreditedToUser
    FROM 
        Debts d
    JOIN 
        Expenses e ON d.ExpenseID = e.ExpenseID
    WHERE 
        d.OwedToUserID = %s OR d.OwedByUserID = %s;
    """
    result = exec_get_one(query, (user_id, user_id, user_id, user_id, user_id, user_id))
    return result[0] if result else 0

def calculate_group_total_owed(user_id):
    query = """
    SELECT 
        SUM(
            CASE 
                WHEN gd.OwedToUserID = %s AND gd.OwedByUserID != %s THEN gd.AmountOwed
                WHEN gd.OwedByUserID = %s AND gd.OwedToUserID != %s THEN -gd.AmountOwed
                ELSE 0
            END
        ) AS NetAmountCreditedToUser
    FROM 
        GroupDebts gd
    JOIN 
        GroupExpenses ge ON gd.ExpenseID = ge.ExpenseID
    WHERE 
        ge.GroupID IN (SELECT GroupID FROM GroupMembers WHERE UserID = %s)
        AND (gd.OwedToUserID = %s OR gd.OwedByUserID = %s);
    """
    result = exec_get_one(query, (user_id, user_id, user_id, user_id, user_id, user_id, user_id))
    return result[0] if result else 0
