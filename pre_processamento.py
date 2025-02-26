import pandas as pd

# --- 1. CARREGAR DADOS ---

clientes_df = pd.read_csv("clientes.csv")
produtos_df = pd.read_csv("produtos.csv")
vendas_df = pd.read_csv("vendas.csv")

# --- 2. LIMPEZA DOS DADOS ---

# Remover caracteres inválidos dos nomes dos clientes
clientes_df["nome"] = clientes_df["nome"].str.replace(r"[^a-zA-Z ]", "", regex=True)

# Corrigir idades inválidas (ex: 157 anos)
clientes_df["idade"] = clientes_df["idade"].apply(lambda x: None if pd.isna(x) or x > 100 else x)

# Preencher idades ausentes com a média arredondada
clientes_df["idade"].fillna(round(clientes_df["idade"].mean()), inplace=True)

# Discretizar idades em 3 faixas etárias
bins = [0, 25, 50, 100]
labels = ["Jovem", "Adulto", "Idoso"]
clientes_df["faixa_etaria"] = pd.cut(clientes_df["idade"], bins=bins, labels=labels, right=False)

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

# Ordenar colunas para melhor organização
colunas_ordenadas = ["codigovenda", "data", "hora", "cliente", "nome_cliente", "idade_cliente", "faixa_etaria_cliente", 
                     "produto", "nome_produto", "secao_produto", "qtde", "preco", "total"]
vendas_final = vendas_final[colunas_ordenadas]

# --- 4. EXPORTAÇÃO DO CSV FINAL ---
vendas_final.to_csv("dados_processados.csv", index=False, sep=";", encoding="utf-8-sig")
print("Arquivo 'dados_processados.csv' salvo com sucesso com formatação corrigida!")

