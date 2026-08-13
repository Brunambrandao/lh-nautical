# Questão 6 — Previsão de Demanda (Bússola de Bordo 702)

## 📌 Contexto e Objetivo
Desenvolvimento de modelo preditivo *baseline* (Média Móvel de 3 meses) para projetar as vendas mensais do produto **"Bússola de Bordo 702"** no 1º Trimestre de 2026.

---

## 📊 Resultados do Período de Teste (1º Trimestre / 2026)

| Mês / Ano | Vendas Reais (`quantidade_real`) | Previsão Baseline (`previsao_baseline`) | Erro Absoluto |
| :---: | :---: | :---: | :---: |
| **2026-01** | **152.0** | **80.333333** | **71.666667** |
| **2026-02** | **98.0** | **110.666667** | **12.666667** |
| **2026-03** | **105.0** | **101.666667** | **3.333333** |

---

## 🎯 Validação de Resultados

### Questão 6.1 — Erro Médio Absoluto (MAE)
* **MAE:** `29.22` unidades

### Questão 6.2 — Soma Total da Previsão de Vendas (Q1 / 2026)
* **Soma Exata das Previsões:** `80.333333 + 110.666667 + 101.666667 = 292.666667`
* **Valor Arredondado (Resposta da Validação):** **`293`** unidades

---

## 💡 Avaliação do Modelo Baseline

### a. O baseline é adequado para esse produto?
**Não.** O modelo apresentou um erro médio de **29.22 unidades**, sendo crítico no mês de pico de vendas (**Janeiro/2026**). Em Janeiro, a demanda real foi de **152 unidades**, mas a previsão baseline indicou apenas **80.33 unidades** (uma subestimativa severa de **71.67 unidades**), o que geraria uma grave ruptura de estoque no auge do verão.

### b. Limitação Técnica do Método
**Incapacidade de capturar Sazonalidade (Atraso Temporal / Lag Effect):** A média móvel é um método exclusivamente reativo e suavizado. Por olhar apenas para os 3 meses imediatamente anteriores (Outubro, Novembro e Dezembro), ela ignora os picos sazonais característicos do segmento náutico no início do ano, reagindo sempre com atraso às flutuações bruscas de demanda.

---

## 🧠 Questão 6.3 — Explicação Técnica

### 1. Construção do Baseline
Modelo de **Média Móvel Simples de 3 Meses** aplicado à série temporal mensal. A previsão para o mês $t$ é dada por:

$$\hat{Y}_t = \frac{Y_{t-1} + Y_{t-2} + Y_{t-3}}{3}$$

### 2. Prevenção de Data Leakage
Garantido mediante aplicação de `.shift(1)` na série temporal antes da janela móvel `.rolling(window=3)`. Desta forma, a previsão do mês $t$ nunca consome dados do próprio mês $t$ ou posteriores.

### 3. Limitação do Modelo
**Reatividade e Atraso Temporal (*Lag Effect*):** Por não incorporar componentes sazonais nem variáveis externas (ex: temperatura, promoções), o modelo reage com atraso aos picos de demanda típicos de início de ano no setor náutico.