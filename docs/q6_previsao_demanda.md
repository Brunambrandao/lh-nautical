# Questão 6 — Resultados e Avaliação do Modelo Baseline

## 📊 Resultados do Período de Teste (1º Trimestre / 2026)

| Mês / Ano | Vendas Reais (`quantidade_real`) | Previsão Baseline (`previsao_baseline`) | Erro Absoluto |
| :---: | :---: | :---: | :---: |
| **2026-01** | **152.0** | **80.33** | **71.67** |
| **2026-02** | **98.0** | **110.67** | **12.67** |
| **2026-03** | **105.0** | **101.67** | **3.33** |

---

### 📈 Métrica Consolidada
* **MAE (Mean Absolute Error):** `29.22` unidades

---

## 💡 Avaliação do Modelo Baseline

### a. O baseline é adequado para esse produto?
**Não.** O modelo apresentou um erro médio de **29.22 unidades**, sendo crítico no mês de pico de vendas (**Janeiro/2026**). Em Janeiro, a demanda real foi de **152 unidades**, mas a previsão baseline indicou apenas **80.33 unidades** (uma subestimativa severa de **71.67 unidades**), o que geraria uma grave ruptura de estoque no auge do verão.

### b. Limitação Técnica do Método
**Incapacidade de capturar Sazonalidade (Atraso Temporal / Lag Effect):** A média móvel é um método exclusivamente reativo e suavizado. Por olhar apenas para os 3 meses imediatamente anteriores (Outubro, Novembro e Dezembro), ela ignora os picos sazonais característicos do segmento náutico no início do ano, reagindo sempre com atraso às flutuações bruscas de demanda.