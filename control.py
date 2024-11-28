# Monitoramento e Orquestração
# Data: 17/08/2021
# Descrição: Script de controle do pipeline de dados
# -------------------------------------------------------

# control.py
import great_expectations as ge
from collect import collect_from_api, collect_from_database
from connect import connect_datasets
from compose import clean_data, transform_data
from consume import save_to_database, save_to_csv

class GreatExpectations:
    def __init__(self, dataframe, expectations_config=None):
        """
        Inicializa o verificador de qualidade de dados com um DataFrame e configurações de expectativas.
        
        :param dataframe: pd.DataFrame - Dados a serem verificados.
        :param expectations_config: dict - Configurações para expectativas de qualidade de dados.
        """
        self.df = ge.from_pandas(dataframe)
        self.expectations_config = expectations_config or {}

    def set_expectations(self):
        """
        Define expectativas com base nas configurações fornecidas.
        """
        for field, expectations in self.expectations_config.get('fields', {}).items():
            if expectations.get('completeness', False):
                self.df.expect_column_values_to_not_be_null(field)

            if expectations.get('uniqueness', False):
                self.df.expect_column_values_to_be_unique(field)

            if 'consistency' in expectations:
                expected_values = expectations['consistency']
                self.df.expect_column_values_to_be_in_set(field, expected_values)

            if 'accuracy' in expectations:
                min_value = expectations['accuracy'].get('min', None)
                max_value = expectations['accuracy'].get('max', None)
                if min_value is not None:
                    self.df.expect_column_values_to_be_greater_than_or_equal_to(field, min_value)
                if max_value is not None:
                    self.df.expect_column_values_to_be_less_than_or_equal_to(field, max_value)

            if 'integrity' in expectations:
                foreign_key = expectations['integrity'].get('foreign_key')
                reference_values = expectations['integrity'].get('reference_values')
                if foreign_key and reference_values:
                    self.df.expect_column_values_to_be_in_set(foreign_key, reference_values)

    def run_quality_checks(self):
        """
        Executa as verificações de qualidade de dados com base nas expectativas definidas e retorna o resultado.
        """
        self.set_expectations()
        results = self.df.validate()
        if not results['success']:
            logging.warning("Uma ou mais verificações de qualidade falharam.")
        else:
            logging.info("Todas as verificações de qualidade foram bem-sucedidas.")
        return results

    def generate_report(self, report_path='data_quality_report.html'):
        """
        Gera um relatório HTML das verificações de qualidade de dados.
        
        :param report_path: Caminho onde o relatório será salvo.
        """
        results = self.run_quality_checks()
        validation_docs = ge.data_context.DataContext()
        validation_docs.build_data_docs()
        validation_docs.open_data_docs(results['run_id'])

def execute_bronze():
    # Etapa de coleta
    data_api = collect_from_api('https://api.example.com/data')
    data_db = collect_from_database('sqlite:///mydatabase.db', 'SELECT * FROM table')

    # Etapa de conexão
    data_combined = connect_datasets([data_api, data_db])

    # Etapa de composição
    data_cleaned = clean_data(data_combined)
    data_transformed = transform_data(data_cleaned)

    # Etapa de consumo
    save_to_database(data_transformed, 'sqlite:///mydatabase.db', 'processed_data')
    save_to_csv(data_transformed, 'processed_data.csv')
    
    print("Pipeline executado com sucesso!")

if __name__ == "__main__":
    execute_bronze()
