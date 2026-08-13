"""
Questão 2.1 - Gerador de Schema SQL (PostgreSQL) a partir de arquivos CSV

"""

import csv
import os
import re
from datetime import datetime


def infer_pg_type(val_str):
    """
    Infere o tipo de dado compatível com PostgreSQL para um valor individual em string.
    Retorna uma string representando o tipo sugerido.
    """
    val = val_str.strip()

    # Caso 1: Valor vazio/nulo
    if not val or val.lower() in ('null', 'none', ''):
        return None

    # Caso 2: Booleano
    if val.lower() in ('true', 'false', 't', 'f'):
        return 'BOOLEAN'

    # Caso 3: Inteiro
    if re.match(r'^-?\d+$', val):
        return 'BIGINT'

    # Caso 4: Decimal / Float
    if re.match(r'^-?\d+\.\d+$', val):
        return 'NUMERIC'

    # Caso 5: Data e Hora (TIMESTAMP)
    for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S.%f'):
        try:
            datetime.strptime(val, fmt)
            return 'TIMESTAMP'
        except ValueError:
            pass

    # Caso 6: Apenas Data (DATE)
    try:
        datetime.strptime(val, '%Y-%m-%d')
        return 'DATE'
    except ValueError:
        pass

    # Caso Padrão: Texto
    return 'TEXT'


def resolve_type_priority(types_found):
    """
    Define o tipo final da coluna do PostgreSQL com base nos tipos encontrados nas linhas.
    Prioridade: TEXT > TIMESTAMP > DATE > NUMERIC > BIGINT > BOOLEAN
    """
    # Remove Nulos
    types_found = {t for t in types_found if t is not None}

    if not types_found:
        return 'TEXT'  # Se a coluna for 100% nula na amostragem

    if 'TEXT' in types_found:
        return 'TEXT'

    if 'TIMESTAMP' in types_found:
        return 'TIMESTAMP'

    if 'DATE' in types_found:
        return 'DATE'

    if 'NUMERIC' in types_found:
        return 'NUMERIC'

    if 'BIGINT' in types_found:
        return 'BIGINT'

    if 'BOOLEAN' in types_found:
        return 'BOOLEAN'

    return 'TEXT'


def generate_schema(csv_dir, output_file, max_sample_rows=1000):
    """
    Lê todos os CSVs de um diretório e gera o arquivo DDL schema.sql para PostgreSQL.
    """
    if not os.path.exists(csv_dir):
        print(f"Erro: O diretório '{csv_dir}' não foi encontrado.")
        return

    csv_files = sorted([f for f in os.listdir(csv_dir) if f.endswith('.csv')])

    if not csv_files:
        print(f"Nenhum arquivo CSV encontrado em '{csv_dir}'.")
        return

    print(f"Encontrados {len(csv_files)} arquivos CSV. Gerando DDL PostgreSQL...")

    sql_statements = []
    sql_statements.append("-- ========================================================")
    sql_statements.append("-- DDL de Criação de Tabelas - LH Nautical (PostgreSQL)")
    sql_statements.append(f"-- Gerado automaticamente em Python (Bibliotecas Nativas)")
    sql_statements.append("-- ========================================================\n")

    for file_name in csv_files:
        table_name = os.path.splitext(file_name)[0].lower()
        file_path = os.path.join(csv_dir, file_name)

        with open(file_path, mode='r', encoding='utf-8', errors='ignore') as f:
            reader = csv.reader(f)
            try:
                headers = next(reader)
            except StopIteration:
                print(f"Aviso: Arquivo '{file_name}' está vazio. Pulando...")
                continue

            headers = [h.strip().lower() for h in headers]
            column_types = {h: set() for h in headers}

            # Amostragem de linhas para inferência de performance
            row_count = 0
            for row in reader:
                if row_count >= max_sample_rows:
                    break
                row_count += 1

                for col_name, val in zip(headers, row):
                    inferred = infer_pg_type(val)
                    if inferred:
                        column_types[col_name].add(inferred)

        # Monta a estrutura DDL
        sql_statements.append(f"CREATE TABLE IF NOT EXISTS {table_name} (")
        col_defs = []
        for col_name in headers:
            final_type = resolve_type_priority(column_types[col_name])
            col_defs.append(f"    {col_name} {final_type}")

        sql_statements.append(",\n".join(col_defs))
        sql_statements.append(");\n")

    # Escreve o arquivo final schema.sql
    with open(output_file, mode='w', encoding='utf-8') as out_f:
        out_f.write("\n".join(sql_statements))

    print(f"Sucesso! O arquivo '{output_file}' foi gerado com {len(csv_files)} tabelas.")


if __name__ == "__main__":
    # Caminho da pasta contendo os CSVs e local do arquivo de saída
    DIRECTORY_CSV = "lh_nautical_csv"
    OUTPUT_SQL = "schema.sql"

    generate_schema(DIRECTORY_CSV, OUTPUT_SQL)