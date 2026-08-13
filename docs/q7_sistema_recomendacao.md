# Questão 7 — Sistema de Recomendação por Similaridade de Cosseno

## 📌 Objetivo
Desenvolvimento de um motor de recomendação item-item (*Item-Based Collaborative Filtering*) baseado na similaridade do comportamento de compra dos clientes, tomando como referência o produto **"Motor de Popa 1949"** (ID: 180).

---

## 📊 Matriz Usuário × Produto e Métrica
* **Linhas:** `customer_id`
* **Colunas:** `product_id`
* **Valores:** Binário (`1` se comprou o produto ao menos uma vez, `0` caso contrário).
* **Métrica:** Similaridade de Cosseno (*Cosine Similarity*).

---

## 🏆 Top 5 Produtos Mais Similares

| Ranking | Product ID | Nome do Produto | Similaridade de Cosseno |
| :---: | :---: | :--- | :---: |
| **1º** | **389** | Motor de Popa 5331 | **0.256553** |
| **2º** | **295** | Cabo Náutico 2105 | **0.256239** |
| **3º** | **75** | Vela Mestra 1913 | **0.255785** |
| **4º** | **337** | Cabo Náutico 9048 | **0.239332** |
| **5º** | **55** | GPS Plotter 6249 | **0.237744** |

---

## 🛠️ Comandos de Execução
Para reproduzir a matriz e o ranking no ambiente local:

```powershell
python queries/rodar_q7.py