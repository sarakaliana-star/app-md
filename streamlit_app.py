import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------------------------------------
# 🎨 Configurações gerais
# -----------------------------------------------------------
st.set_page_config(page_title="Rendimento Escolar - EFAs e Escolas Rurais", layout="wide")

# -----------------------------------------------------------
# 🧭 Título e introdução
# -----------------------------------------------------------
st.title("📊 Escolas do MEPES e Escolas Rurais - Censo Escolar 2024")

st.markdown("""
### 🎯 Objetivo

Este aplicativo tem como objetivo **comparar as taxas de rendimento escolar (aprovação, reprovação e abandono)** entre escolas do campo e escolas privadas, 
com base nos dados do **Censo Escolar 2024**.  

A iniciativa busca **destacar o papel das Escolas Famílias Agrícolas (EFAs)** e da **pedagogia da alternância** na promoção da permanência escolar, 
considerando suas especificidades pedagógicas e territoriais.
""")

# -----------------------------------------------------------
# 📂 Carregar planilha
# -----------------------------------------------------------
df = pd.read_excel("tx_rend_escolas_2024.xlsx")

# -----------------------------------------------------------
# 🔧 Selecionar e renomear colunas
# -----------------------------------------------------------
df = df[['Nome do Município', 'Nome da Escola', 'Dependência Administrativa',
         'Taxa de Aprovação', 'Taxa de Reprovação', 'Taxa de Abandono']]

df = df.rename(columns={
    'Nome do Município': 'Município',
    'Dependência Administrativa': 'Localização'
})

df['Localização'] = df['Localização'].astype(str).str.strip().str.capitalize()

# -----------------------------------------------------------
# 🧹 Limpeza e conversão
# -----------------------------------------------------------
df['Taxa de Aprovação'] = pd.to_numeric(df['Taxa de Aprovação'], errors='coerce')
df['Taxa de Reprovação'] = pd.to_numeric(df['Taxa de Reprovação'], errors='coerce')
df['Taxa de Abandono'] = pd.to_numeric(df['Taxa de Abandono'], errors='coerce')

tipos_validos = ['Estadual', 'Privada']
df = df[df['Localização'].isin(tipos_validos)]

# -----------------------------------------------------------
# 🎛️ Barra lateral de filtros
# -----------------------------------------------------------
st.sidebar.header("🔎 Filtros")

# Filtro por município
municipios = sorted(df['Município'].dropna().unique())
municipio_selecionado = st.sidebar.multiselect(
    "Selecione o(s) município(s):", 
    municipios, 
    default=municipios
)

# Filtro por tipo de escola
locais = df['Localização'].unique()
localizacao_selecionada = st.sidebar.multiselect(
    "Selecione o tipo de escola:", 
    locais, 
    default=locais
)

# Filtro por intervalo de taxa de aprovação
min_aprov, max_aprov = float(df['Taxa de Aprovação'].min()), float(df['Taxa de Aprovação'].max())
intervalo_aprovacao = st.sidebar.slider(
    "Intervalo da Taxa de Aprovação (%)", 
    min_aprov, max_aprov, 
    (min_aprov, max_aprov)
)

# Aplicar filtros
df_filtrado = df[
    (df['Município'].isin(municipio_selecionado)) &
    (df['Localização'].isin(localizacao_selecionada)) &
    (df['Taxa de Aprovação'].between(intervalo_aprovacao[0], intervalo_aprovacao[1]))
]

# -----------------------------------------------------------
# 📊 Comparação da Taxa de Aprovação
# -----------------------------------------------------------
st.subheader("📊 Comparação da Taxa de Aprovação: Estadual x Privada")

taxa_aprovacao = df_filtrado.groupby('Localização')['Taxa de Aprovação'].mean().reset_index()

fig, ax = plt.subplots()
ax.bar(taxa_aprovacao['Localização'], taxa_aprovacao['Taxa de Aprovação'], color='royalblue')
for i, v in enumerate(taxa_aprovacao['Taxa de Aprovação']):
    ax.text(i, v + 0.5, f"{v:.1f}%", ha='center', fontsize=11, fontweight='bold')
