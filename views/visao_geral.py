import streamlit as st
from components.ranking import secao_ranking_completa
from services.metrics import calcular_metricas
from config.theme import cores_vibrantes, template
from components.ranking import secao_ranking_completa
from services.metrics import ranking_vendedoras_df,ranking_lojas_df
import plotly.graph_objects as go

template_df = template()
cores_vibrante_df = cores_vibrantes()


def render(dados):

    avaliacoes        = dados['avaliacoes']
    vendedoras        = dados['vendedoras']
    lojas             = dados['lojas']
    aval_vend_completa = dados['aval_vend_completa']
    aval_loja_completa = dados['aval_loja_completa']
    aval_supervisores  = dados['aval_supervisores']
    aval_vendedoras    = dados['aval_vendedoras'] 

    template_df = template()
    cores_vibrante_df = cores_vibrantes()
    st.markdown("### 📊 Visão Geral da Empresa — Todos os Períodos")

    total_aval, media_estrelas, media_recomendacao, bem_pct = calcular_metricas(avaliacoes)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""<div class='metric-principal'>
            <div class='metric-principal-label'>Total de Avaliações</div>
            <div class='metric-principal-value'>{total_aval:,}</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class='metric-principal'>
            <div class='metric-principal-label'>Média Estrelas</div>
            <div class='metric-principal-value'>{media_estrelas:.2f}/5.0</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class='metric-principal'>
            <div class='metric-principal-label'>Taxa de Bem Atendimento</div>
            <div class='metric-principal-value'>{bem_pct:.1f}%</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col4, col5, col6 = st.columns(3)
    col4.metric("👍 Média de Recomendação", f"{media_recomendacao:.2f}/10")
    col5.metric("👩‍💼 Total de Vendedoras", f"{len(vendedoras):,}")
    col6.metric("🏬 Total de Lojas", f"{len(lojas):,}")

    st.markdown("---")

    col_p1, col_p2 = st.columns(2)
    with col_p1:
        dist_est = avaliacoes['estrela_1_5'].value_counts().sort_index()
        fig = go.Figure(data=[go.Pie(
            labels=[f"{int(i)} estrela(s)" for i in dist_est.index],
            values=dist_est.values,
            hole=0.4,
            marker=dict(colors=cores_vibrante_df, line=dict(color="#0f0c29", width=3)),
            textfont=dict(size=16),
        )])
        fig.update_layout(template_df, title="⭐ Distribuição de Estrelas", height=420)
        st.plotly_chart(fig, width='stretch', key="pizza_estrelas_geral")

    with col_p2:
        dist_atend = avaliacoes['bem_atendimento'].value_counts()
        fig2 = go.Figure(data=[go.Pie(
            labels=dist_atend.index,
            values=dist_atend.values,
            hole=0.4,
            marker=dict(colors=["#10b981", "#f97316", "#f43f5e"], line=dict(color="#0f0c29")),
            textfont=dict(size=16)
        )])
        fig2.update_layout(template_df, title="😊 Bem Atendimento", height=420)
        st.plotly_chart(fig2, width='stretch', key="pizza_atend_geral")

    st.markdown("---")

    secao_ranking_completa(dados,avaliacoes, aval_vend_completa, aval_supervisores, sufixo="geral")

    st.markdown("---")

    st.markdown("### 🚨 Vendedoras Sem Avaliação")
    ids_avaliadas = aval_vendedoras['vendedora_id'].dropna().unique()
    vendedoras_sem = vendedoras[~vendedoras['id'].isin(ids_avaliadas)].copy()
    vendedoras_sem = vendedoras_sem.merge(lojas[['id', 'loja']], left_on='loja_id', right_on='id', how='left')
    if len(vendedoras_sem) > 0:
        tabela_sem = vendedoras_sem[['vendedora', 'loja']].copy()
        tabela_sem.columns = ['Vendedora', 'Loja']
        st.error(f"⚠️ {len(tabela_sem)} vendedoras estão sem avaliações")
        st.dataframe(tabela_sem.sort_values(['Loja', 'Vendedora']),width='stretch', hide_index=True)
    else:
        st.success("🟢 Todas as vendedoras possuem avaliação")

    st.markdown("---")

    st.markdown("### 💾 Exportar Dados")
    rv_exp = ranking_vendedoras_df(aval_vend_completa)
    rl_exp = ranking_lojas_df(avaliacoes, lojas)
    colunas_det = ['nome_cliente', 'loja', 'tipo', 'estrela_1_5', 'bem_atendimento', 'recomendacao_1_10', 'createdat']
    colunas_det = [c for c in colunas_det if c in aval_loja_completa.columns]

    c1, c2, c3 = st.columns(3)
    with c1:
        st.download_button("📥 Ranking Vendedoras", rv_exp.to_csv(index=False, encoding='utf-8-sig'), "ranking_vendedoras.csv", "text/csv")
    with c2:
        st.download_button("📥 Ranking Lojas", rl_exp.to_csv(index=False, encoding='utf-8-sig'), "ranking_lojas.csv", "text/csv")
    with c3:
        st.download_button("📥 Todas Avaliações", aval_loja_completa[colunas_det].to_csv(index=False, encoding='utf-8-sig'), "todas_avaliacoes.csv", "text/csv")
