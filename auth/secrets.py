import streamlit as st


def load_auth_config() -> dict:
    return {
        "credentials": {
            "usernames": {
                user: dict(data)
                for user, data in st.secrets["credentials"]["usernames"].items()
            }
        },
        "cookie": {
            "name": st.secrets["cookie"]["name"],
            "key": st.secrets["cookie"]["key"],
            "expiry_days": int(st.secrets["cookie"]["expiry_days"]),
        },
    }