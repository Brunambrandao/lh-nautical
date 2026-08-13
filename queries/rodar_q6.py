"""
Script de Execução - Questão 6: Previsão de Demanda (Bússola de Bordo 702)
Modelo Baseline: Média Móvel dos Últimos 3 Meses
Validação Q6.2: Soma Total das Previsões no 1º Trimestre de 2026
"""

import pandas as pd
import sqlite3

DB_FILE = "lh_nautical_bruto.db"


def executar_q6():
  conn = sqlite3.connect(DB_FILE)

  # 1. Agrupamento mensal de vendas da 'Bússola de Bordo 702'
  sql_vendas = """
    SELECT 
        STRFTIME('%Y-%m', o.created_at) AS mes_ano,
        SUM(oi.quantity) AS quantidade_real
    FROM order_items oi
    JOIN orders o ON oi.order_id = o.id
    JOIN product_variants pv ON oi.product_variant_id = pv.id
    JOIN products p ON pv.product_id = p.id
    WHERE LOWER(p.name) LIKE '%bússola de bordo 702%'
       OR LOWER(p.name) LIKE '%bussola de bordo 702%'
    GROUP BY STRFTIME('%Y-%m', o.created_at)
    ORDER BY mes_ano ASC;
    """

  df = pd.read_sql_query(sql_vendas, conn)
  conn.close()

  df['quantidade_real'] = df['quantidade_real'].astype(float)

  # 2. Modelo Baseline: Média Móvel de 3 meses (shift=1)
  df['previsao_baseline'] = (
      df['quantidade_real'].shift(1).rolling(window=3).mean()
  )

  # 3. Período de Teste: 1º Trimestre de 2026
  df_teste = df[df['mes_ano'].isin(['2026-01', '2026-02', '2026-03'])].copy()

  # 4. Cálculos da Questão 6.1 (MAE) e Questão 6.2 (Soma Total de Previsão)
  df_teste['erro_absoluto'] = (
      df_teste['quantidade_real'] - df_teste['previsao_baseline']
  ).abs()
  mae = df_teste['erro_absoluto'].mean()

  soma_previsoes = df_teste['previsao_baseline'].sum()
  soma_arredondada = round(soma_previsoes)

  print("=" * 70)
  print(" DESEMPENHO NO 1º TRIMESTRE DE 2026 (PERÍODO DE TESTE)")
  print("=" * 70)
  print(df_teste.to_string(index=False))

  print("\n" + "-" * 70)
  print(f" MAE (Mean Absolute Error): {mae:.2f} unidades")
  print("-" * 70)
  print(f" Soma Exata das Previsões (Q1/2026): {soma_previsoes:.6f}")
  print(
      f" VALIDAÇÃO (Q6.2) - Soma Arredondada (Inteiro): {soma_arredondada} unidades"
  )
  print("-" * 70)


if __name__ == "__main__":
  executar_q6()