import psycopg2
import yaml
import os

def connect():
    config = {}
    yml_path = os.path.join(os.path.dirname(__file__), '../../config/db.yml') #db.yml
    # yml_path ='config/db.yml'
    with open(yml_path, 'r') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    return psycopg2.connect(dbname=config['database'],
                            user=config['user'],
                            password=config['password'],
                            host=config['host'],
                            port=config['port'])

def exec_sql_file(path):
    full_path = os.path.join(os.path.dirname(__file__), f'../../{path}')
    conn = connect()
    cur = conn.cursor()
    with open(full_path, 'r') as file:
        cur.execute(file.read())
    conn.commit()
    conn.close()

def exec_get_one(sql, args={}):
    conn = connect()
    cur = conn.cursor()
    cur.execute(sql, args)
    one = cur.fetchone()
    conn.close()
    return one

def exec_get_all(sql, args={}):
    conn = connect()
    cur = conn.cursor()
    cur.execute(sql, args)
    # https://www.psycopg.org/docs/cursor.html#cursor.fetchall

    list_of_tuples = cur.fetchall()
    conn.close()
    return list_of_tuples

def exec_commit(sql, args={}):
    conn = connect()
    cur = conn.cursor()
    result=cur.execute(sql, args)
    conn.commit()
    conn.close()
    return result

def exec_fetch(sql,args={}):
    conn = connect()
    cur = conn.cursor()
    cur.execute(sql, args)
    result = cur.fetchone()
    conn.commit()
    conn.close()
    return result

def commit_dataframe(df, table):
    """Insert a DataFrame into a specified table and return the ID of the first inserted record."""
    conn = connect()
    # Preparing SQL for inserting data
    column_str = ','.join(['%s' for _ in df.columns])  # Fixed to use _ for unused loop variable
    cols = ','.join(list(df.columns))
    query = f"INSERT INTO {table} ({cols}) VALUES ({column_str}) RETURNING id"
    
    with conn:
        with conn.cursor() as cursor:
            try:
                # Executing the insert query with the first row of the DataFrame
                cursor.execute(query, tuple(df.iloc[0]))
                id_of_new_row = cursor.fetchone()[0]
                conn.commit()  # Commit is redundant here because of the 'with' context manager
                return id_of_new_row
            except psycopg2.DatabaseError as error:
                # Log the error and rollback the transaction if an error occurs
                print(f"Error: {error}")
                conn.rollback()
                return None
            finally:
                cursor.close()

def update_dataframe(df, table, record_id):
    """Update records in a table from a DataFrame based on the ID."""
    with connect() as conn:
        with conn.cursor() as cur:
            # Convert DataFrame rows to tuples, adding the record_id at the end for the WHERE clause
            tuples = [tuple(x) for x in df.to_numpy()]
            tuples[0] = tuples[0] + (record_id,)
            # Generate the SET part of the SQL statement dynamically from DataFrame columns
            cols = ', '.join([f"{col} = %s" for col in df.columns])
            query = f"UPDATE {table} SET {cols} WHERE id = %s RETURNING id"
            # Execute the UPDATE query with the tuple containing column values and the record_id
            cur.execute(query, tuples[0])
            updated_record_id = cur.fetchone()[0]  # Fetch the returned id after the update
            conn.commit()  # Commit the transaction to make sure changes are saved
            return updated_record_id

