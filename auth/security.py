import streamlit as st
import time

MAX_ATTEMPTS = 5
LOCKOUT_SECONDS = 300


def check_rate_limit(username: str) -> bool:
    key = f"rl_{username}"
    now = time.time()

    if key not in st.session_state:
        st.session_state[key] = {"attempts": 0, "locked_until": 0}

    record = st.session_state[key]

    if now < record["locked_until"]:
        remaining = int(record["locked_until"] - now)
        st.error(f"Conta bloqueada. Tente novamente em {remaining}s.")
        return False

    return True


def register_failed_attempt(username: str):
    key = f"rl_{username}"
    record = st.session_state.get(key, {"attempts": 0, "locked_until": 0})
    record["attempts"] += 1

    if record["attempts"] >= MAX_ATTEMPTS:
        record["locked_until"] = time.time() + LOCKOUT_SECONDS
        record["attempts"] = 0
        st.warning("Muitas tentativas. Conta bloqueada por 5 minutos.")

    st.session_state[key] = record


def reset_attempts(username: str):
    st.session_state.pop(f"rl_{username}", None)