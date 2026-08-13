"""
Script de Execução - Questão 7: Sistema de Recomendação por Similaridade de Cosseno
Item de Referência: Motor de Popa 1949
"""

import numpy as np
import pandas as pd
import sqlite3
from sklearn.metrics.pairwise import cosine_similarity

DB_FILE = "lh_nautical_bruto.db"


def executar_q7():
  conn = sqlite3.connect(DB_FILE)

  # 1. Extração das interações únicas entre Cliente e Produto
  query = """
    SELECT DISTINCT
        o.customer_id,
        p.id AS product_id,
        p.name AS product_name
    FROM order_items oi
    JOIN orders o ON oi.order_id = o.id
    JOIN product_variants pv ON oi.product_variant_id = pv.id
    JOIN products p ON pv.product_id = p.id
    """

  df_interacoes = pd.read_sql_query(query, conn)
  conn.close()

  # Dicionário de apoio: Mapear ID para Nome do Produto
  mapa_produtos = (
      df_interacoes[['product_id', 'product_name']]
      .drop_duplicates()
      .set_index('product_id')['product_name']
      .to_dict()
  )

  # 2. Construção da Matriz Usuário x Produto (Presença = 1, Ausência = 0)
  matriz_usuario_item = pd.crosstab(
      df_interacoes['customer_id'], df_interacoes['product_id']
  )
  # Usando map em vez de applymap para compatibilidade com Pandas 2.1+
  matriz_usuario_item = matriz_usuario_item.map(lambda x: 1 if x > 0 else 0)

  # 3. Transposição para Matriz Produto x Usuário e cálculo da Similaridade de Cosseno
  matriz_produto_cliente = matriz_usuario_item.T
  sim_matrix = cosine_similarity(matriz_produto_cliente)

  # Converter em DataFrame rotulado por Product ID
  df_sim = pd.DataFrame(
      sim_matrix,
      index=matriz_produto_cliente.index,
      columns=matriz_produto_cliente.index,
  )

  # 4. Localizar o ID do produto "Motor de Popa 1949"
  prod_ref_id = None
  for pid, pname in mapa_produtos.items():
    if 'motor de popa 1949' in pname.lower():
      prod_ref_id = pid
      prod_ref_nome = pname
      break

  if prod_ref_id is None:
    print("ALERTA: Produto 'Motor de Popa 1949' não foi localizado na base.")
    return

  print(
      f"🔍 Produto de Referência Encontrado: {prod_ref_nome} (ID:"
      f" {prod_ref_id})\n"
  )

  # 5. Gerar Ranking dos 5 produtos mais similares (excluindo o próprio item)
  similares = df_sim[prod_ref_id].drop(index=prod_ref_id)
  top_5 = similares.sort_values(ascending=False).head(5)

  df_ranking = pd.DataFrame({
      'product_id': top_5.index,
      'product_name': [mapa_produtos[pid] for pid in top_5.index],
      'similaridade_cosseno': top_5.values,
  })

  print("=" * 80)
  print(" TOP 5 PRODUTOS MAIS SIMILARES AO 'MOTOR DE POPA 1949'")
  print("=" * 80)
  print(df_ranking.to_string(index=False))
  print("=" * 80)


if __name__ == '__main__':
  executar_q7()