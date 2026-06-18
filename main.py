import streamlit as st
import streamlit_authenticator as stauth

from auth.secrets import load_auth_config
from auth.security import check_rate_limit, register_failed_attempt, reset_attempts
from auth.session import init_session, check_session_timeout, force_logout


from data.processor import get_dataframes
from views import visao_geral, evolucao_mensal, analise_por_mes
from config.theme import style,inject_login_css

st.set_page_config(
    page_title="Dashboard Avaliações",
    page_icon="📊",
    layout="wide"
)

init_session()
config = load_auth_config()

authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
)

status = st.session_state.get("authentication_status")

if status is not True:
  
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        authenticator.login()

status   = st.session_state.get("authentication_status")
username = st.session_state.get("username", "")

if status is False:
    if username and not check_rate_limit(username):
        st.stop()
    register_failed_attempt(username or "unknown")
    st.error("Usuário ou senha incorretos.")
    st.stop()

elif status is None:
    st.info("Faça login para continuar.")
    st.stop()


reset_attempts(username)
check_session_timeout()

style() 

with st.sidebar:
    st.write(f"Olá, **{st.session_state['name']}**")
    if st.button("Sair", type="secondary"):
        authenticator.logout()
        force_logout()

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