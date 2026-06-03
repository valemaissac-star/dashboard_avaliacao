import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(
    page_title="Dashboard de Avaliações",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ======================================================
# TEMA VISUAL GLOBAL
# ======================================================

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    }
    h1 { font-size: 2.8rem !important; font-weight: 900 !important; color: #ffffff !important; }
    h2 { font-size: 2rem !important; font-weight: 800 !important; color: #e0e0ff !important; }
    h3 { font-size: 1.6rem !important; font-weight: 700 !important; color: #c0c0ff !important; }
    p, div, span, label { font-size: 1.05rem !important; }
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #1a1a3e, #2d2d6b);
        border: 1px solid #4444aa;
        border-radius: 16px;
        padding: 20px !important;
        box-shadow: 0 0 20px rgba(100, 100, 255, 0.3);
    }
    [data-testid="metric-container"] label {
        font-size: 1rem !important;
        color: #aaaaff !important;
        font-weight: 700 !important;
    }
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: 900 !important;
        color: #ffffff !important;
    }
    .stSelectbox label { font-size: 1.1rem !important; font-weight: 700 !important; color: #aaaaff !important; }
    .stDataFrame { border-radius: 12px; overflow: hidden; }
    hr { border-color: #4444aa !important; opacity: 0.4; }
    .stDownloadButton button {
        background: linear-gradient(135deg, #6600cc, #9900ff) !important;
        color: white !important;
        font-weight: 700 !important;
        border-radius: 10px !important;
        font-size: 1rem !important;
        border: none !important;
    }
    .metric-principal {
        background: linear-gradient(135deg, #2d1b69, #4a2c8e);
        border: 2px solid #7c5cdb;
        border-radius: 20px;
        padding: 30px !important;
        box-shadow: 0 0 30px rgba(124, 92, 219, 0.4);
        text-align: center;
    }
    .metric-principal-value {
        font-size: 3.5rem !important;
        font-weight: 900 !important;
        color: #FFE66D !important;
        margin: 10px 0;
    }
    .metric-principal-label {
        font-size: 1.3rem !important;
        color: #c0c0ff !important;
        font-weight: 700 !important;
    }
    .stTabs[data-baseweb="tab-list"] {
        background: linear-gradient(135deg, #1a1a3e, #2d2d6b);
        border-radius: 14px;
        padding: 6px;
        gap: 6px;
    }
    .stTabs[data-baseweb="tab"] {
        background: transparent;
        border-radius: 10px;
        color: #aaaaff !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #6600cc, #9900ff) !important;
        color: white !important;
    }
    .mes-card {
        background: linear-gradient(135deg, #1a1a3e, #2d2d6b);
        border-radius: 14px;
        padding: 16px 20px;
        margin-bottom: 10px;
        box-shadow: 0 0 12px rgba(100, 100, 255, 0.2);
    }
</style>
""", unsafe_allow_html=True)

CORES_VIBRANTES = [
    "#FF6B6B", "#FFE66D", "#4ECDC4", "#A855F7",
    "#F97316", "#22D3EE", "#10B981", "#F43F5E",
    "#6366F1", "#84CC16", "#EC4899", "#14B8A6",
    "#F59E0B", "#8B5CF6", "#06B6D4", "#EF4444"
]

TEMPLATE_GRAFICO = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(15,12,41,0.0)",
    plot_bgcolor="rgba(15,12,41,0.0)",
    font=dict(family="Inter, sans-serif", size=14, color="#e0e0ff"),
    title_font=dict(size=20, color="#ffffff", family="Inter, sans-serif"),
)

# ======================================================
# CARREGAMENTO DOS DADOS
# ======================================================

@st.cache_data
def load_data():
    paths = [
        ('arquivos_30_04_26/', 'Pasta arquivos'),
        ('arquivos/', 'Pasta arquivos'),
        ('', 'Raiz do repositório'),
    ]
    for path_prefix, _ in paths:
        try:
            avaliacoes = pd.read_excel(f'{path_prefix}avaliacoes.xlsx')
            vendedoras = pd.read_excel(f'{path_prefix}vendedoras.xlsx')
            lojas = pd.read_excel(f'{path_prefix}lojas.xlsx')
            supervisores = pd.read_excel(f'{path_prefix}supervisores.xlsx')
            supervisores_lojas = pd.read_excel(f'{path_prefix}supervisores_lojas.xlsx')
            return avaliacoes, vendedoras, lojas, supervisores, supervisores_lojas
        except Exception:
            continue
    raise FileNotFoundError("❌ Arquivos Excel não encontrados!")

try:
    avaliacoes, vendedoras, lojas, supervisores, supervisores_lojas = load_data()
except FileNotFoundError as e:
    st.error(str(e))
    st.stop()

# ======================================================
# PROCESSAMENTO BASE
# ======================================================

for df in [avaliacoes, vendedoras, lojas, supervisores, supervisores_lojas]:
    df.columns = df.columns.str.lower().str.strip()

vendedoras = vendedoras.rename(columns={'lojaid': 'loja_id', '_id': 'id'})
avaliacoes = avaliacoes.rename(columns={'_id': 'id', 'vendedoraid': 'vendedora_id', 'supervisorid': 'supervisor_id', 'lojaid': 'loja_id'})
supervisores = supervisores.rename(columns={'_id': 'id'})
lojas = lojas.rename(columns={'_id': 'id'})

avaliacoes['estrela_1_5'] = pd.to_numeric(avaliacoes['estrela_1_5'], errors='coerce')
avaliacoes['recomendacao_1_10'] = pd.to_numeric(avaliacoes['recomendacao_1_10'], errors='coerce')
avaliacoes['createdat'] = pd.to_datetime(avaliacoes['createdat'], errors='coerce')
avaliacoes['mes_ano'] = avaliacoes['createdat'].dt.to_period('M')
avaliacoes['mes_ano_str'] = avaliacoes['mes_ano'].astype(str)

aval_vendedoras = avaliacoes[avaliacoes['tipo'] == 'vendedora'].copy()
aval_supervisores = avaliacoes[avaliacoes['tipo'] == 'supervisor'].copy()

aval_loja_completa = avaliacoes.merge(
    lojas[['id', 'loja']], left_on='loja_id', right_on='id', how='left'
)

aval_vend_completa = avaliacoes.merge(
    vendedoras[['id', 'vendedora', 'loja_id']], left_on='vendedora_id', right_on='id', how='left', suffixes=('', '_vend')
)

if 'loja_id_vend' in aval_vend_completa.columns:
    aval_vend_completa['loja_id'] = aval_vend_completa['loja_id_vend']

aval_vend_completa = aval_vend_completa.merge(
    lojas[['id', 'loja']], left_on='loja_id', right_on='id', how='left'
)

meses_disponives = sorted(avaliacoes['mes_ano_str'].dropna().unique().tolist())

# ======================================================
# FUNÇÕES AUXILIARES
# ======================================================

def calcular_metricas(df):
    total = len(df)
    media_est = df['estrela_1_5'].mean() if total > 0 else 0
    media_rec = df['recomendacao_1_10'].mean() if total > 0 else 0
    pct_bem = (df['bem_atendimento'] == 'sim').sum() / total * 100 if total > 0 else 0
    return total, media_est, media_rec, pct_bem


def ranking_vendedoras_df(aval_vend_df):
    if len(aval_vend_df) == 0:
        return pd.DataFrame()

    r = aval_vend_df.groupby(['vendedora', 'loja']).agg(
        media_estrelas=('estrela_1_5', 'mean'),
        total=('estrela_1_5', 'count'),
        media_recomendacao=('recomendacao_1_10', 'mean'),
        pct_bem=('bem_atendimento', lambda x: (x == 'sim').sum() / len(x) * 100)
    ).reset_index()

    max_aval = r['total'].max()
    r['volume_normalizado'] = (r['total'] / max_aval) * 5 if max_aval > 0 else 0
    r['score_final'] = r['media_estrelas'] * 0.7 + r['volume_normalizado'] * 0.3
    r = r.sort_values('score_final', ascending=False)

    r = r.rename(columns={
        'vendedora': 'Vendedora',
        'loja': 'Loja',
        'media_estrelas': 'Média Estrelas',
        'total': 'Total Avaliações',
        'media_recomendacao': 'Média Recomendação',
        'pct_bem': '% Bem Atendimento',
        'volume_normalizado': 'Volume Normalizado',
        'score_final': 'Score Final'
    })
    return r


def ranking_supervisores_df(aval_sup_df):
    if len(aval_sup_df) == 0:
        return pd.DataFrame()

    aval_sup_c = aval_sup_df.merge(
        supervisores[['id', 'nome_supervisor']], left_on='supervisor_id', right_on='id', how='left'
    )

    r = aval_sup_c.groupby('nome_supervisor').agg(
        media_estrelas=('estrela_1_5', 'mean'),
        total=('estrela_1_5', 'count'),
        media_recomendacao=('recomendacao_1_10', 'mean'),
        pct_bem=('bem_atendimento', lambda x: (x == 'sim').sum() / len(x) * 100)
    ).reset_index()

    max_super = r['total'].max()
    r['volume_normalizado'] = (r['total'] / max_super) * 5 if max_super > 0 else 0
    r['score_final'] = r['media_estrelas'] * 0.7 + r['volume_normalizado'] * 0.3
    r = r.sort_values('score_final', ascending=False)

    r = r.rename(columns={
        'nome_supervisor': 'Supervisor',
        'media_estrelas': 'Média Estrelas',
        'total': 'Total Avaliações',
        'media_recomendacao': 'Média Recomendação',
        'pct_bem': '% Bem Atendimento',
        'volume_normalizado': 'Volume Normalizado',
        'score_final': 'Score Final'
    })
    return r


def ranking_lojas_df(aval_loja_df):
    if len(aval_loja_df) == 0:
        return pd.DataFrame()

    aval_loja_c = aval_loja_df.merge(lojas[['id', 'loja']], left_on='loja_id', right_on='id', how='left')

    r = aval_loja_c.groupby('loja').agg(
        media_estrelas=('estrela_1_5', 'mean'),
        total=('estrela_1_5', 'count'),
        media_recomendacao=('recomendacao_1_10', 'mean'),
        pct_bem=('bem_atendimento', lambda x: (x == 'sim').sum() / len(x) * 100)
    ).reset_index()

    max_loja = r['total'].max()
    r['volume_normalizado'] = (r['total'] / max_loja) * 5 if max_loja > 0 else 0
    r['score_final'] = r['media_estrelas'] * 0.7 + r['volume_normalizado'] * 0.3
    r = r.sort_values('score_final', ascending=False)

    r = r.rename(columns={
        'loja': 'Loja',
        'media_estrelas': 'Média Estrelas',
        'total': 'Total Avaliações',
        'media_recomendacao': 'Média Recomendação',
        'pct_bem': '% Bem Atendimento',
        'volume_normalizado': 'Volume Normalizado',
        'score_final': 'Score Final'
    })
    return r


def grafico_ranking_h(df, col_y, col_x, titulo, colorscale="Plasma", height=500):
    top = df.head(20)
    fig = go.Figure(data=[go.Bar(
        y=top[col_y],
        x=top[col_x],
        orientation='h',
        text=top[col_x].round(2),
        textposition='outside',
        textfont=dict(size=14, color="#ffffff"),
        marker=dict(
            color=top[col_x],
            colorscale=colorscale,
            showscale=True,
            colorbar=dict(title='Score', tickfont=dict(size=13)),
            line=dict(color="rgba(255, 255, 255, 0.1)", width=1)
        ),
    )])
    fig.update_layout(
        **TEMPLATE_GRAFICO,
        title=titulo,
        height=height,
        xaxis=dict(title="Score Final", tickfont=dict(size=13)),
        yaxis=dict(tickfont=dict(size=13), autorange="reversed"),
    )
    return fig


def secao_ranking_completa(aval_df, aval_vend_df, aval_sup_df, sufixo=""):

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
                fig.update_layout(**TEMPLATE_GRAFICO, title=f"⭐ Estrelas — {v_sel}", height=380)
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
                fig2.update_layout(**TEMPLATE_GRAFICO, title=f"🤩 Atendimento — {v_sel}", height=380)
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
    rs = ranking_supervisores_df(aval_sup_df)
    if len(rs) > 0:
        st.plotly_chart(grafico_ranking_h(rs, 'Supervisor', 'Score Final', 'Ranking Supervisores', 'Rainbow', 450),
                        use_container_width=True, key=f"rank_sup_{sufixo}")
        st.dataframe(rs.round(2), use_container_width=True, hide_index=True)
    else:
        st.info("Sem avaliações de supervisores neste período.")

    st.markdown("---")

    # Ranking Lojas
    st.markdown("### 🏬 Ranking das Lojas")
    rl = ranking_lojas_df(aval_df)
    if len(rl) > 0:
        st.plotly_chart(grafico_ranking_h(rl, 'Loja', 'Score Final', 'Top Lojas 🏬', 'Turbo', 550),
                        use_container_width=True, key=f"rank_loja_{sufixo}")
        st.dataframe(rl.round(2), use_container_width=True, hide_index=True)
    else:
        st.info("Sem avaliações de lojas neste período.")


# ======================================================
# HEADER
# ======================================================

st.markdown("""
<div style='text-align:center; padding: 2rem 0 1rem 0;'>
    <h1>⭐ Dashboard de Avaliações</h1>
    <p style='color:#aaaaff; font-size:1.2rem !important;'>Análise completa de Vendedoras, Supervisores e Lojas</p>
</div>
""", unsafe_allow_html=True)
st.markdown("---")

# ======================================================
# ABAS PRINCIPAIS
# ======================================================

aba_geral, aba_mensal, aba_por_mes = st.tabs([
    "📈 Visão Geral",
    "📅 Evolução Mensal",
    "⏰ Análise por Mês"
])

# ======================================================
# ABA 1 — VISÃO GERAL
# ======================================================

with aba_geral:
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
            marker=dict(colors=CORES_VIBRANTES, line=dict(color="#0f0c29", width=3)),
            textfont=dict(size=16),
        )])
        fig.update_layout(**TEMPLATE_GRAFICO, title="⭐ Distribuição de Estrelas", height=420)
        st.plotly_chart(fig, use_container_width=True, key="pizza_estrelas_geral")

    with col_p2:
        dist_atend = avaliacoes['bem_atendimento'].value_counts()
        fig2 = go.Figure(data=[go.Pie(
            labels=dist_atend.index,
            values=dist_atend.values,
            hole=0.4,
            marker=dict(colors=["#10b981", "#f97316", "#f43f5e"], line=dict(color="#0f0c29")),
            textfont=dict(size=16)
        )])
        fig2.update_layout(**TEMPLATE_GRAFICO, title="😊 Bem Atendimento", height=420)
        st.plotly_chart(fig2, use_container_width=True, key="pizza_atend_geral")

    st.markdown("---")

    secao_ranking_completa(avaliacoes, aval_vend_completa, aval_supervisores, sufixo="geral")

    st.markdown("---")

    st.markdown("### 🚨 Vendedoras Sem Avaliação")
    ids_avaliadas = aval_vendedoras['vendedora_id'].dropna().unique()
    vendedoras_sem = vendedoras[~vendedoras['id'].isin(ids_avaliadas)].copy()
    vendedoras_sem = vendedoras_sem.merge(lojas[['id', 'loja']], left_on='loja_id', right_on='id', how='left')
    if len(vendedoras_sem) > 0:
        tabela_sem = vendedoras_sem[['vendedora', 'loja']].copy()
        tabela_sem.columns = ['Vendedora', 'Loja']
        st.error(f"⚠️ {len(tabela_sem)} vendedoras estão sem avaliações")
        st.dataframe(tabela_sem.sort_values(['Loja', 'Vendedora']), use_container_width=True, hide_index=True)
    else:
        st.success("🟢 Todas as vendedoras possuem avaliação")

    st.markdown("---")

    st.markdown("### 💾 Exportar Dados")
    rv_exp = ranking_vendedoras_df(aval_vend_completa)
    rl_exp = ranking_lojas_df(avaliacoes)
    colunas_det = ['nome_cliente', 'loja', 'tipo', 'estrela_1_5', 'bem_atendimento', 'recomendacao_1_10', 'createdat']
    colunas_det = [c for c in colunas_det if c in aval_loja_completa.columns]

    c1, c2, c3 = st.columns(3)
    with c1:
        st.download_button("📥 Ranking Vendedoras", rv_exp.to_csv(index=False, encoding='utf-8-sig'), "ranking_vendedoras.csv", "text/csv")
    with c2:
        st.download_button("📥 Ranking Lojas", rl_exp.to_csv(index=False, encoding='utf-8-sig'), "ranking_lojas.csv", "text/csv")
    with c3:
        st.download_button("📥 Todas Avaliações", aval_loja_completa[colunas_det].to_csv(index=False, encoding='utf-8-sig'), "todas_avaliacoes.csv", "text/csv")

# ======================================================
# ABA 2 — EVOLUÇÃO MENSAL
# ======================================================

with aba_mensal:
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
    fig_vol.update_layout(**TEMPLATE_GRAFICO, title="📊 Quantidade de Avaliações por Mês", height=500,
                          xaxis=dict(title="Mês", tickfont=dict(size=14)),
                          yaxis=dict(title="Quantidade", tickfont=dict(size=14)))
    st.plotly_chart(fig_vol, use_container_width=True, key="vol_mensal")

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
        fig_est.update_layout(**TEMPLATE_GRAFICO, title="⭐ Evolução da Média de Estrelas", height=400,
                              xaxis=dict(title="Mês"),
                              yaxis=dict(title="Média (1-5)", range=[1, 5.4]))
        st.plotly_chart(fig_est, use_container_width=True, key="evo_estrelas")

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
        fig_rec.update_layout(**TEMPLATE_GRAFICO, title="👍 Evolução da Média de Recomendação", height=400,
                              xaxis=dict(title="Mês"),
                              yaxis=dict(title="Média (1-10)", range=[0, 11]))
        st.plotly_chart(fig_rec, use_container_width=True, key="evo_recomendacao")

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
    fig_bem.update_layout(**TEMPLATE_GRAFICO, title="😊 Evolução do % Bem Atendimento", height=390,
                          xaxis=dict(title="Mês"),
                          yaxis=dict(title="%", range=[0, 110]))
    st.plotly_chart(fig_bem, use_container_width=True, key="evo_bem_atend")

    st.markdown("---")

    st.markdown("### 📋 Tabela Resumo Mensal")
    evo_display = evo.copy().rename(columns={
        'total': 'Total Avaliações',
        'media_estrelas': 'Média Estrelas',
        'media_recomendacao': 'Média Recomendação',
        'bem_atendimento': '% Bem Atendimento'
    })
    st.dataframe(evo_display.round(2), use_container_width=True, hide_index=True)

# ======================================================
# ABA 3 — ANÁLISE POR MÊS
# ======================================================

with aba_por_mes:
    st.markdown("### ⏰ Análise Detalhada por Mês")

    if not meses_disponives:
        st.warning("Nenhum mês identificado nos dados.")
        st.stop()

    mes_sel = st.selectbox("Selecione o mês para análise:", options=meses_disponives,
                           index=len(meses_disponives) - 1, key="sel_mes_principal")

    aval_mes = avaliacoes[avaliacoes['mes_ano_str'] == mes_sel].copy()
    aval_vend_mes = aval_vend_completa[aval_vend_completa['mes_ano_str'] == mes_sel].copy()
    aval_sup_mes = aval_supervisores[aval_supervisores['mes_ano_str'] == mes_sel].copy()

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

    idx_mes = meses_disponives.index(mes_sel)
    if idx_mes > 0:
        mes_ant = meses_disponives[idx_mes - 1]
        aval_ant = avaliacoes[avaliacoes['mes_ano_str'] == mes_ant]
        delta_tot = total_m - len(aval_ant)
        col5.metric("📊 Variação vs Mês Anterior", f"{total_m:,} avaliações", delta=f"{delta_tot:+,} avaliações")

    st.markdown("---")

    col_p1, col_p2 = st.columns(2)
    with col_p1:
        dist_est = aval_mes['estrela_1_5'].value_counts().sort_index()
        fig_p1 = go.Figure(data=[go.Pie(
            labels=[f"{int(i)} estrela(s)" for i in dist_est.index],
            values=dist_est.values, hole=0.4,
            marker=dict(colors=CORES_VIBRANTES, line=dict(color='#0f0c29', width=3)),
            textfont=dict(size=16),
        )])
        fig_p1.update_layout(**TEMPLATE_GRAFICO, title=f"⭐ Estrelas — {mes_sel}", height=400)
        st.plotly_chart(fig_p1, use_container_width=True, key=f"pizza_est_{mes_sel}")

    with col_p2:
        dist_atend = aval_mes['bem_atendimento'].value_counts()
        fig_p2 = go.Figure(data=[go.Pie(
            labels=dist_atend.index, values=dist_atend.values, hole=0.4,
            marker=dict(colors=["#10B981", "#F97316", "#F43F5E"], line=dict(color="#0f0c29", width=3)),
            textfont=dict(size=16),
        )])
        fig_p2.update_layout(**TEMPLATE_GRAFICO, title=f"😊 Bem Atendimento — {mes_sel}", height=400)
        st.plotly_chart(fig_p2, use_container_width=True, key=f"pizza_atend_{mes_sel}")

    st.markdown("---")

    secao_ranking_completa(aval_mes, aval_vend_mes, aval_sup_mes, sufixo=mes_sel.replace("-", "_"))

    st.markdown("---")

    st.markdown("### 🚨 Vendedoras Sem Avaliação neste Mês")
    ids_aval_mes = aval_vend_mes['vendedora_id'].dropna().unique() if 'vendedora_id' in aval_vend_mes.columns else []
    vend_sem_mes = vendedoras[~vendedoras['id'].isin(ids_aval_mes)].copy()
    vend_sem_mes = vend_sem_mes.merge(lojas[['id', 'loja']], left_on='loja_id', right_on='id', how='left')
    if len(vend_sem_mes) > 0:
        tab_sem = vend_sem_mes[['vendedora', 'loja']].copy()
        tab_sem.columns = ['Vendedora', 'Loja']
        st.error(f"⚠️ {len(tab_sem)} vendedoras sem avaliação em {mes_sel}")
        st.dataframe(tab_sem.sort_values(['Loja', 'Vendedora']), use_container_width=True, hide_index=True)
    else:
        st.success(f"✅ Todas as vendedoras têm avaliação em {mes_sel}!")

    st.markdown("---")

    st.markdown("### 💾 Exportar Dados do Mês")
    rv_mes = ranking_vendedoras_df(aval_vend_mes)
    rl_mes = ranking_lojas_df(aval_mes)

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
st.markdown("<p style='text-align:center;color:#6666aa;font-size:0.95rem;'>Dashboard de Avaliações · Atualize a página para recarregar</p>",
            unsafe_allow_html=True)