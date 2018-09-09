"""
Connections for databases and functions for generating connection 
string for SQL Alchemy and creating Pandas dataframe from SQL.

example:
-------------------
import sys
sys.path.append('/path/to/folder')
import connections as con

con.sql_to_dataframe('DISTRIBUTION', 'select * from proj_belysning.belysning limit 10')
-------------------
"""

import pandas as pd
from sqlalchemy import create_engine

CONNECTIONS = [
    {
        'PRODUCTION': {
            'host': 'xx',
            'dbname': 'xx',
            'user': 'xx',
            'password': 'xx',
            'port': 5432
        }
    }, {
        'DISTRIBUTION': {
            'host': 'xx',
            'dbname': 'xx',
            'user': 'xx',
            'password': 'xx',
            'port': 5432
        }
    }, {
        'COLLECTOR': {
            'host': 'xx',
            'dbname': 'xx',
            'user': 'xx',
            'password': 'xx',
            'port': 5432
        }
    }
]

def list_connections(connections=CONNECTIONS):
    """
    Printing names of availible connections
    """
    con_name_lst = [list(con.keys())[0] for con in connections]

    for name in con_name_lst:
        print(name)

def get_connection_sting(connection_name, connections=CONNECTIONS):
    """
    Returns connection string for SQL Alchemy engine.
    """

    # Validating connection name
    connection_name = connection_name.lower()
    con_name_lst = [list(con.keys())[0].lower() for con in connections]
    
    if connection_name not in con_name_lst:
        raise ValueError("Couldn't not find connection with given name")
    
    for name in connections:
        if connection_name == list(name.keys())[0].lower():
            server = list(name.values())[0]

    # Creating connection sting
    user =  server.get('user')
    password = server.get('password')
    host = server.get('host')
    port = server.get('port')
    dbname = server.get('dbname')

    con_str = f'postgresql://{user}:{password}@{host}:{port}/{dbname}'

    return con_str

def sql_to_dataframe(connection, query):
    """
    Takes DB connection and SQL query and return Pandas dataframe and the 
    sqlalchemy engine for returning modified data to PostgreSQL using pd.to_sql
    """

    con_str = get_connection_sting(connection)
    engine = create_engine(con_str)
    df = pd.read_sql_query(query,con=engine)

    return df, engine
