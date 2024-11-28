# connect.py
# Data: 14/11/2024
# Descrição: Este módulo conecta os dados de diferentes fontes 
# e os integra em uma estrutura comum. Ex: camada landing no S3.
# ----------------------------------------------------------

import pandas as pd

def connect_datasets(dataset_list):
    # Concatena os datasets em uma única tabela (DataFrame) consolidada
    return pd.concat(dataset_list, ignore_index=True)
