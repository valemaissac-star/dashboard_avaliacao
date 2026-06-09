import streamlit as st
from data.processor import get_dataframes
from views import visao_geral, evolucao_mensal, analise_por_mes
from config.theme import style

st.set_page_config(
    page_title="Dashboard Avaliações",
    page_icon="📊",
    layout="wide"
)


dados = get_dataframes()

aba_geral, aba_mensal, aba_analise = st.tabs([
    "📈 Visão Geral",
    "📅 Evolução Mensal",
    "⏰ Análise por Mês"
])

with aba_geral:
    visao_geral.render(dados)

with aba_mensal:
    evolucao_mensal.render(dados)

with aba_analise:
    analise_por_mes.render(dados)