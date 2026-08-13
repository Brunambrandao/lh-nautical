# Questão 1 - Análise Exploratória de Dados (EDA) na Tabela `orders`

## Parte 1 & 2 - Resumo dos Dados
- **Quantidade Total de Linhas:** 48.998
- **Intervalo de Datas (`created_at`):** 01/01/2020 01:19:28 até 31/12/2026 23:43:09
- **Valor Mínimo (`total`):** R$ 32,62
- **Valor Máximo (`total`):** R$ 127.262,02
- **Valor Médio (`total`):** R$ 28.704,99

---

## Parte 3 - Interpretação e Diagnóstico de Confiabilidade

### 1. Possíveis Outliers em `total`
O valor máximo encontrado (R$ 127.262,02) é substancialmente superior à média geral (R$ 28.704,99). Essa forte discrepância indica uma alta assimetria à direita na distribuição das vendas e a presença marcante de *outliers* — que podem representar compras corporativas/frotas de alto valor ou incoerências registradas no sistema.

### 2. Qualidade dos Dados
O valor mínimo é positivo (R$ 32,62), indicando ausência de valores zerados ou negativos diretamente na coluna `total`. A janela temporal está consistente (2020 a 2026). No entanto, o volume bruto de 48.998 registros ainda necessita de cruzamento com tabelas de itens, pagamentos e devoluções para identificar eventuais pedidos cancelados ou órfãos.

### 3. Conclusão para a Diretoria (Sr. Almir & Gabriel Santos)
**A tabela `orders` em seu estado bruto NÃO está pronta para tomada de decisões estratégicas.** 

Embora o volume de dados seja robusto, a forte presença de outliers e a ausência de filtros por status (cancelamentos/devoluções) distorcem a média de faturamento. **Recomenda-se um tratamento e higienização prévia (Data Cleaning)** antes de utilizar esses dados em relatórios de desempenho ou modelos preditivos.