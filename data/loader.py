import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    paths = [
        'arquivos_30_04_26/',
        'arquivos/',
        '',
    ]
    for prefix in paths:
        try:
            avaliacoes         = pd.read_excel(f'{prefix}avaliacoes.xlsx')
            vendedoras         = pd.read_excel(f'{prefix}vendedoras.xlsx')
            lojas              = pd.read_excel(f'{prefix}lojas.xlsx')
            supervisores       = pd.read_excel(f'{prefix}supervisores.xlsx')
            supervisores_lojas = pd.read_excel(f'{prefix}supervisores_lojas.xlsx')
            return avaliacoes, vendedoras, lojas, supervisores, supervisores_lojas
        except Exception:
            continue
    raise FileNotFoundError("❌ Arquivos Excel não encontrados!")