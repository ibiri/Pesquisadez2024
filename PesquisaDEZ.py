import streamlit as st
import pandas as pd
import sys

# Carregar os dados
dados = "https://github.com/ibiri/Pesquisadez2024/raw/main/Banco%20Amazonas%20dezembro%202024.xlsx"
data = pd.read_excel(dados)

# Criar painel lateral para seleção de município
st.sidebar.title("Filtros")

# Remover valores 0 e NaN da lista de municípios
municipios_validos = data["Municipio2"].dropna().astype(str)
municipios_validos = municipios_validos[municipios_validos != "0"].unique()

# Adicionar a opção "Todos" no filtro
municipios = ["Todos"] + sorted(municipios_validos)
municipio_selecionado = st.sidebar.selectbox("Selecione o Município", municipios)

# Filtrar os dados pelo município selecionado (se "Todos", não filtra)
if municipio_selecionado == "Todos":
    data_filtrada = data
else:
    data_filtrada = data[data["Municipio2"].astype(str) == municipio_selecionado]

# --- Interface Principal ---
st.title("Pesquisa Amazonas - Dezembro 2024")
st.divider()

# --- Tabela 1: Estim1 ---
st.subheader("Resultados de Estimativa")

percent_series = data_filtrada['Estim1'].value_counts(normalize=True) * 100
percent_series = percent_series.map(lambda x: f"{x:.2f}%")

nome_mapping = {
    "david_almeida": "David Almeida",
    "NS_NR": "NS/NR",
    "omar_aziz": "Omar Aziz",
    "candidato_bolsonaro": "Candidato do Bolsonaro",
    "BrancoNulo": "Branco/Nulo"
}

percent_series.index = percent_series.index.map(lambda x: nome_mapping.get(x, x))
percent_table = percent_series.reset_index()
percent_table.columns = ['Candidato', 'Percentual']

# Exibir tabela sem índice
st.table(percent_table.style.hide(axis="index"))

# --- Tabela 2: Rejeição ---
st.subheader("Rejeição dos Candidatos")

percent_series_rejeicao = data_filtrada['Rejeicao'].value_counts(normalize=True) * 100
percent_series_rejeicao = percent_series_rejeicao.map(lambda x: f"{x:.2f}%")

nome_mapping_rejeicao = {
    "david_almeida": "David Almeida",
    "candidato_bolsonaro": "Candidato do Bolsonaro",
    "Naorejeitanenhum": "Não rejeita nenhum",
    "NS_NR": "NS/NR",
    "omar_aziz": "Omar Aziz",
    "option_6": "Tadeu de Souza"
}

percent_series_rejeicao.index = percent_series_rejeicao.index.map(lambda x: nome_mapping_rejeicao.get(x, x))
percent_table_rejeicao = percent_series_rejeicao.reset_index()
percent_table_rejeicao.columns = ['Candidato', 'Percentual']

# Exibir tabela sem índice
st.table(percent_table_rejeicao.style.hide(axis="index"))
