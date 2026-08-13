"""
Script de Execução - Questão 4 (Análise de Clientes Fiéis)
"""

import sqlite3
import pandas as pd

DB_FILE = "lh_nautical_bruto.db"


def executar_q4():
  conn = sqlite3.connect(DB_FILE)

  # Consulta 1: TOP 10 Clientes de Elite (Ticket Médio com >= 13 categorias)
  sql_top_10 = """
    WITH cliente_metricas AS (
        SELECT 
            o.customer_id,
            SUM(DISTINCT o.total) AS faturamento_total,
            COUNT(DISTINCT o.id) AS frequencia,
            (CAST(SUM(DISTINCT o.total) AS FLOAT) / COUNT(DISTINCT o.id)) AS ticket_medio,
            COUNT(DISTINCT p.category_id) AS diversidade_categorias
        FROM orders o
        JOIN order_items oi ON o.id = oi.order_id
        JOIN product_variants pv ON oi.product_variant_id = pv.id
        JOIN products p ON pv.product_id = p.id
        WHERE o.total IS NOT NULL AND o.total != ''
        GROUP BY o.customer_id
        HAVING COUNT(DISTINCT p.category_id) >= 13
    )
    SELECT 
        customer_id,
        faturamento_total,
        frequencia,
        ticket_medio,
        diversidade_categorias
    FROM cliente_metricas
    ORDER BY ticket_medio DESC, customer_id ASC
    LIMIT 10;
    """

  df_top10 = pd.read_sql_query(sql_top_10, conn)

  print("=" * 65)
  print(" TOP 10 CLIENTES FIÉIS (ELEGÍVEIS - DIVERSIDADE >= 13 CATEGORIAS)")
  print("=" * 65)
  print(df_top10.to_string(index=False))

  # Guardar a lista de IDs dos 10 clientes
  top_10_ids = tuple(df_top10["customer_id"].tolist())

  # Consulta 2: Categoria mais vendida em quantidade de itens para esse TOP 10
  sql_categoria = f"""
    SELECT 
        c.id AS category_id,
        c.name AS nome_categoria,
        SUM(CAST(oi.quantity AS INT)) AS total_itens_comprados
    FROM orders o
    JOIN order_items oi ON o.id = oi.order_id
    JOIN product_variants pv ON oi.product_variant_id = pv.id
    JOIN products p ON pv.product_id = p.id
    JOIN categories c ON p.category_id = c.id
    WHERE o.customer_id IN {top_10_ids}
    GROUP BY c.id, c.name
    ORDER BY total_itens_comprados DESC;
    """

  df_cat = pd.read_sql_query(sql_categoria, conn)

  print("\n" + "=" * 65)
  print(" CATEGORIAS MAIS COMPRADAS PELO TOP 10 CLIENTES (EM QTD DE ITENS)")
  print("=" * 65)
  print(df_cat.to_string(index=False))

  conn.close()


if __name__ == "__main__":
  executar_q4()