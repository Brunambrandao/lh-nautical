# 📊 LH Náutico — Análise de Dados & Business Intelligence

Este repositório contém a solução completa de análise de dados, modelagem SQL, relatórios diagnósticos e dashboards interativos desenvolvidos para o projeto **LH Náutico**. 

O objetivo principal do projeto é transformar dados brutos de vendas, clientes e produtos em *insights* estratégicos para suporte à tomada de decisão executiva.

---

## 🛠️ Tecnologias e Ferramentas Utilizadas

- **SQL / SQLite:** Modelagem de dados, criação de views e consultas analíticas avançadas.
- **Python:** Automação de execução de queries e processamento de dados (`pandas`, `sqlite3`).
- **Power BI:** Construção de dashboards interativos e visualização de dados.
- **Git & GitHub:** Controle de versão e documentação de código.

---

## 📁 Estrutura do Repositório

```text
lh-nautico/
├── dashboards/                  # Arquivos de Business Intelligence e imagens
│   ├── images/                  # Capturas de tela dos dashboards desenvolvidos
│   └── dashboard_lh_nautical.pbix
├── docs/                        # Documentação detalhada e diagnósticos por questão
│   ├── q1_diagnostico.md
│   ├── q4_analise_clientes.md
│   ├── q5_dimensao_calendario.md
│   ├── q6_previsao_demanda.md
│   └── q7_sistema_recomendacao.md
├── lh_nautical_csv/             # Base de dados em formato CSV
├── queries/                     # Scripts de automação Python e consultas SQL (.sql)
├── .gitignore                   # Arquivos ignorados pelo Git
├── lh_nautical_bruto.db         # Banco de dados SQLite
└── README.md                    # Documentação principal do projeto