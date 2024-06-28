from utilities.swen_344_db_utils import exec_get_all

def get_contact():
    query = '''SELECT firstname, contact_number FROM "user";'''
    result = exec_get_all(query)
    print(result)
    return result
