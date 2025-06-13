import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Configurações iniciais
st.set_page_config(page_title="Dashboard de Colaboradores", layout="wide")

# Carregar dados
tabela = pd.read_excel('BaseColaboradores11.xlsx', engine='openpyxl')

# Título
st.title("📊 Dashboard de Colaboradores")
st.markdown("Este painel permite analisar os salários totais por cargo de forma interativa.")

# SIDEBAR - Filtros
st.sidebar.header("🔍 Filtros")

# Filtro múltiplo por cargos
todos_cargos = sorted(tabela['Cargo'].unique())
cargos_selecionados = st.sidebar.multiselect("Selecione os cargos:", todos_cargos, default=todos_cargos)

# Filtro por faixa salarial
min_sal, max_sal = float(tabela['Salario Total'].min()), float(tabela['Salario Total'].max())
faixa_salarial = st.sidebar.slider("Faixa salarial:", min_sal, max_sal, (min_sal, max_sal))

# Filtro aplicado ao DataFrame
dados_filtrados = tabela[
    (tabela['Cargo'].isin(cargos_selecionados)) &
    (tabela['Salario Total'] >= faixa_salarial[0]) &
    (tabela['Salario Total'] <= faixa_salarial[1])
]

# LAYOUT DE COLUNAS
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📈 Gráfico de Salário por Cargo")
    if dados_filtrados.empty:
        st.warning("Nenhum dado encontrado com os filtros selecionados.")
    else:
        fig = px.bar(dados_filtrados, x='Cargo', y='Salario Total',
                     color='Cargo', hover_data=['Salario Total'],
                     title="Salário Total por Cargo", labels={'Salario Total': 'Salário (R$)'})
        st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("📋 Dados Filtrados")
    st.dataframe(dados_filtrados[['Cargo', 'Salario Total']])

# Checkbox para exibir toda a base de dados
if st.checkbox("📂 Exibir dados completos"):
    st.subheader("Base de dados completa")
    st.dataframe(tabela)

# Footer
st.markdown("---")
st.markdown("Desenvolvido com ❤️ usando Streamlit")