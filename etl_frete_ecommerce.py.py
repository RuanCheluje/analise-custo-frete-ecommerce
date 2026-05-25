# =========================
# IMPORTAÇÕES
# =========================
import pandas as pd
import os
import numpy as np
from datetime import datetime


# =====================================================
#  FUNÇÃO DE CONVERSÃO INTELIGENTE
# =====================================================

def converter_valor(valor):
    valor = str(valor).strip()

    if valor == "" or valor.lower() == "nan":
        return np.nan

    if "," in valor:
        valor = valor.replace(".", "").replace(",", ".")
    return pd.to_numeric(valor, errors="coerce")


# =====================================================
#  PASSO 1 — EXTRAÇÃO (BASE DE FRETES)
# =====================================================

caminho_pasta = r"./data/fretes"

arquivos = [f for f in os.listdir(caminho_pasta) if f.endswith(('.xlsx', '.xls', '.xlsm'))]

lista_dfs_total = []

for arquivo in arquivos:
    caminho_arquivo = os.path.join(caminho_pasta, arquivo)
    
    try:
        df = pd.read_excel(caminho_arquivo, sheet_name="BASE NOVO", dtype=str)
        
        df['ARQUIVO_ORIGEM'] = arquivo
        
        colunas_valor = ['VALOR CT-E', 'VALOR ICMS']
        
        for col in colunas_valor:
            if col in df.columns:
                df[col] = df[col].apply(converter_valor)
        
        lista_dfs_total.append(df)
    
    except Exception as e:
        print(f"Erro no arquivo {arquivo}: {e}")

df_total = pd.concat(lista_dfs_total, ignore_index=True)

df_total.columns = (
    df_total.columns
    .str.strip()
    .str.upper()
    .str.replace(r"[^\w]", "_", regex=True)
)

print("Dimensão df_total:", df_total.shape)


# =====================================================
#  PASSO 2 — EXTRAÇÃO NOTAS
# =====================================================

caminho_notas = r"./data/notas"

lista_dfs_notas = []

for arquivo in os.listdir(caminho_notas):
    if arquivo.endswith(".xlsx"):
        caminho_arquivo = os.path.join(caminho_notas, arquivo)
        
        try:
            df = pd.read_excel(
                caminho_arquivo,
                sheet_name="Notas fiscais",
                engine="openpyxl"
            )
            
            df["ARQUIVO_ORIGEM"] = arquivo
            
            colunas_valores = ["Total", "vICMS", "Valor mercadoria"]
            
            for col in colunas_valores:
                if col in df.columns:
                    df[col] = df[col].apply(converter_valor)
            
            lista_dfs_notas.append(df)

        except Exception as e:
            print(f"Erro ao processar {arquivo}: {e}")

df_notas_total = pd.concat(lista_dfs_notas, ignore_index=True)

df_notas_total.columns = (
    df_notas_total.columns
    .str.strip()
    .str.upper()
    .str.replace(r"[^\w]", "_", regex=True)
)

print("Dimensão df_notas_total:", df_notas_total.shape)


# =====================================================
#  PASSO 3 — ETL VALOR_NF
# =====================================================

df_total["NUM_NFE"] = pd.to_numeric(df_total["NUM_NFE"], errors="coerce").astype("Int64")
df_notas_total["NFE"] = pd.to_numeric(df_notas_total["NFE"], errors="coerce").astype("Int64")

mapa_valores = dict(
    zip(
        df_notas_total["NFE"],
        df_notas_total["VALOR_MERCADORIA"]
    )
)

df_total["VALOR_NF"] = 0.0

mask = df_total["TIPO_DE_ENTREGA"] == "ENTREGA_NORMAL"

df_total.loc[mask, "VALOR_NF"] = (
    df_total.loc[mask, "NUM_NFE"]
    .map(mapa_valores)
)

df_total["VALOR_NF"] = df_total["VALOR_NF"].fillna(0)


# =====================================================
#  PASSO 4 — ETL CUSTO_FRETE
# =====================================================

df_total["VALOR_CT_E"] = pd.to_numeric(df_total["VALOR_CT_E"], errors="coerce")

if "SITUAÇÃO_CT_E" in df_total.columns:
    df_total.rename(columns={"SITUAÇÃO_CT_E": "SITUACAO_CT_E"}, inplace=True)

df_filtrado = df_total[df_total["SITUACAO_CT_E"] == "ENTRADA_REALIZADA"]

mapa_custo_frete = (
    df_filtrado
    .groupby("CHAVE_DE_ACESSO_NFE")["VALOR_CT_E"]
    .sum()
)

df_total["CUSTO_FRETE"] = 0.0

mask = df_total["TIPO_DE_ENTREGA"] == "ENTREGA_NORMAL"

df_total.loc[mask, "CUSTO_FRETE"] = (
    df_total.loc[mask, "CHAVE_DE_ACESSO_NFE"]
    .map(mapa_custo_frete)
)

df_total["CUSTO_FRETE"] = df_total["CUSTO_FRETE"].fillna(0)

col_valor_nf_index = df_total.columns.get_loc("VALOR_NF")

coluna = df_total.pop("CUSTO_FRETE")
df_total.insert(col_valor_nf_index + 1, "CUSTO_FRETE", coluna)


# =====================================================
#  PASSO 5 — PERC_FRETE
# =====================================================

df_total["PERC_FRETE"] = np.nan

mask = (
    (df_total["VALOR_NF"] > 0) &
    (df_total["TIPO_DE_ENTREGA"] == "ENTREGA_NORMAL") &
    (df_total["SITUACAO_CT_E"] == "ENTRADA_REALIZADA")
)

df_total.loc[mask, "PERC_FRETE"] = (
    df_total.loc[mask, "CUSTO_FRETE"] /
    df_total.loc[mask, "VALOR_NF"]
)

df_total["PERC_FRETE"] = df_total["PERC_FRETE"].round(4)


# =====================================================
#  PASSO 6 — CLASSIFICAÇÃO
# =====================================================

df_total["CLASSIFICACAO_FRETE"] = pd.Series(dtype="string")

df_total.loc[df_total["PERC_FRETE"] <= 0.04, "CLASSIFICACAO_FRETE"] = "BAIXO"

df_total.loc[
    (df_total["PERC_FRETE"] > 0.04) &
    (df_total["PERC_FRETE"] <= 0.05),
    "CLASSIFICACAO_FRETE"
] = "OK"

df_total.loc[df_total["PERC_FRETE"] > 0.05, "CLASSIFICACAO_FRETE"] = "ALTO"


# =====================================================
#  PASSO 7 — EXPORTAÇÃO PARQUET
# =====================================================

df_final_total = df_total

df_final_total["CLASSIFICACAO_FRETE"] = df_final_total["CLASSIFICACAO_FRETE"].astype("string")

data_hoje = datetime.now().strftime("%Y%m%d")

caminho_saida = f"./output/df_final_total_{data_hoje}.parquet"

os.makedirs("./output", exist_ok=True)

df_final_total.to_parquet(
    caminho_saida,
    index=False,
    engine="pyarrow"
)

print(f"\n✅ Arquivo exportado com sucesso em:\n{caminho_saida}")