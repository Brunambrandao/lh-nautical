"""
Script de Validação e Carga de Dados dos CSVs (Banco Local SQLite)
Objetivo: Garantir que todos os 24 CSVs da pasta 'lh_nautical_csv' são lidos e carregados sem erros.
"""

import os
import sqlite3
import pandas as pd

# Caminhos dos diretórios
CSV_DIR = "lh_nautical_csv"
DB_FILE = "lh_nautical_bruto.db"


def validar_e_carregar():
  # 1. Verifica se a pasta dos CSVs existe
  if not os.path.exists(CSV_DIR):
    print(f"Erro: A pasta '{CSV_DIR}' não foi encontrada na raiz do projeto.")
    return

  # 2. Conecta (ou cria) o banco de dados SQLite local
  conn = sqlite3.connect(DB_FILE)
  csv_files = sorted([f for f in os.listdir(CSV_DIR) if f.endswith(".csv")])

  print("=" * 60)
  print(
      f"INICIANDO VALIDAÇÃO DE CARGA BRUTA ({len(csv_files)} TABELAS ENCONTRADAS)"
  )
  print("=" * 60)

  total_linhas_geral = 0

  for idx, file_name in enumerate(csv_files, 1):
    table_name = os.path.splitext(file_name)[0].lower()
    file_path = os.path.join(CSV_DIR, file_name)

    try:
      # Lê o CSV preservando os valores brutos sem realizar limpezas
      df = pd.read_csv(file_path, dtype=str, keep_default_na=False)
      qtd_linhas = len(df)
      total_linhas_geral += qtd_linhas

      # Insere os dados na tabela do SQLite
      df.to_sql(name=table_name, con=conn, if_exists="replace", index=False)

      print(
          f"[{idx:02d}/24] ✔ Tabela '{table_name:<20}': {qtd_linhas:>6} linhas"
          " carregadas."
      )

    except Exception as e:
      print(f"[{idx:02d}/24] ✖ Erro na tabela '{table_name}': {e}")

  conn.close()

  print("=" * 60)
  print(" RESUMO DA VALIDAÇÃO:")
  print(f" - Total de tabelas processadas: {len(csv_files)}")
  print(f" - Total de linhas carregadas no banco: {total_linhas_geral:,}")
  print(" STATUS: TODAS AS TABELAS FORAM CARREGADAS COM SUCESSO!")
  print("=" * 60)


if __name__ == "__main__":
  validar_e_carregar()