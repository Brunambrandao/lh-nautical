# LH Nautical — Desafio Lighthouse (Dados e IA)

Solução completa do desafio técnico da Indicium para a vaga de Trainee em Dados e IA, aplicada ao cenário fictício da **LH Nautical**, uma varejista náutica com lojas físicas, armazéns e e-commerce, com dados operacionais cobrindo o período de 2020 a 2026.

O objetivo do projeto é percorrer um pipeline de dados de ponta a ponta: da ingestão de dados brutos (CSV) até a geração de insights de negócio, previsão de demanda e um sistema de recomendação, sempre priorizando organização, clareza de raciocínio e rastreabilidade das decisões técnicas.

## Sobre o desafio

O desafio simula uma situação real: os dados da empresa chegam desorganizados em 24 arquivos CSV, e cabe a mim estruturar o schema, carregar os dados sem alterá-los, e responder a perguntas de negócio feitas por três stakeholders fictícios: o Tech Lead (visão técnica), a Gerente de Negócios (foco em performance) e o Fundador (cético em relação à tecnologia, precisa ser convencido por dados).

## Etapas realizadas

| # | Etapa | Entregável | Tecnologia |
|---|---|---|---|
| 1 | EDA inicial na tabela `orders` | Consulta SQL sem tratamento prévio dos dados | SQL |
| 2 | Geração do schema (DDL) a partir dos CSVs | `schema.sql` + script gerador | Python 3 (stdlib apenas) |
| 3 | Carregamento bruto dos 24 CSVs | Script de carga sem limpeza/tratamento | Python + pandas + SQLAlchemy |
| 4 | Análise de clientes fiéis (ticket médio x diversidade de categorias) | Consulta SQL com CTEs | SQL |
| 5 | Dimensão de calendário e vendas médias por dia da semana | Consulta SQL com geração de série de datas | SQL |
| 6 | Previsão de demanda (média móvel de 3 meses) | Script com validação de MAE | Python + pandas |
| 7 | Sistema de recomendação por similaridade de cosseno | Script com matriz usuário × produto | Python + pandas + scikit-learn |
| 8 | Dashboard de vendas e performance | Painel interativo (5 páginas) | Power BI |

## Estrutura do repositório

```
lh-nautical/
├── dashboards/                  # Arquivos de Business Intelligence e imagens
│   ├── images/                  # Capturas de tela do dashboard (5 páginas)
│   └── dashboard_lh_nautical.pbix
├── docs/                        # Documentação detalhada e diagnósticos por questão
│   ├── q1_diagnostico.md
│   ├── q4_analise_clientes.md
│   ├── q5_dimensao_calendario.md
│   ├── q6_previsao_demanda.md
│   └── q7_sistema_recomendacao.md
├── lh_nautical_csv/             # Base de dados em formato CSV (24 tabelas brutas)
├── queries/                     # Consultas SQL e scripts de execução por questão
│   ├── q1_eda_orders.sql
│   ├── q4_analise_clientes.sql
│   ├── rodar_q1.py ... rodar_q7.py
│   └── scripts/                 # Scripts de infraestrutura (schema e carga)
│       ├── generate_schema.py
│       ├── load_data.py
│       └── test_load.py
├── .gitignore                   # Arquivos ignorados pelo Git
├── LICENSE                      # Licença MIT
├── lh_nautical_bruto.db         # Banco de dados SQLite (dados brutos, para testes)
├── schema.sql                   # DDL gerado a partir dos CSVs
└── README.md                    # Documentação principal do projeto
```

## Como executar

1. Clone o repositório e instale as dependências:
   ```bash
   pip install pandas sqlalchemy scikit-learn numpy
   ```
2. Para gerar o schema a partir dos CSVs:
   ```bash
   python queries/scripts/generate_schema.py
   ```
3. Para carregar os dados brutos (SQLite local, usado para validação rápida):
   ```bash
   python queries/scripts/test_load.py
   ```
4. Para carregar em um PostgreSQL (defina as variáveis de ambiente `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `DB_NAME`):
   ```bash
   python queries/scripts/load_data.py
   ```
5. Para rodar as análises de cada questão:
   ```bash
   python queries/rodar_q1.py
   python queries/rodar_q4.py
   python queries/rodar_q5.py
   python queries/rodar_q6.py
   python queries/rodar_q7.py
   ```

## Principais decisões técnicas

- **Sem tratamento nas etapas de EDA e carregamento (Q1 e Q3):** por exigência do desafio, os dados foram mantidos em seu estado bruto (`dtype=str`, sem remoção de nulos) para preservar a fidelidade da camada raw.
- **Schema gerado apenas com bibliotecas nativas (Q2):** a inferência de tipo por coluna prioriza `TEXT` sempre que há qualquer inconsistência na amostra, para evitar erros de carga por tipagem incorreta.
- **Dimensão de calendário construída via SQL (Q5):** necessária para evitar viés de sobrevivência ao calcular médias de vendas por dia da semana — dias sem vendas registradas são contabilizados como R$ 0,00 em vez de serem ignorados.
- **Modelo de previsão com prevenção de vazamento de dados (Q6):** a média móvel usa `shift(1)` antes do `rolling`, garantindo que a previsão de um mês nunca "veja" dados do próprio mês.
- **Sistema de recomendação binário (Q7):** a matriz usuário × produto ignora quantidade e considera apenas presença/ausência de compra, isolando o sinal de co-ocorrência entre produtos.

## Dashboard

O painel de Vendas e Performance foi construído em Power BI e está **finalizado**, com 5 páginas:

1. **Capa** — identificação do projeto e autoria.
2. **Visão Geral / Vendas** — indicadores gerais (total de pedidos, faturamento, ticket médio, total de clientes), evolução de faturamento por mês/ano, top 10 produtos mais vendidos e vendas médias por dia da semana (Questão 5).
3. **Clientes** — ranking dos 10 clientes fiéis (Questão 4), categoria com mais itens comprados pelo grupo elite e distribuição de diversidade de categorias por cliente.
4. **Previsão de Demanda** — vendas reais vs. previsão baseline (MM3) para "Bússola de Bordo 702", MAE do modelo e discussão da limitação de sazonalidade (Questão 6).
5. **Recomendação de Produtos** — lógica do modelo de similaridade de cosseno e top 5 produtos similares ao "Motor de Popa 1949" (Questão 7).

O arquivo do dashboard está em `dashboards/dashboard_lh_nautical.pbix`, com capturas de tela em `dashboards/images/`.


## Licença

Este projeto está licenciado sob os termos da licença **MIT** — veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## Autor

Bruna Brandão