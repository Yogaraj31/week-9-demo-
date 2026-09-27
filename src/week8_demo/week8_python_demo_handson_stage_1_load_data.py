import pandas as pd
import sqlite3

def load_data(database_file_path, database_sql):
    
    with sqlite3.connect(database_file_path) as conn:
        df = pd.read_sql_query(
        database_sql,
        conn,
    )
    return df