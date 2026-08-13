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

---

## 🔍 Validação da Questão 7.2 

### 🏆 Resultado
O produto com **MAIOR similaridade de cosseno** ao item de referência **"Motor de Popa 1949"** (Product ID: `180`) é o **"Motor de Popa 5331"** (Product ID: `389`), apresentando um índice de similaridade de **`0.256553`** (~25,66%).

---

### 🧠 Passo a Passo Metodológico

1. **Vetorização das Compras (Matriz Binária):**
   * Cada produto foi transformado em um vetor $V_p$ de dimensão $N$ (onde $N$ é o total de clientes).
   * Onde $V_{p,c} = 1$ indica que o cliente $c$ adquiriu o produto $p$, e $0$ caso contrário.

2. **Cálculo da Similaridade de Cosseno:**
   * Aplicou-se o cálculo do cosseno entre os vetores de cada par de produtos:
     $$\text{Similaridade}(A, B) = \frac{A \cdot B}{\Vert{}A\Vert{} \Vert{}B\Vert{}}$$
   * Essa métrica mede o ângulo entre os vetores de compra, identificando produtos que tendem a co-ocorrer nos históricos dos mesmos clientes, independentemente do volume total absoluto.

3. **Filtragem e Ordenação:**
   * Isolou-se o vetor do produto `ID 180` (*Motor de Popa 1949*).
   * Excluiu-se o próprio item do vetor resultado (cuja similaridade é $1.0$).
   * Ordenaram-se os demais $N-1$ produtos em ordem decrescente de pontuação.

---

### 💻 Evidência de Execução Local (Terminal)

Saída gerada pelo script `queries/rodar_q7.py`:

```text
🔍 Produto de Referência Encontrado: Motor de Popa 1949 (ID: 180)

================================================================================
 TOP 5 PRODUTOS MAIS SIMILARES AO 'MOTOR DE POPA 1949'
================================================================================
product_id       product_name  similaridade_cosseno
       389  Motor de Popa 5331              0.256553
       295   Cabo Náutico 2105              0.256239
        75    Vela Mestra 1913              0.255785
       337   Cabo Náutico 9048              0.239332
        55    GPS Plotter 6249              0.237744
================================================================================