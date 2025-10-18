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
# Selecionar e renomear colunas
# ---------------------------
df = df[['Nome do Município', 'Nome da Escola', 'Dependência Administrativa', 
         'Taxa de Aprovação', 'Taxa de Reprovação', 'Taxa de Abandono']]

df = df.rename(columns={
    'Nome do Município': 'Município',
    'Dependência Administrativa': 'Localização'
})

# ---------------------------
# Limpeza e conversão
# ---------------------------
df['Localização'] = df['Localização'].astype(str).str.strip().str.capitalize()
df['Taxa de Aprovação'] = pd.to_numeric(df['Taxa de Aprovação'], errors='coerce')
df['Taxa de Reprovação'] = pd.to_numeric(df['Taxa de Reprovação'], errors='coerce')
df['Taxa de Abandono'] = pd.to_numeric(df['Taxa de Abandono'], errors='coerce')

tipos_validos = ['Estadual', 'Privada']
df_comparacao = df[df['Localização'].isin(tipos_validos)]

# ============================================================
# 📊 COMPARAÇÃO 1: TAXA DE APROVAÇÃO
# ============================================================
st.subheader("📊 Comparação da Taxa de Aprovação: Estadual x Privada")

taxa_aprovacao = df_comparacao.groupby('Localização')['Taxa de Aprovação'].mean().reset_index()

# Gráfico com valores sobre as barras
fig, ax = plt.subplots()
ax.bar(taxa_aprovacao['Localização'], taxa_aprovacao['Taxa de Aprovação'])
for i, v in enumerate(taxa_aprovacao['Taxa de Aprovação']):
    ax.text(i, v + 0.5, f"{v:.1f}%", ha='center', fontsize=11, fontweight='bold')
ax.set_ylabel("Taxa de Aprovação (%)")
ax.set_ylim(0, 110)
st.pyplot(fig)

# Texto automático - aprovação
if not taxa_aprovacao.empty and all(taxa_aprovacao['Localização'].isin(['Estadual', 'Privada'])):
    taxa_estadual = taxa_aprovacao.loc[taxa_aprovacao['Localização'] == 'Estadual', 'Taxa de Aprovação'].values[0]
    taxa_privada = taxa_aprovacao.loc[taxa_aprovacao['Localização'] == 'Privada', 'Taxa de Aprovação'].values[0]

    st.markdown(f"""
    ### 📈 Resultados - Taxa de Aprovação

    As análises indicam que a **taxa média de aprovação** das escolas estaduais é de aproximadamente **{taxa_estadual:.1f}%**, 
    enquanto nas escolas privadas é de **{taxa_privada:.1f}%**.  

    Esse resultado revela uma proximidade entre os dois grupos, sugerindo que, apesar das diferentes condições de funcionamento, 
    as escolas públicas estaduais vêm alcançando taxas de aprovação compatíveis com as privadas.
    """)

# ============================================================
# 📉 COMPARAÇÃO 2: TAXA DE ABANDONO
# ============================================================
st.subheader("📉 Comparação da Taxa de Abandono: Estadual x Privada")

taxa_abandono = df_comparacao.groupby('Localização')['Taxa de Abandono'].mean().reset_index()

# Gráfico com valores sobre as barras
fig2, ax2 = plt.subplots()
ax2.bar(taxa_abandono['Localização'], taxa_abandono['Taxa de Abandono'], color='tomato')
for i, v in enumerate(taxa_abandono['Taxa de Abandono']):
    ax2.text(i, v + 0.2, f"{v:.1f}%", ha='center', fontsize=11, fontweight='bold')
ax2.set_ylabel("Taxa de Abandono (%)")
ax2.set_ylim(0, 10)
st.pyplot(fig2)

# Texto automático - abandono
if not taxa_abandono.empty and all(taxa_abandono['Localização'].isin(['Estadual', 'Privada'])):
    abandono_estadual = taxa_abandono.loc[taxa_abandono['Localização'] == 'Estadual', 'Taxa de Abandono'].values[0]
    abandono_privada = taxa_abandono.loc[taxa_abandono['Localização'] == 'Privada', 'Taxa de Abandono'].values[0]

    st.markdown(f"""
    ### 🧭 Resultados - Taxa de Abandono

    Observa-se que a **taxa média de abandono** nas escolas estaduais é de **{abandono_estadual:.1f}%**, 
    enquanto nas escolas privadas é de **{abandono_privada:.1f}%**.  

    A diferença, embora possa variar conforme o território, destaca a importância de políticas voltadas à **permanência e ao acompanhamento escolar**, 
    especialmente no contexto das escolas do campo.
    """)

# ============================================================
# 🌱 CONCLUSÃO
# ============================================================
st.markdown("""
### 🌱 Considerações Finais

As **Escolas Famílias Agrícolas (EFAs)**, ao adotarem a **pedagogia da alternância**, têm papel essencial na redução da evasão e na 
manutenção dos estudantes em contextos rurais.  
Ao integrar o tempo-escola e o tempo-comunidade, essas instituições fortalecem o vínculo dos jovens com o campo, 
valorizando os saberes locais e promovendo uma **educação contextualizada, crítica e transformadora**.
""")

# ============================================================
# 🗂️ TABELAS DETALHADAS
# ============================================================
st.subheader("🗂️ Escolas com Municípios e Taxas")
df_tabela = df[['Município', 'Nome da Escola', 'Localização',
                'Taxa de Aprovação', 'Taxa de Reprovação', 'Taxa de Abandono']]
st.dataframe(df_tabela)

st.subheader("📈 Taxa de Aprovação por Escola")
st.dataframe(df[['Município', 'Nome da Escola', 'Localização', 'Taxa de Aprovação']])
