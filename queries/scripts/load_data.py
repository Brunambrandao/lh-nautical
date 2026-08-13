"""
Questão 3.1 - Script de Carregamento de Dados (CSV para PostgreSQL)
Premissas:
- Carregar todos os 24 arquivos CSV para o banco bruto.
- Preservar os dados sem realizar tratamentos (sem remoção de nulos/caracteres).
"""

import os
import pandas as pd
from sqlalchemy import create_engine

# 1. Configurações de Conexão com o PostgreSQL
# (Ajuste os parâmetros caso esteja usando credenciais locais específicas)
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "lh_nautical")

# Diretório dos arquivos CSV
CSV_DIR = "lh_nautical_csv"


def get_db_engine():
  """Cria e retorna a engine de conexão com o PostgreSQL usando SQLAlchemy."""
  connection_string = (
      f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
  )
  return create_engine(connection_string)


def load_all_csvs(csv_directory):
  """Lê todos os CSVs do diretório e insere as tabelas brutas no PostgreSQL."""
  if not os.path.exists(csv_directory):
    print(f"Erro: Diretório '{csv_directory}' não encontrado.")
    return

  engine = get_db_engine()
  csv_files = sorted([f for f in os.listdir(csv_directory) if f.endswith(".csv")])

  print(f"Iniciando o carregamento de {len(csv_files)} arquivos CSV...")

  for file_name in csv_files:
    table_name = os.path.splitext(file_name)[0].lower()
    file_path = os.path.join(csv_directory, file_name)

    print(f"-> Carregando '{file_name}' para a tabela '{table_name}'...")

    try:
      # Lê o CSV preservando os tipos e valores originais (dtype=str evita conversões indesejadas)
      df = pd.read_csv(file_path, dtype=str, keep_default_na=False)

      # Insere no PostgreSQL substituindo o conteúdo caso a tabela já exista
      df.to_sql(
          name=table_name,
          con=engine,
          if_exists="replace",
          index=False,
          method="multi",
          chunksize=5000,
      )

      print(
          f"   Sucesso: {len(df)} linhas inseridas na tabela '{table_name}'."
      )

    except Exception as e:
      print(f"   Erro ao carregar '{file_name}': {e}")

  print("\n========================================================")
  print(" Carregamento de todos os arquivos concluído com sucesso!")
  print("========================================================")


if __name__ == "__main__":
  load_all_csvs(CSV_DIR)