import streamlit as st
import pandas as pd
from sqlalchemy import create_engine




@st.cache_data
def load_data():

    url = st.secrets["DATABASE_URL"]
    engine = create_engine(url)
    avaliacoes         = pd.read_sql("SELECT * FROM avaliacoes", engine)
    vendedoras         = pd.read_sql("SELECT * FROM vendedoras", engine)
    lojas              = pd.read_sql("SELECT * FROM lojas", engine)
    supervisores       = pd.read_sql("SELECT * FROM supervisores", engine)
    supervisores_lojas = pd.read_sql("SELECT * FROM supervisores_lojas", engine)
    engine.dispose()
    return avaliacoes, vendedoras, lojas, supervisores, supervisores_lojas