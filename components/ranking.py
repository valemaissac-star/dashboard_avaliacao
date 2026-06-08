import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from services.metrics import ranking_vendedoras_df   
from services.metrics import ranking_supervisores_df  
from services.metrics import ranking_lojas_df 
from components.charts import grafico_ranking_h
from config.theme import template

def secao_ranking_completa(dados,aval_df, aval_vend_df, aval_sup_df, sufixo=""):

    aval_supervisores  = dados['aval_supervisores']
    # Ranking de Vendedoras
    st.markdown("### 🏆 Ranking de Vendedoras")
    rv = ranking_vendedoras_df(aval_vend_df)

    if len(rv) > 0:
        st.plotly_chart(grafico_ranking_h(rv, 'Vendedora', 'Score Final', 'Top Vendedoras', "Plasma", 550),
                        use_container_width=True, key=f"rank_vend_{sufixo}")
        st.dataframe(rv.round(2), use_container_width=True, hide_index=True)

        st.markdown("## 🔎 Detalhes por Vendedora 👩‍💼")
        list_v = sorted(rv['Vendedora'].dropna().unique().tolist())
        v_sel = st.selectbox("Selecione a vendedora:", list_v, key=f"sel_vend_{sufixo}")
        aval_sel = aval_vend_df[aval_vend_df['vendedora'] == v_sel]

        if len(aval_sel) > 0:
            loja_vend = aval_sel['loja'].iloc[0] if 'loja' in aval_sel.columns and not aval_sel['loja'].isna().all() else "Sem loja"

            c1, c2, c3, c4, c5 = st.columns(5)
            c1.metric("🌟 Média Estrelas", f"{aval_sel['estrela_1_5'].mean():.2f}/5")
            c2.metric("👌 Média Recomendação", f"{aval_sel['recomendacao_1_10'].mean():.2f}/10")
            pct = (aval_sel['bem_atendimento'] == 'sim').sum() / len(aval_sel) * 100
            c3.metric("😎 Bem Atendimento", f"{pct:.1f}%")
            c4.metric("📒 Total", len(aval_sel))
            c5.metric("🏬 Loja", loja_vend)

            cc1, cc2 = st.columns(2)

            with cc1:
                dist = aval_sel['estrela_1_5'].value_counts().sort_index()
                fig = go.Figure(data=[go.Bar(
                    x=dist.index,
                    y=dist.values,
                    text=dist.values,
                    textposition='outside',
                    textfont=dict(size=15),
                    marker=dict(
                        color=dist.values,
                        colorscale="Turbo",
                        line=dict(color="rgba(255, 255, 255, 0.2)", width=1),
                    )
                )])
                fig.update_layout(template(), title=f"⭐ Estrelas — {v_sel}", height=380)
                st.plotly_chart(fig, use_container_width=True, key=f"estrelas_vend_{sufixo}_{v_sel}")

            with cc2:
                dist2 = aval_sel['bem_atendimento'].value_counts()
                fig2 = go.Figure(data=[go.Pie(
                    labels=dist2.index,
                    values=dist2.values,
                    hole=0.45,
                    marker=dict(colors=["#10B981", "#F97316", "#F43F5E"], line=dict(color="#0f0c29")),
                    textfont=dict(size=15)
                )])
                fig2.update_layout(template(), title=f"🤩 Atendimento — {v_sel}", height=380)
                st.plotly_chart(fig2, use_container_width=True, key=f"atend_vend_{sufixo}_{v_sel}")

        if 'comentario_cliente' in aval_sel.columns:
            comentarios = aval_sel[aval_sel['comentario_cliente'].notna()]
            if len(comentarios) > 0:
                st.markdown("**🗯️ Comentários:**")
                for _, row in comentarios.iterrows():
                    stars = int(row['estrela_1_5']) if not pd.isna(row['estrela_1_5']) else 0
                    st.markdown(f"""
                        <div style='background:linear-gradient(135deg, #1a1a3e, #2d2d6b);
                                    border-left:4px solid #A855F7;
                                    border-radius:10px;
                                    padding:14px 18px;
                                    margin-bottom:10px;'>
                            <span style='color:#FFE66D; font-size:1.1rem; font-weight:700;'>
                                {"🌠" * stars} ({stars}/5)
                            </span><br>
                            <span style='color:#c0c0ff; font-size:1rem;'>{row['comentario_cliente']}</span>
                        </div>
                    """, unsafe_allow_html=True)
    else:
        st.info("Sem avaliações de vendedoras neste período.")

    st.markdown("---")

    # Ranking Supervisores
    st.markdown("### 👔 Ranking de Supervisores")
    rs = ranking_supervisores_df(aval_sup_df, dados['supervisores'])
    if len(rs) > 0:
        st.plotly_chart(grafico_ranking_h(rs, 'Supervisor', 'Score Final', 'Ranking Supervisores', 'Rainbow', 450),
                        use_container_width=True, key=f"rank_sup_{sufixo}")
        st.dataframe(rs.round(2), use_container_width=True, hide_index=True)
    else:
        st.info("Sem avaliações de supervisores neste período.")

    st.markdown("---")

    # Ranking Lojas
    st.markdown("### 🏬 Ranking das Lojas")
    rl = ranking_lojas_df(aval_df, dados['lojas'])
    if len(rl) > 0:
        st.plotly_chart(grafico_ranking_h(rl, 'Loja', 'Score Final', 'Top Lojas 🏬', 'Turbo', 550),
                        use_container_width=True, key=f"rank_loja_{sufixo}")
        st.dataframe(rl.round(2), use_container_width=True, hide_index=True)
    else:
        st.info("Sem avaliações de lojas neste período.")
