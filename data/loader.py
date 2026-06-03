import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
# ======================================================
# CARREGAMENTO DOS DADOS
# ======================================================

@st.cache_data

def get_engine() :
    url = st.secrets["DATABASE_URL"]
    return create_engine(url)
def load_data():
    paths = [
        ('arquivos_30_04_26/', 'Pasta arquivos'),
        ('arquivos/', 'Pasta arquivos'),
        ('', 'Raiz do repositório'),
    ]
    for path_prefix, _ in paths:
        try:
            avaliacoes = pd.read_excel(f'{path_prefix}avaliacoes.xlsx')
            vendedoras = pd.read_excel(f'{path_prefix}vendedoras.xlsx')
            lojas = pd.read_excel(f'{path_prefix}lojas.xlsx')
            supervisores = pd.read_excel(f'{path_prefix}supervisores.xlsx')
            supervisores_lojas = pd.read_excel(f'{path_prefix}supervisores_lojas.xlsx')
            return avaliacoes, vendedoras, lojas, supervisores, supervisores_lojas
        except Exception:
            continue
    raise FileNotFoundError("❌ Arquivos Excel não encontrados!")
try:
    avaliacoes, vendedoras, lojas, supervisores, supervisores_lojas = load_data()
except FileNotFoundError as e:
    st.error(str(e))
    st.stop()
