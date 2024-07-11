from utilities.swen_344_db_utils import exec_get_all

def check_contacts_exist(contacts):
    # Extract unique contact numbers
    unique_contacts = list({contact['contact'] for contact in contacts})
    
    if not unique_contacts:
        return []

    placeholders = ', '.join(['%s'] * len(unique_contacts))
    query = f'''
        SELECT user_id, firstname FROM "user"
        WHERE contact_number IN ({placeholders})
    '''
    result = exec_get_all(query, tuple(unique_contacts))
    print("Result:",result)
    return result
