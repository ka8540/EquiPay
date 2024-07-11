from utilities.swen_344_db_utils import exec_get_all

def normalize_contact(contact):
    # Ensure all contact numbers are prefixed with a plus sign
    clean_contact = ''.join(filter(str.isdigit, contact))
    return f'+{clean_contact}'  # Prepend the plus sign to match the database format

def check_contacts_exist(contacts):
    # Normalize and extract unique contact numbers
    unique_contacts = list({normalize_contact(contact['contact']) for contact in contacts})
    
    if not unique_contacts:
        return []

    placeholders = ', '.join(['%s'] * len(unique_contacts))
    query = f'''
        SELECT user_id, firstname FROM "user"
        WHERE contact_number IN ({placeholders})
    '''
    result = exec_get_all(query, tuple(unique_contacts))
    print("Result:", result)
    return result
