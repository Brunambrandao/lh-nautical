"""
Script de Execução - Questão 4 (Análise de Clientes Fiéis)
Alinhado à lógica de q4_analise_clientes.sql (sem fan-out por order_items)
"""

import sqlite3
import pandas as pd

DB_FILE = "lh_nautical_bruto.db"


def executar_q4():
  conn = sqlite3.connect(DB_FILE)

  # Consulta alinhada rigorosamente com a Questão 4.1 do desafio
  # (mesma estrutura de duas CTEs do arquivo q4_analise_clientes.sql,
  # evitando duplicação de o.total pelo JOIN com order_items)
  sql_top_10 = """
    WITH categorias_por_cliente AS (
        -- 1. Identifica a diversidade real de categorias por cliente
        SELECT
            o.customer_id,
            COUNT(DISTINCT p.category_id) AS diversidade_categorias
        FROM orders o
        JOIN order_items oi ON o.id = oi.order_id
        JOIN product_variants pv ON oi.product_variant_id = pv.id
        JOIN products p ON pv.product_id = p.id
        GROUP BY o.customer_id
        HAVING COUNT(DISTINCT p.category_id) >= 13
    ),
    metricas_pedidos AS (
        -- 2. Calcula faturamento e frequência SEM juntar com order_items,
        -- evitando que o.total seja somado uma vez por item do pedido
        SELECT
            o.customer_id,
            SUM(o.total) AS faturamento_total,
            COUNT(DISTINCT o.id) AS frequencia,
            (SUM(o.total) * 1.0 / COUNT(DISTINCT o.id)) AS ticket_medio
        FROM orders o
        WHERE o.customer_id IN (SELECT customer_id FROM categorias_por_cliente)
        GROUP BY o.customer_id
    )
    SELECT
        m.customer_id,
        m.faturamento_total,
        m.frequencia,
        m.ticket_medio,
        c.diversidade_categorias
    FROM metricas_pedidos m
    JOIN categorias_por_cliente c ON m.customer_id = c.customer_id
    ORDER BY m.ticket_medio DESC, m.customer_id ASC
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