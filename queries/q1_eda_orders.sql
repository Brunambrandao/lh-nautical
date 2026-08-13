-- Questão 1.1: Análise Exploratória Inicial (EDA) na Tabela 'orders'
-- Objetivo: Mapear volume, período temporal e métricas de distribuição sem tratamento prévio.

SELECT 
    -- Parte 1: Visão Geral da Tabela
    COUNT(*) AS total_linhas,
    MIN(created_at) AS data_minima,
    MAX(created_at) AS data_maxima,

    -- Parte 2: Análise da Coluna Numérica 'total'
    MIN(total) AS valor_minimo,
    MAX(total) AS valor_maximo,
    AVG(total) AS valor_medio,

    -- Diagnóstico Auxiliar: Verificação de Nulos
    COUNT(*) - COUNT(created_at) AS nulos_created_at,
    COUNT(*) - COUNT(total) AS nulos_total
FROM orders;