import sqlite3
import pandas as pd

# Conexão com o banco de dados
conn = sqlite3.connect("lh_nautical_bruto.db")

# Consulta alinhada rigorosamente com a Questão 4.1 do desafio
query_q4 = """
WITH cliente_metricas AS (
    SELECT   
        o.customer_id,
        SUM(o.total) AS faturamento_total, -- Removido DISTINCT para somar todos os pedidos
        COUNT(DISTINCT o.id) AS frequencia,
        (SUM(o.total) * 1.0 / COUNT(DISTINCT o.id)) AS ticket_medio,
        COUNT(DISTINCT p.category_id) AS diversidade_categorias
    FROM orders o
    JOIN order_items oi ON o.id = oi.order_id
    JOIN product_variants pv ON oi.product_variant_id = pv.id
    JOIN products p ON pv.product_id = p.id
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

df_q4 = pd.read_sql_query(query_q4, conn)
conn.close()

print(df_q4)