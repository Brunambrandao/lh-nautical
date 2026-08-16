-- Questão 5.1: Média Real de Vendas por Dia da Semana com Dimensão de Calendário
-- Dialeto: PostgreSQL (Lojas Físicas / POS)

WITH range_datas AS (
    -- Captura o intervalo completo de datas da loja física (channel = 'pos')
    SELECT 
        MIN(CAST(created_at AS DATE)) AS min_date,
        MAX(CAST(created_at AS DATE)) AS max_date
    FROM orders
    WHERE LOWER(channel) = 'pos'
),
calendario AS (
    -- Gera uma linha para cada dia corrido do período
    SELECT 
        generate_series(min_date, max_date, '1 day'::interval)::date AS data
    FROM range_datas
),
calendario_dow AS (
    -- Converte o dia da semana para o formato legível em português
    SELECT 
        data,
        EXTRACT(DOW FROM data) AS dow_num,
        CASE EXTRACT(DOW FROM data)
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
    -- Soma o faturamento total por data para a loja física
    SELECT 
        CAST(created_at AS DATE) AS data,
        SUM(total) AS valor_venda
    FROM orders
    WHERE LOWER(channel) = 'pos'
    GROUP BY CAST(created_at AS DATE)
)
-- Cruzamento via LEFT JOIN para contabilizar dias sem venda como R$ 0,00
SELECT 
    c.dia_semana,
    COUNT(c.data) AS total_dias_periodo,
    COUNT(v.data) AS dias_com_vendas,
    (COUNT(c.data) - COUNT(v.data)) AS dias_sem_vendas,
    COALESCE(SUM(v.valor_venda), 0) AS faturamento_total,
    ROUND(COALESCE(SUM(v.valor_venda), 0) / COUNT(c.data), 2) AS media_vendas_diaria
FROM calendario_dow c
LEFT JOIN vendas_diarias v ON c.data = v.data
GROUP BY c.dow_num, c.dia_semana
ORDER BY media_vendas_diaria ASC;
