-- Questão 4.1: Análise de Clientes Fiéis (Elite)
-- Mapeamento dos TOP 10 clientes por Ticket Médio com pelo menos 13 categorias distintas compradas

WITH cliente_metricas AS (
    SELECT 
        o.customer_id,
        SUM(o.total) AS faturamento_total,
        COUNT(DISTINCT o.id) AS frequencia,
        (SUM(o.total) * 1.0 / COUNT(DISTINCT o.id)) AS ticket_medio,
        COUNT(DISTINCT p.category_id) AS diversidade_categorias
    FROM orders o
    INNER JOIN order_items oi ON o.id = oi.order_id
    INNER JOIN product_variants pv ON oi.product_variant_id = pv.id
    INNER JOIN products p ON pv.product_id = p.id
    GROUP BY o.customer_id
    HAVING COUNT(DISTINCT p.category_id) >= 13
),
top_10_clientes AS (
    SELECT 
        customer_id,
        faturamento_total,
        frequencia,
        ticket_medio,
        diversidade_categorias
    FROM cliente_metricas
    ORDER BY ticket_medio DESC, customer_id ASC
    LIMIT 10
)
SELECT * FROM top_10_clientes;