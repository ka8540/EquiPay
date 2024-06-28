from utilities.swen_344_db_utils import exec_get_all

def get_graph_values(user_id):
    query = '''
    SELECT amount, date FROM Expenses WHERE PayerID = %s
    UNION ALL
    SELECT amount, date FROM GroupExpenses WHERE PayerID = %s;
    '''
    results = exec_get_all(query, (user_id, user_id))
    return results
