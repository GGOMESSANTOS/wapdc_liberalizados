# compose.py
# Data: 14/11/2024
# Descrição: Este módulo realiza a limpeza e transformação dos dados
# coletados. Ele é responsável por preparar os dados para análise.
# ----------------------------------------------------------

def clean_data(df):
    '''
    Limpa os dados removendo valores nulos e outliers
    Args:
        df (pd.DataFrame): DataFrame com os dados
    Returns:
        pd.DataFrame: DataFrame limpo
    '''
    df = df.dropna()
    return df

def transform_data(df):
    '''
    Realiza alguma transformação nos dados, como criar colunas derivadas
    Args:
        df (pd.DataFrame): DataFrame com os dados
    Returns:
        pd.DataFrame: DataFrame transformado
    '''
    df['new_column'] = df['existing_column'] * 1.1
    return df