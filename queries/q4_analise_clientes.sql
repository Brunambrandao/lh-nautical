-- Questão 4.1: Análise de Clientes Fiéis (Elite)
-- Mapeamento dos TOP 10 clientes por Ticket Médio com pelo menos 13 categorias distintas compradas

WITH categorias_por_cliente AS (
    -- 1. Identifica a diversidade de categorias reais por cliente
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
    -- 2. Calcula faturamento e frequencia exatos sem duplicar valores pelos itens
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