"""
Script de Execução - Questão 5 (Dimensão de Calendário e Vendas por Dia da Semana)
"""

import sqlite3
import pandas as pd

DB_FILE = "lh_nautical_bruto.db"


def executar_q5():
  conn = sqlite3.connect(DB_FILE)

  # 1. Verificar colunas da tabela orders
  cursor = conn.cursor()
  cursor.execute("PRAGMA table_info(orders);")
  columns = [col[1] for col in cursor.fetchall()]

  date_col = next(
      (
          c
          for c in ["created_at", "order_date", "date", "created_date"]
          if c in columns
      ),
      columns[0],
  )
  channel_col = next(
      (
          c
          for c in [
              "channel",
              "sales_channel",
              "type",
              "order_type",
              "store_type",
          ]
          if c in columns
      ),
      None,
  )

  where_clause = ""
  if channel_col:
    where_clause = f"WHERE LOWER({channel_col}) = 'pos'"

  # 2. Query com dimensão de datas em SQLite (Gerador Recursivo de Datas)
  sql_q5 = f"""
    WITH RECURSIVE 
    range_datas AS (
        SELECT 
            MIN(DATE({date_col})) AS min_date,
            MAX(DATE({date_col})) AS max_date
        FROM orders
        {where_clause}
    ),
    calendario(data) AS (
        SELECT min_date FROM range_datas
        UNION ALL
        SELECT DATE(data, '+1 day')
        FROM calendario, range_datas
        WHERE data < max_date
    ),
    calendario_dow AS (
        SELECT 
            data,
            CAST(STRFTIME('%w', data) AS INT) AS dow_num,
            CASE CAST(STRFTIME('%w', data) AS INT)
                WHEN 0 THEN 'Domingo'
                WHEN 1 THEN 'Segunda-feira'
                WHEN 2 THEN 'Terça-feira'
                WHEN 3 THEN 'Quarta-feira'
                WHEN 4 THEN 'Quinta-feira'
                WHEN 5 THEN 'Sexta-feira'
                WHEN 6 THEN 'Sábado'
            END AS dia_semana
        FROM calendario
    ),
    vendas_diarias AS (
        SELECT 
            DATE({date_col}) AS data,
            SUM(CAST(total AS FLOAT)) AS valor_venda
        FROM orders
        {where_clause}
        GROUP BY DATE({date_col})
    )
    SELECT 
        c.dow_num,
        c.dia_semana,
        COUNT(c.data) AS total_dias_periodo,
        COUNT(v.data) AS dias_com_vendas,
        (COUNT(c.data) - COUNT(v.data)) AS dias_sem_vendas,
        ROUND(COALESCE(SUM(v.valor_venda), 0), 2) AS faturamento_total,
        ROUND(COALESCE(SUM(v.valor_venda), 0) / COUNT(c.data), 2) AS media_vendas_diaria
    FROM calendario_dow c
    LEFT JOIN vendas_diarias v ON c.data = v.data
    GROUP BY c.dow_num, c.dia_semana
    ORDER BY media_vendas_diaria ASC;
    """

  df_result = pd.read_sql_query(sql_q5, conn)

  print("=" * 75)
  print(" RESULTADO DA ANÁLISE DE VENDAS POR DIA DA SEMANA (COM DIMENSÃO DE DATA)")
  print("=" * 75)
  print(df_result.to_string(index=False))

  conn.close()


if __name__ == "__main__":
  executar_q5()