import streamlit as st
import time

SESSION_TIMEOUT = 3600


def init_session():
    if "last_activity" not in st.session_state:
        st.session_state["last_activity"] = time.time()


def check_session_timeout() -> bool:
    if not st.session_state.get("authentication_status"):
        return True

    elapsed = time.time() - st.session_state.get("last_activity", 0)
    if elapsed > SESSION_TIMEOUT:
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.warning("Sessão expirada por inatividade. Faça login novamente.")
        st.rerun()
        return False

    st.session_state["last_activity"] = time.time()
    return True


def force_logout():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()