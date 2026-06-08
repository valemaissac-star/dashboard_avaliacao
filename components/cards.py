import streamlit as st


def metric_principal(label, valor):
    st.markdown(f"""
        <div class='metric-principal'>
            <div class='metric-principal-label'>{label}</div>
            <div class='metric-principal-value'>{valor}</div>
        </div>
    """, unsafe_allow_html=True)



def mes_card(mes, total, media_estrelas, bem_atendimento):
   st.markdown(f"""
                <div class='mes-card'>
                    <div style='color:#ffe66d; font-size:1.1rem; font-weight:900;'>{mes}</div>
                    <div style='color:#ffffff; font-size:1.8rem; font-weight:900;'>{total}):,</div>
                    <div style='color:#e0e0ff; font-size:0.9rem;'>Avaliações</div>
                    <hr style='border-color:#4444aa; margin:8px 0;'>
                    <div style='color:#e0e0ff; font-size:0.85rem;'>🌟 {media_estrelas:.2f} &nbsp;|&nbsp; 😁 {bem_atendimento:.1f}%</div>
                </div>
            """, unsafe_allow_html=True)