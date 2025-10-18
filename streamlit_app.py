import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ---------------------------
# Título
# ---------------------------
st.title("📊 Escolas do MEPES e Escolas Rurais - Censo Escolar 2024")

# ---------------------------
# Texto de Objetivo
# ---------------------------
st.markdown("""
### 🎯 Objetivo

Este aplicativo tem como objetivo **comparar as taxas de rendimento escolar (aprovação, reprovação e abandono)** entre escolas do campo e escolas privadas, com base nos dados do **Censo Escolar 2024**.  

A iniciativa busca **destacar o papel das Escolas Famílias Agrícolas (EFAs)** e da **pedagogia da alternância** na promoção da permanência escolar, considerando suas especificidades pedagógicas e territoriais.
""")

# ---------------------------
# Carregar planilha
# ---------------------------
df = pd.read_excel("tx_rend_escolas_2024.xlsx")

# ---------------------------
# Selecionar apenas colunas importantes
# ---------------------------
df = df[['Nome do Município', 'Nome da Escola', 'Dependência Administrativa', 
         'Taxa de Aprovação', 'Taxa de Reprovação', 'Taxa de Abandono']]

# Renomear colunas para ficar mais amigável
df = df.rename(columns={
    'Nome do Município': 'Município',
    'Dependência Administrativa': 'Localização'
})

# ---------------------------
# Limpeza e conversão de dados
# ---------------------------
df['Localização'] = df['Localização'].astype(str).str.strip().str.capitalize()
df['Taxa de Aprovação'] = pd.to_numeric(df['Taxa de Aprovação'], errors='coerce')
df['Taxa de Reprovação'] = pd.to_numeric(df['Taxa de Reprovação'], errors='coerce')
df['Taxa de Abandono'] = pd.to_numeric(df['Taxa de Abandono'], errors='coerce')

# ---------------------------
# Comparação da taxa de aprovação: Estadual x Privada
# ---------------------------
st.subheader("📊 Comparação da Taxa de Aprovação: Estadual x Privada")

tipos_validos = ['Estadual', 'Privada']
df_comparacao = df[df['Localização'].isin(tipos_validos)]
taxa_media = df_comparacao.groupby('Localização')['Taxa de Aprovação'].mean().reset_index()

st.bar_chart(taxa_media.set_index('Localização'))

# ---------------------------
# Texto de Resultados automáticos
# ---------------------------
if not taxa_media.empty and all(taxa_media['Localização'].isin(['Estadual', 'Privada'])):
    taxa_estadual = taxa_media.loc[taxa_media['Localização'] == 'Estadual', 'Taxa de Aprovação'].values[0]
    taxa_privada = taxa_media.loc[taxa_media['Localização'] == 'Privada', 'Taxa de Aprovação'].values[0]

    st.markdown(f"""
    ### 📈 Resultados

    As análises indicam que a **taxa média de aprovação** das escolas estaduais é de aproximadamente **{taxa_estadual:.1f}%**, enquanto nas escolas privadas é de **{taxa_privada:.1f}%**.  

    Esses resultados evidenciam um desempenho semelhante entre os dois grupos, mas reforçam a importância de compreender as **especificidades das escolas do campo**, especialmente das **Escolas Famílias Agrícolas (EFAs)**, que atuam com a **pedagogia da alternância**.  
    Essa metodologia contribui significativamente para a **permanência escolar**, ao articular o tempo-escola e o tempo-comunidade, valorizando os saberes locais e fortalecendo o vínculo dos jovens com o território.
    """)

# ---------------------------
# Tabela detalhada: Município + Escola + taxas
# ---------------------------
st.subheader("🗂️ Escolas com Municípios e Taxas")
df_tabela = df[['Município', 'Nome da Escola', 'Localização',
                'Taxa de Aprovação', 'Taxa de Reprovação', 'Taxa de Abandono']]
st.dataframe(df_tabela)

# ---------------------------
# Tabela adicional: Taxa de Aprovação por Escola
# ---------------------------
st.subheader("📈 Taxa de Aprovação por Escola")
st.dataframe(df[['Município', 'Nome da Escola', 'Localização', 'Taxa de Aprovação']])
