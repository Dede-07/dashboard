import streamlit as st
import pandas as pd
import plotly.express as px

# Carregar dados
df = pd.read_excel("bancoGAMES.xlsx")

st.set_page_config(page_title="Dashboard Estatística 🎮", page_icon = "📊", layout="wide")

# Função para mostrar o dashboard
def show_dashboard():
    st.title("Dashboard de Consoles de Videogame 🎮")
    
    # Criar duas colunas para exibir os gráficos de forma mais organizada
    col1, col2 = st.columns(2)

    # Gráfico 1: Unidades vendidas por console (na primeira coluna)
    with col1:
        df_sorted_consoles = df.sort_values(by='UNIDADES VENDIDAS', ascending=False)
        top_10_consoles = df_sorted_consoles.head(10)
        fig1 = px.bar(top_10_consoles, x='UNIDADES VENDIDAS', y='CONSOLE', orientation='h', 
                      title="Top 10 Consoles Mais Vendidos")
        fig1.update_yaxes(categoryorder='total ascending')  
        st.plotly_chart(fig1, use_container_width=True)

    # Gráfico 2: Faturamento por Empresa (na segunda coluna)
    with col2:
        df_grouped = df.groupby('EMPRESA')['FATURAMENTO'].sum().reset_index()
        df_sorted = df_grouped.sort_values(by='FATURAMENTO', ascending=False)
        df_sorted['FATURAMENTO_FORMATADO'] = df_sorted['FATURAMENTO'].apply(lambda x: f'{x/1e9:.2f}B' if x >= 1e9 else f'{x/1e6:.2f}M')
        
        fig2 = px.bar(df_sorted, x='EMPRESA', y='FATURAMENTO', title="Faturamento por Empresa (em $)", text=df_sorted['FATURAMENTO_FORMATADO'])
        st.plotly_chart(fig2, use_container_width=True)

    # Segunda linha com gráficos lado a lado
    col3, col4 = st.columns(2)

    # Gráfico 3: Unidades vendidas ao longo dos anos (na primeira coluna)
    with col3:
        df_preco_medio = df.groupby('EMPRESA')['PREÇO INICIAL'].mean().reset_index()
        df_preco_medio = df_preco_medio.sort_values('PREÇO INICIAL', ascending=False)
        fig3 = px.bar(df_preco_medio, x='EMPRESA', y='PREÇO INICIAL', title="Preço Inicial Médio por Empresa (em $)", text_auto='.2s')
        st.plotly_chart(fig3, use_container_width=True)

    # Gráfico 4: Distribuição dos Tipos de Console (na segunda coluna)
    with col4:
        fig4 = px.histogram(df, x='TIPO', title="Quantidade de Vendas por Tipos de Consoles")
        st.plotly_chart(fig4, use_container_width=True)

    # Gráficos na linha inferior
    col5, col6 = st.columns(2)

    # Gráfico 5: Preço inicial médio por empresa (na primeira coluna)
    with col5:
        df_grouped_tipo_empresa = df.groupby(['EMPRESA', 'TIPO'])['UNIDADES VENDIDAS'].sum().reset_index()
        df_grouped_tipo_empresa = df_grouped_tipo_empresa.sort_values('UNIDADES VENDIDAS', ascending=False)
        fig5 = px.bar(df_grouped_tipo_empresa, x='EMPRESA', y='UNIDADES VENDIDAS', color='TIPO',
                      title="Unidades Vendidas por Tipo de Console e Empresa", text_auto='.2s')
        st.plotly_chart(fig5, use_container_width=True)

    # Gráfico 6: Ano de lançamento vs. descontinuação (na segunda coluna)
    with col6:
        df_grouped_tipo_faturamento = df.groupby('TIPO')['FATURAMENTO'].sum().reset_index()
        df_grouped_tipo_faturamento = df_grouped_tipo_faturamento.sort_values('FATURAMENTO', ascending=False)
        df_grouped_tipo_faturamento['FATURAMENTO'] = df_grouped_tipo_faturamento['FATURAMENTO'] / 1e9
        fig6 = px.bar(df_grouped_tipo_faturamento, x='TIPO', y='FATURAMENTO', 
                      title="Faturamento por Tipo de Console", text_auto='.2s')
        fig6.update_layout(yaxis_title="Faturamento (Bilhões)")
        st.plotly_chart(fig6, use_container_width=True)

    # Fonte do Dashboard
    st.write("Feito por: André, Arthur e Lucas 🎮")

# Função para mostrar o banco de dados
def show_database():
    st.title("Banco de Dados de Consoles 📊")
    st.write("Aqui estão os dados do Excel carregados:")

    # Exibindo o DataFrame
    st.dataframe(df)

    st.markdown("➡️ [Visualizar o arquivo no excel]( https://docs.google.com/spreadsheets/d/1dMITLQojncXc6F8RNfCfSRDvKznxNpdl/edit?usp=sharing&ouid=101200214570574763659&rtpof=true&sd=true)")

def show_sobreAula():
    st.title("Dados Quantitativos para contas 📈")
    st.write("Aqui estão os dados quantitativos onde foram feitos esses cálculos:")

    # Selecionando as colunas quantitativas
    df_quantitativo = df[['UNIDADES VENDIDAS', 'PREÇO INICIAL', 'FATURAMENTO']]
    st.dataframe(df_quantitativo)

    st.subheader("Média, Mediana, Moda, Desvio Padrão e Coeficiente de Variação por Coluna:")

    for coluna in df_quantitativo.columns:
        st.write(f"Coluna - **{coluna}:**")
        
        # Média
        media = df_quantitativo[coluna].mean()
        st.write(f"Média: {media:,.2f}")
        
        # Mediana
        mediana = df_quantitativo[coluna].median()
        st.write(f"Mediana: {mediana:,.2f}")
        
        # Moda
        moda = df_quantitativo[coluna].mode()[0]
        st.write(f"Moda: {moda:,.2f}")
        
        # Desvio Padrão
        desvio_padrao = df_quantitativo[coluna].std()
        st.write(f"Desvio Padrão: {desvio_padrao:,.2f}")

        # Coeficiente de Variação (Desvio Padrão / Média)
        coef_variacao = (desvio_padrao / media) * 100
        st.write(f"Coeficiente de Variação: {coef_variacao:,.2f} %")

        st.write("---") 


# Menu de navegação
menu = st.sidebar.selectbox("Escolha a página", ("Dashboard 📶", "Sobre as aulas ✍🏼","Banco de Dados 📈"))

# Navegação entre as páginas
if menu == "Dashboard 📶":
    show_dashboard()
elif menu == "Banco de Dados 📈":
    show_database()
elif menu == "Sobre as aulas ✍🏼":
    show_sobreAula()
