#  Ingestão de Dados
#  Este módulo é responsável pela extração dos dados de diferentes fontes. 
# Ele conecta-se às APIs, bases de dados, ou lê arquivos CSV, JSON, etc.
# O módulo é responsável por coletar os dados e retorná-los em um formato
# tabular, geralmente um DataFrame do Pandas ou pyspark.

import requests
import pandas as pd
import sqlalchemy
import boto3

def collect_from_api(api_url):
    '''
    Coleta dados de uma API e retorna um DataFrame
    Args:
        api_url (str): URL da API
    Returns:
        pd.DataFrame: DataFrame com os dados da API
    '''
    response = requests.get(api_url)
    data = response.json()
    return pd.DataFrame(data)

def collect_from_database(connection_string, query):
    '''
    Coleta dados de uma base de dados e retorna um DataFrame
    Args:
        connection_string (str): String de conexão com a base de dados
        query (str): Query SQL para coleta dos dados
    Returns:
        pd.DataFrame: DataFrame com os dados da base de dados
    '''
    engine = sqlalchemy.create_engine(connection_string)
    data = pd.read_sql(query, engine)
    return data

def collect_from_file(file_path):
    '''
    Coleta dados de um arquivo e retorna um DataFrame
    Args:
        file_path (str): Caminho do arquivo
    Returns:
        pd.DataFrame: DataFrame com os dados do arquivo
    '''
    data = pd.read_csv(file_path)
    return data

def collect_aws_s3(bucket, file_key):
    '''
    Coleta dados de um arquivo no AWS S3 e retorna um DataFrame
    Args:
        bucket (str): Nome do bucket no AWS S3
        file_key (str): Caminho do arquivo no bucket
    Returns:
        pd.DataFrame: DataFrame com os dados do arquivo no S3
    '''
    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket=bucket, Key=file_key)
    data = pd.read_csv(obj['Body'])