import streamlit as st
import pandas as pd
from services.metrics import calcular_metricas, ranking_vendedoras_df, ranking_lojas_df
from config.theme import cores_vibrantes, template
from components.ranking import secao_ranking_completa
import plotly.graph_objects as go

def render(dados):
    avaliacoes         = dados['avaliacoes']
    vendedoras         = dados['vendedoras']
    lojas              = dados['lojas']
    aval_vend_completa = dados['aval_vend_completa']
    meses_disponiveis  = dados['meses_disponiveis']
    aval_supervisores  = dados['aval_supervisores']

    template_df       = template()
    cores_vibrante_df = cores_vibrantes()

    st.markdown("### ⏰ Análise Detalhada por Mês")

    if not meses_disponiveis:
        st.warning("Nenhum mês identificado nos dados.")
        st.stop()

    mes_sel = st.selectbox(
        "Selecione o mês para análise:",
        options=meses_disponiveis,
        index=len(meses_disponiveis) - 1,
        key="sel_mes_principal"
    )

    aval_mes      = avaliacoes[avaliacoes['mes_ano_str'] == mes_sel].copy()
    aval_vend_mes = aval_vend_completa[aval_vend_completa['mes_ano_str'] == mes_sel].copy()
    aval_sup_mes  = aval_supervisores[aval_supervisores['mes_ano_str'] == mes_sel].copy()

    if len(aval_mes) == 0:
        st.warning(f"Nenhuma avaliação encontrada em {mes_sel}")
        st.stop()

    total_m, media_est_m, media_rec_m, bem_pct_m = calcular_metricas(aval_mes)

    st.markdown(f"#### 🗓️ Métricas de {mes_sel}")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""<div class='metric-principal'>
            <div class='metric-principal-label'>Total de Avaliações</div>
            <div class='metric-principal-value'>{total_m:,}</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class='metric-principal'>
            <div class='metric-principal-label'>Média de Estrelas</div>
            <div class='metric-principal-value'>{media_est_m:.2f}/5</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class='metric-principal'>
            <div class='metric-principal-label'>Taxa de Bem Atendimento</div>
            <div class='metric-principal-value'>{bem_pct_m:.1f}%</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col4, col5 = st.columns(2)
    col4.metric("👍 Média de Recomendação", f"{media_rec_m:.2f}/10")

    idx_mes = meses_disponiveis.index(mes_sel)
    if idx_mes > 0:
        mes_ant   = meses_disponiveis[idx_mes - 1]
        aval_ant  = avaliacoes[avaliacoes['mes_ano_str'] == mes_ant]
        delta_tot = total_m - len(aval_ant)
        col5.metric("📊 Variação vs Mês Anterior", f"{total_m:,} avaliações", delta=f"{delta_tot:+,} avaliações")

    st.markdown("---")

    col_p1, col_p2 = st.columns(2)
    with col_p1:
        dist_est = aval_mes['estrela_1_5'].value_counts().sort_index()
        fig_p1 = go.Figure(data=[go.Pie(
            labels=[f"{int(i)} estrela(s)" for i in dist_est.index],
            values=dist_est.values,
            hole=0.4,
            marker=dict(colors=cores_vibrante_df, line=dict(color='#0f0c29', width=3)),  
            textfont=dict(size=16),
        )])
        fig_p1.update_layout(template_df, title=f"⭐ Estrelas — {mes_sel}", height=400)  
        st.plotly_chart(fig_p1, width='stretch', key=f"pizza_est_{mes_sel}")

    with col_p2:
        dist_atend = aval_mes['bem_atendimento'].value_counts()
        fig_p2 = go.Figure(data=[go.Pie(
            labels=dist_atend.index,
            values=dist_atend.values,
            hole=0.4,
            marker=dict(colors=["#10B981", "#F97316", "#F43F5E"], line=dict(color="#0f0c29", width=3)),
            textfont=dict(size=16),
        )])
        fig_p2.update_layout(template_df, title=f"😊 Bem Atendimento — {mes_sel}", height=400) 
        st.plotly_chart(fig_p2, width='stretch', key=f"pizza_atend_{mes_sel}")

    st.markdown("---")

    secao_ranking_completa(dados, aval_mes, aval_vend_mes, aval_sup_mes, sufixo=mes_sel.replace("-", "_"))

    st.markdown("---")

    st.markdown("### 🚨 Vendedoras Sem Avaliação neste Mês")
    ids_aval_mes = aval_vend_mes['vendedora_id'].dropna().unique() if 'vendedora_id' in aval_vend_mes.columns else []
    vend_sem_mes = vendedoras[~vendedoras['id'].isin(ids_aval_mes)].copy()
    vend_sem_mes = vend_sem_mes.merge(lojas[['id', 'loja']], left_on='loja_id', right_on='id', how='left')
    if len(vend_sem_mes) > 0:
        tab_sem         = vend_sem_mes[['vendedora', 'loja']].copy()
        tab_sem.columns = ['Vendedora', 'Loja']
        st.error(f"⚠️ {len(tab_sem)} vendedoras sem avaliação em {mes_sel}")
        st.dataframe(tab_sem.sort_values(['Loja', 'Vendedora']),width='stretch', hide_index=True)
    else:
        st.success(f"✅ Todas as vendedoras têm avaliação em {mes_sel}!")

    st.markdown("---")

    st.markdown("### 💾 Exportar Dados do Mês")
    rv_mes = ranking_vendedoras_df(aval_vend_mes)
    rl_mes = ranking_lojas_df(aval_mes, lojas)

    c1, c2, c3 = st.columns(3)
    with c1:
        if len(rv_mes) > 0:
            st.download_button(f"📥 Vendedoras {mes_sel}", rv_mes.to_csv(index=False, encoding='utf-8-sig'),
                               f"vendedoras_{mes_sel}.csv", "text/csv")
    with c2:
        if len(rl_mes) > 0:
            st.download_button(f"📥 Lojas {mes_sel}", rl_mes.to_csv(index=False, encoding='utf-8-sig'),
                               f"lojas_{mes_sel}.csv", "text/csv")
    with c3:
        st.download_button(f"📥 Avaliações {mes_sel}", aval_mes.to_csv(index=False, encoding='utf-8-sig'),
                           f"avaliacoes_{mes_sel}.csv", "text/csv")

    st.markdown("---")
    st.markdown(
        "<p style='text-align:center;color:#6666aa;font-size:0.95rem;'>Dashboard de Avaliações · Atualize a página para recarregar</p>",
        unsafe_allow_html=True
    )