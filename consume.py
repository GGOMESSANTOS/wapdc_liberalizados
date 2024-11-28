# consume.py
# Autor: Jairo Lopes
# Data: 2020-12-20
# Descrição: Funções para consumir dados de diferentes fontes. 
# Democratização dos Dados
# ----------------------------------------------------------

def save_to_database(df, connection_string, table_name):
    import sqlalchemy
    engine = sqlalchemy.create_engine(connection_string)
    df.to_sql(table_name, engine, if_exists='replace', index=False)

def save_to_csv(df, file_path):
    df.to_csv(file_path, index=False)

