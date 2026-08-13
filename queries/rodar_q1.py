import pandas as pd

# 1. Carrega a tabela orders do CSV sem fazer nenhum tratamento
df_orders = pd.read_csv("lh_nautical_csv/orders.csv")

# Converter a coluna de data para datetime para extrair min e max corretamente
df_orders["created_at"] = pd.to_datetime(df_orders["created_at"])

# 2. Executa as agregações solicitadas na Questão 1
total_linhas = len(df_orders)
data_minima = df_orders["created_at"].min()
data_maxima = df_orders["created_at"].max()

valor_minimo = df_orders["total"].min()
valor_maximo = df_orders["total"].max()
valor_medio = df_orders["total"].mean()

# 3. Exibe os resultados organizados no terminal
print("=" * 40)
print("RESULTADOS DA QUESTÃO 1 - EDA ORDERS")
print("=" * 40)
print(f"Total de linhas: {total_linhas}")
print(f"Data mínima: {data_minima}")
print(f"Data máxima: {data_maxima}")
print(f"Valor mínimo (total): {valor_minimo}")
print(f"Valor máximo (total): {valor_maximo}")
print(f"Valor médio (total): {valor_medio:.2f}")
print("=" * 40)