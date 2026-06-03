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
@st.cache_data
def load_data():
    engine = get_engine()
    avaliacoes        = pd.read_sql("SELECT * FROM avaliacoes", engine)
    vendedoras        = pd.read_sql("SELECT * FROM vendedoras", engine)
    lojas             = pd.read_sql("SELECT * FROM lojas", engine)
    supervisores      = pd.read_sql("SELECT * FROM supervisores", engine)
    supervisores_lojas = pd.read_sql("SELECT * FROM supervisores_lojas", engine)
    return avaliacoes, vendedoras, lojas, supervisores, supervisores_lojas