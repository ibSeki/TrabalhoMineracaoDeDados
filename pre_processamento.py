import pandas as pd
import numpy as np

# --- 1. CARREGAR DADOS ---
clientes_df = pd.read_csv("clientes.csv", sep=",", encoding="utf-8-sig")
produtos_df = pd.read_csv("produtos.csv", sep=",", encoding="utf-8-sig")
vendas_df = pd.read_csv("vendas.csv", sep=",", encoding="utf-8-sig")

# --- 2. LIMPEZA DOS DADOS ---

# Remover caracteres inválidos dos nomes dos clientes e padronizar formato
clientes_df["nome"] = clientes_df["nome"].str.replace(r"[^a-zA-Z ]", "", regex=True).str.title()

# Corrigir idades inválidas (ex: 157 anos)
clientes_df["idade"] = clientes_df["idade"].apply(lambda x: np.nan if pd.isna(x) or x > 100 or x < 0 else x)

# Discretizar idades em 3 faixas etárias
bins = [0, 25, 50, 100]
labels = ["Jovem", "Adulto", "Idoso"]
clientes_df["faixa_etaria"] = pd.cut(clientes_df["idade"], bins=bins, labels=labels, right=False)

# Padronizar nomes dos produtos
produtos_df["nome"] = produtos_df["nome"].str.title()

# --- 3. INTEGRAÇÃO DOS DADOS ---

# Juntar informações dos clientes na base de vendas
vendas_com_clientes = vendas_df.merge(clientes_df, left_on="cliente", right_on="codigo", how="left").drop(columns=["codigo", "endereco"])

# Juntar informações dos produtos na base de vendas
vendas_final = vendas_com_clientes.merge(produtos_df, left_on="produto", right_on="codigo", how="left").drop(columns=["codigo"])

# Renomear colunas para melhor compreensão
vendas_final.rename(columns={
    "nome_x": "nome_cliente",
    "idade": "idade_cliente",
    "faixa_etaria": "faixa_etaria_cliente",
    "nome_y": "nome_produto",
    "secao": "secao_produto"
}, inplace=True)

# Converter a coluna de data para o formato datetime
vendas_final["data"] = pd.to_datetime(vendas_final["data"], format="%d/%m/%Y", errors="coerce")

# Ordenar colunas para melhor organização
colunas_ordenadas = ["codigovenda", "data", "hora", "cliente", "nome_cliente", "idade_cliente", "faixa_etaria_cliente", 
                     "produto", "nome_produto", "secao_produto", "qtde", "preco", "total"]
vendas_final = vendas_final[colunas_ordenadas]

# Remover linhas com informações ausentes do cliente
vendas_final.dropna(subset=["nome_cliente", "idade_cliente", "faixa_etaria_cliente"], inplace=True)

# --- 4. EXPORTAÇÃO DO CSV FINAL ---
vendas_final.to_csv("dados_processados.csv", index=False, sep=";", encoding="utf-8-sig")
print("Arquivo 'dados_processados.csv' salvo com sucesso com formatação corrigida!")