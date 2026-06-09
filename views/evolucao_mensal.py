from services.metrics import calcular_metricas
from config.theme import cores_vibrantes, template
from components.ranking import secao_ranking_completa
from services.metrics import ranking_vendedoras_df,ranking_lojas_df
import plotly.graph_objects as go
# ======================================================
# ABA 2 — EVOLUÇÃO MENSAL
# ======================================================
import streamlit as st



cores_vibrante_df = cores_vibrantes()

def render(dados):

    avaliacoes = dados['avaliacoes']
 
    template_df = template()

    st.markdown("## 📆 Evolução Mensal de Avaliações")

    evo = avaliacoes.groupby('mes_ano_str').agg(
        total=('estrela_1_5', 'count'),
        media_estrelas=('estrela_1_5', 'mean'),
        media_recomendacao=('recomendacao_1_10', 'mean'),
        bem_atendimento=('bem_atendimento', lambda x: (x == 'sim').sum() / len(x) * 100)
    ).reset_index().rename(columns={'mes_ano_str': 'Mês'})
    evo = evo.sort_values('Mês')

    st.markdown("### 📈 Resumo por Mês")
    num_meses = len(evo)
    cols_mes = st.columns(min(num_meses, 4))
    for i, (_, row) in enumerate(evo.iterrows()):
        col_idx = i % min(num_meses, 4)
        with cols_mes[col_idx]: 
            st.markdown(f"""
                <div class='mes-card'>
                    <div style='color:#ffe66d; font-size:1.1rem; font-weight:900;'>{row['Mês']}</div>
                    <div style='color:#ffffff; font-size:1.8rem; font-weight:900;'>{int(row['total']):,}</div>
                    <div style='color:#e0e0ff; font-size:0.9rem;'>Avaliações</div>
                    <hr style='border-color:#4444aa; margin:8px 0;'>
                    <div style='color:#e0e0ff; font-size:0.85rem;'>🌟 {row['media_estrelas']:.2f} &nbsp;|&nbsp; 😁 {row['bem_atendimento']:.1f}%</div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### 📊 Volume de Avaliações por Mês")
    fig_vol = go.Figure(data=[go.Bar(
        x=evo['Mês'],
        y=evo['total'],
        text=evo['total'].apply(lambda v: f"{int(v):,}"),
        textposition="outside",
        textfont=dict(size=16, color="#ffffff"),
        marker=dict(
            color=evo['total'],
            colorscale="Plasma",
            showscale=False,
            line=dict(color="rgba(225, 255, 255, 0.16)", width=1),
        ),
    )])
    fig_vol.update_layout(template_df, title="📊 Quantidade de Avaliações por Mês", height=500,
                          xaxis=dict(title="Mês", tickfont=dict(size=14)),
                          yaxis=dict(title="Quantidade", tickfont=dict(size=14)))
    st.plotly_chart(fig_vol, width='stretch', key="vol_mensal")

    st.markdown("---")

    col_g1, col_g2 = st.columns(2)
    with col_g1:
        fig_est = go.Figure()
        fig_est.add_trace(go.Scatter(
            x=evo['Mês'], y=evo['media_estrelas'],
            mode='lines+markers+text',
            text=evo['media_estrelas'].round(2),
            textposition='top center',
            textfont=dict(size=13, color="#ffe66d"),
            line=dict(color="#ffe66d", width=3),
            marker=dict(size=11, color="#ffe66d", line=dict(color="#ffffff", width=2)),
        ))
        fig_est.update_layout(template_df, title="⭐ Evolução da Média de Estrelas", height=400,
                              xaxis=dict(title="Mês"),
                              yaxis=dict(title="Média (1-5)", range=[1, 5.4]))
        st.plotly_chart(fig_est, width='stretch', key="evo_estrelas")

    with col_g2:
        fig_rec = go.Figure()
        fig_rec.add_trace(go.Scatter(
            x=evo['Mês'], y=evo['media_recomendacao'],
            mode='lines+markers+text',
            name='Média Recomendação',
            text=evo['media_recomendacao'].round(2),
            textposition='top center',
            textfont=dict(size=13, color="#4ecdc4"),
            line=dict(color="#4ecdc4", width=3),
            marker=dict(size=11, color="#4ecdc4", line=dict(color="#ffffff", width=2)),
        ))
        fig_rec.update_layout(template_df, title="👍 Evolução da Média de Recomendação", height=400,
                              xaxis=dict(title="Mês"),
                              yaxis=dict(title="Média (1-10)", range=[0, 11]))
        st.plotly_chart(fig_rec, width='stretch', key="evo_recomendacao")

    st.markdown("---")

    fig_bem = go.Figure()
    fig_bem.add_trace(go.Scatter(
        x=evo['Mês'], y=evo['bem_atendimento'],
        mode='lines+markers+text',
        name='% Bem Atendimento',
        text=evo['bem_atendimento'].round(1).apply(lambda v: f"{v}%"),
        textposition='top center',
        textfont=dict(size=13, color="#10b981"),
        line=dict(color="#10b981", width=3),
        marker=dict(size=11, color="#10b981", line=dict(color="#ffffff", width=2)),
        fill='tozeroy',
        fillcolor='rgba(16,185,129,0.12)',
    ))
    fig_bem.update_layout(template_df, title="😊 Evolução do % Bem Atendimento", height=390,
                          xaxis=dict(title="Mês"),
                          yaxis=dict(title="%", range=[0, 110]))
    st.plotly_chart(fig_bem, width='stretch', key="evo_bem_atend")

    st.markdown("---")

    st.markdown("### 📋 Tabela Resumo Mensal")
    evo_display = evo.copy().rename(columns={
        'total': 'Total Avaliações',
        'media_estrelas': 'Média Estrelas',
        'media_recomendacao': 'Média Recomendação',
        'bem_atendimento': '% Bem Atendimento'
    })
    st.dataframe(evo_display.round(2),width='stretch', hide_index=True)
