import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


# Título
st.title("📊 Dashboard de Despesas dos Deputados (2022–2025)")

# Carregar dados
@st.cache_data
def carregar_dados():
    df23 = pd.read_csv('despesas_deputados_2023.csv', encoding='utf-8-sig')
    df24 = pd.read_csv('despesas_deputados_2024.csv', encoding='utf-8-sig')
    df25 = pd.read_csv('despesas_deputados_2025.csv', encoding='utf-8-sig')
    df = pd.concat([df23, df24, df25], ignore_index=True)
    df['data'] = pd.to_datetime(df['data'])
    df['ano'] = df['data'].dt.year
    return df

df = carregar_dados()

# Filtro por ano
anos = sorted(df['ano'].unique())
ano_selecionado = st.selectbox("Selecione o ano", anos)

df_filtrado = df[df['ano'] == ano_selecionado]

# CARTÕES COM KPIs principais
total_despesas = df_filtrado['valor'].sum()
total_deputados = df_filtrado['nomeDeputado'].nunique()
total_documentos = df_filtrado['numeroDoc'].nunique()

valor_formatado = locale.currency(total_despesas, grouping=True)
st.metric("💰 Total de Despesas", valor_formatado)
st.metric("🧑‍⚖️ Deputados Ativos", total_deputados)
st.metric("📄 Documentos Registrados", total_documentos)

#GRÁFICO DOS 10 DEPUTADOS
st.subheader("🔝 Top 10 Deputados por Despesa")

top_deputados = df_filtrado.groupby('nomeDeputado')['valor'].sum().nlargest(10)
top_deputados = top_deputados.sort_values(ascending=False).reset_index()

fig = px.bar(
    top_deputados,
    x='nomeDeputado',
    y='valor',
    title='Top 10 Deputados por Despesa',
    labels={'valor': 'Valor (R$)', 'nomeDeputado': 'Deputado'},
)

fig.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig, use_container_width=True)

top_despesas = df_filtrado.groupby('tipo_despesa')['valor'].sum().sort_values(ascending=False).head(10).reset_index()

top_despesas['valor_formatado'] = top_despesas['valor'].map(lambda x: f"R$ {x:,.0f}".replace(",", "v").replace(".", ",").replace("v", "."))

#FUNIL
fig = px.funnel(
    top_despesas,
    y='tipo_despesa',
    x='valor',
    text='valor_formatado',
    title='🔻 Despesas por Tipo (Gráfico de Funil)',
    labels={'valor': 'Valor (R$)', 'tipo_despesa': 'Tipo de Despesa'}
)

fig.update_traces(
    texttemplate='<b>%{text}</b>',
    textposition="outside",
    textfont_size=12
)


st.plotly_chart(fig, use_container_width=True)


#GRAFICO DE ACOMPANHAMENTO MENSAL

df_filtrado['mes_ano'] = pd.to_datetime(df_filtrado['data']).dt.to_period('M').dt.to_timestamp()
df_filtrado['mes_nome'] = df_filtrado['mes_ano'].dt.strftime('%b/%Y')  # Exemplo: Jan/2023

mensal = df_filtrado.groupby(['mes_ano', 'mes_nome'])['valor'].sum().reset_index()

fig = px.area(
    mensal,
    x='mes_nome',
    y='valor',
    title='📅 Evolução Mensal das Despesas',
    labels={'valor': 'Valor (R$)', 'mes_nome': 'Mês'},
    markers=True,
)


fig.update_traces(hovertemplate='Mês: %{x}<br>Valor: R$ %{y:,.0f}<extra></extra>')
fig.update_layout(
    xaxis_tickangle=-45,
    yaxis_tickformat=',.0f',
)

st.plotly_chart(fig, use_container_width=True)
