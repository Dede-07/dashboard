import streamlit as st
import pandas as pd
import plotly.express as px

# Carregar dados
df = pd.read_excel("bancoGAMES.xlsx")

st.set_page_config(page_title="Dashboard Estatística 🎮", page_icon="📊", layout="wide")

st.title("Dashboard Estatístico - Consoles de Videogame 🎮")

# Seletor de coluna quantitativa
coluna_selecionada = st.selectbox("**Escolha uma Coluna Quantitativa**:", ['UNIDADES VENDIDAS', 'PREÇO INICIAL', 'FATURAMENTO'])

# Estatísticas básicas
media = df[coluna_selecionada].mean()
mediana = df[coluna_selecionada].median()
moda = df[coluna_selecionada].mode()[0]

# Formatando valores monetários para 'PREÇO INICIAL' e 'FATURAMENTO'
if coluna_selecionada in ['PREÇO INICIAL', 'FATURAMENTO']:
    media = f'$ {media:,.2f}'
    mediana = f'$ {mediana:,.2f}'
    moda = f'$ {moda:,.2f}'
else:
    media = f'{media:,.0f}'
    mediana = f'{mediana:,.0f}'
    moda = f'{moda:,.0f}'

# Criar um container para os cartões
with st.container():
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 📌 Média")
        st.markdown(f"<h2 style='text-align: center; color: #4CAF50;'>{media}</h2>", unsafe_allow_html=True)

    with col2:
        st.markdown("### 🎯 Mediana")
        st.markdown(f"<h2 style='text-align: center; color: #2196F3;'>{mediana}</h2>", unsafe_allow_html=True)

    with col3:
        st.markdown("### 📊 Moda")
        st.markdown(f"<h2 style='text-align: center; color: #FF9800;'>{moda}</h2>", unsafe_allow_html=True)

# Linha de gráficos
col4, col5 = st.columns(2)

# Gráfico de barras - Top 10 consoles mais vendidos (em ordem decrescente)
with col4:
    df_sorted_consoles = df.sort_values(by='UNIDADES VENDIDAS', ascending=False).head(10)
    fig1 = px.bar(df_sorted_consoles, x='UNIDADES VENDIDAS', y='CONSOLE', orientation='h', 
                  title="Top 10 Consoles Mais Vendidos", text_auto='.2s')
    fig1.update_yaxes(categoryorder='total ascending')  # Organiza em ordem decrescente
    st.plotly_chart(fig1, use_container_width=True)

# Gráfico de faturamento por empresa
with col5:
    df_grouped = df.groupby('EMPRESA')['FATURAMENTO'].sum().reset_index().sort_values(by='FATURAMENTO', ascending=False)
    df_grouped['FATURAMENTO_FORMATADO'] = df_grouped['FATURAMENTO'].apply(lambda x: f'{x/1e9:.2f}B' if x >= 1e9 else f'{x/1e6:.2f}M')
    fig2 = px.bar(df_grouped, x='EMPRESA', y='FATURAMENTO', title="Faturamento por Empresa (em $)", text=df_grouped['FATURAMENTO_FORMATADO'])
    st.plotly_chart(fig2, use_container_width=True)

# Segunda linha de gráficos
col6, col7 = st.columns(2)

with col6:
    df_preco_medio = df.groupby('EMPRESA')['PREÇO INICIAL'].mean().reset_index().sort_values('PREÇO INICIAL', ascending=False)
    fig3 = px.bar(df_preco_medio, x='EMPRESA', y='PREÇO INICIAL', title="Preço Inicial Médio por Empresa (em $)", text_auto='.2s')
    st.plotly_chart(fig3, use_container_width=True)

with col7:
    fig4 = px.histogram(df, x='TIPO', title="Distribuição de Tipos de Consoles")
    st.plotly_chart(fig4, use_container_width=True)

# Terceira linha de gráficos
col8, col9 = st.columns(2)

with col8:
    df_grouped_tipo_empresa = df.groupby(['EMPRESA', 'TIPO'])['UNIDADES VENDIDAS'].sum().reset_index()
    df_grouped_tipo_empresa = df_grouped_tipo_empresa.sort_values('UNIDADES VENDIDAS', ascending=False)
    fig5 = px.bar(df_grouped_tipo_empresa, x='EMPRESA', y='UNIDADES VENDIDAS', color='TIPO',
                  title="Unidades Vendidas por Tipo de Console e Empresa", text_auto='.2s')
    st.plotly_chart(fig5, use_container_width=True)

with col9:
    df_grouped_tipo_faturamento = df.groupby('TIPO')['FATURAMENTO'].sum().reset_index()
    df_grouped_tipo_faturamento = df_grouped_tipo_faturamento.sort_values('FATURAMENTO', ascending=False)
    df_grouped_tipo_faturamento['FATURAMENTO'] = df_grouped_tipo_faturamento['FATURAMENTO'] / 1e9
    fig6 = px.bar(df_grouped_tipo_faturamento, x='TIPO', y='FATURAMENTO', 
                  title="Faturamento por Tipo de Console", text_auto='.2s')
    fig6.update_layout(yaxis_title="Faturamento (Bilhões)")
    st.plotly_chart(fig6, use_container_width=True)

st.markdown("[Clique aqui para abrir o banco de dados](https://docs.google.com/spreadsheets/d/1dMITLQojncXc6F8RNfCfSRDvKznxNpdl/edit?usp=sharing&ouid=101200214570574763659&rtpof=true&sd=true)")
st.write("🎮 **Feito por:** André, Arthur e Lucas")
