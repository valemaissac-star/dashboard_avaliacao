import streamlit as st


def cores_vibrantes():
  
  CORES_VIBRANTES = [
      "#FF6B6B", "#FFE66D", "#4ECDC4", "#A855F7",
      "#F97316", "#22D3EE", "#10B981", "#F43F5E",
      "#6366F1", "#84CC16", "#EC4899", "#14B8A6",
      "#F59E0B", "#8B5CF6", "#06B6D4", "#EF4444"
]
  cores = CORES_VIBRANTES
  return cores


def template():

  TEMPLATE_GRAFICO = dict(
       template="plotly_dark",
       paper_bgcolor="rgba(15,12,41,0.0)",
       plot_bgcolor="rgba(15,12,41,0.0)",
       font=dict(family="Inter, sans-serif", size=14, color="#e0e0ff"),
       title_font=dict(size=20, color="#ffffff", family="Inter, sans-serif"),
)
  return TEMPLATE_GRAFICO


def style():
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
def inject_login_css():
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] {display: none;}
        header {visibility: hidden;}

        .stApp {
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e) !important;
        }

        /* Centraliza o bloco de login */
        section.main > div {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 90vh;
        }

        /* Card */
        div[data-testid="stForm"] {
            width: 400px !important;
            min-width: 400px !important;
            padding: 2.8rem 2.5rem !important;
            border-radius: 20px !important;
            background: linear-gradient(160deg, #1a1a3e, #12122b) !important;
            border: 1px solid rgba(100,100,255,0.25) !important;
            box-shadow: 0 0 50px rgba(80,60,200,0.35) !important;
        }

        /* Inputs */
        div[data-testid="stForm"] input {
            background: rgba(255,255,255,0.06) !important;
            color: #e0e0ff !important;
            border: 1px solid rgba(100,100,255,0.35) !important;
            border-radius: 10px !important;
            font-size: 1rem !important;
        }

        /* Labels */
        div[data-testid="stForm"] label p {
            color: #aaaaff !important;
            font-size: 0.78rem !important;
            font-weight: 700 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.5px !important;
        }

        /* Botão de SUBMIT (Login) - só o tipo submit */
        div[data-testid="stForm"] [data-testid="stFormSubmitButton"] button {
            width: 100% !important;
            background: linear-gradient(135deg, #6600cc, #9900ff) !important;
            color: white !important;
            font-weight: 700 !important;
            font-size: 1rem !important;
            border-radius: 12px !important;
            border: none !important;
            padding: 0.7rem 0 !important;
            box-shadow: 0 0 24px rgba(153,0,255,0.4) !important;
        }

        /* Botão do olho (ver senha) — resetar para transparente */
        div[data-testid="stForm"] button:not([data-testid="stFormSubmitButton"] button) {
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            color: #aaaaff !important;
            padding: 0 !important;
            width: auto !important;
        }
        </style>

        <div style="text-align:center; padding: 3vh 0 1.5rem;">
            <div style="
                width: 56px; height: 56px;
                background: linear-gradient(135deg, #6600cc, #9900ff);
                border-radius: 16px;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                font-size: 26px;
                box-shadow: 0 0 22px rgba(153,0,255,0.45);
                margin-bottom: 1.1rem;
            ">📊</div>
            <h2 style="
                color: #ffffff;
                font-weight: 800;
                font-size: 1.9rem;
                margin: 0 0 0.3rem;
                letter-spacing: -0.5px;
            ">Valemais Promotora</h2>
            <p style="
                color: #9399b2;
                font-size: 0.78rem;
                margin: 0;
                text-transform: uppercase;
                letter-spacing: 0.6px;
            ">Dashboard de Avaliações</p>
        </div>
        """,
        unsafe_allow_html=True,
    )