ax.set_ylabel("Taxa de Aprovação (%)")
ax.set_ylim(0, 110)
st.pyplot(fig)

# Texto explicativo
if not taxa_aprovacao.empty and all(taxa_aprovacao['Localização'].isin(['Estadual', 'Privada'])):
    taxa_estadual = taxa_aprovacao.loc[taxa_aprovacao['Localização'] == 'Estadual', 'Taxa de Aprovação'].values[0]
    taxa_privada = taxa_aprovacao.loc[taxa_aprovacao['Localização'] == 'Privada', 'Taxa de Aprovação'].values[0]
    st.markdown(f"""
    ### 📈 Resultados - Taxa de Aprovação

    As análises mostram que a **taxa média de aprovação** das escolas estaduais é de **{taxa_estadual:.1f}%**, 
    enquanto nas escolas privadas é de **{taxa_privada:.1f}%**.  

    Essa proximidade reforça o potencial das escolas públicas estaduais — especialmente das **EFAs**, 
    que, mesmo em contextos rurais e com menos recursos, mantêm níveis de aprovação semelhantes aos da rede privada.
    """)

# -----------------------------------------------------------
# 📉 Comparação da Taxa de Abandono
# -----------------------------------------------------------
st.subheader("📉 Comparação da Taxa de Abandono: Estadual x Privada")

taxa_abandono = df_filtrado.groupby('Localização')['Taxa de Abandono'].mean().reset_index()

fig2, ax2 = plt.subplots()
ax2.bar(taxa_abandono['Localização'], taxa_abandono['Taxa de Abandono'], color='tomato')
for i, v in enumerate(taxa_abandono['Taxa de Abandono']):
    ax2.text(i, v + 0.2, f"{v:.1f}%", ha='center', fontsize=11, fontweight='bold')
ax2.set_ylabel("Taxa de Abandono (%)")
ax2.set_ylim(0, 10)
st.pyplot(fig2)

# Texto explicativo
if not taxa_abandono.empty and all(taxa_abandono['Localização'].isin(['Estadual', 'Privada'])):
    abandono_estadual = taxa_abandono.loc[taxa_abandono['Localização'] == 'Estadual', 'Taxa de Abandono'].values[0]
    abandono_privada = taxa_abandono.loc[taxa_abandono['Localização'] == 'Privada', 'Taxa de Abandono'].values[0]
    st.markdown(f"""
    ### 🧭 Resultados - Taxa de Abandono

    A **taxa média de abandono** nas escolas estaduais é de **{abandono_estadual:.1f}%**, 
    enquanto nas privadas é de **{abandono_privada:.1f}%**.  

    Mesmo com desafios estruturais, as escolas públicas vêm apresentando bons indicadores, 
    o que destaca o papel das **políticas de permanência escolar** e o diferencial da **pedagogia da alternância** nas **EFAs**.
    """)

# -----------------------------------------------------------
# 🌱 Conclusão
# -----------------------------------------------------------
st.markdown("""
### 🌱 Considerações Finais

As **Escolas Famílias Agrícolas (EFAs)**, com a **pedagogia da alternância**, 
têm papel essencial na **redução da evasão** e na **manutenção dos estudantes** em contextos rurais.  
Ao integrar o **tempo-escola** e o **tempo-comunidade**, essas instituições fortalecem o vínculo dos jovens com o campo, 
valorizando os saberes locais e promovendo uma **educação contextualizada, crítica e transformadora**.
""")

# -----------------------------------------------------------
# 📋 Tabelas Detalhadas
# -----------------------------------------------------------
st.subheader("🗂️ Escolas com Municípios e Taxas Filtradas")
st.dataframe(df_filtrado[['Município', 'Nome da Escola', 'Localização',
                          'Taxa de Aprovação', 'Taxa de Reprovação', 'Taxa de Abandono']])
