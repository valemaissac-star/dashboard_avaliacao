# ======================================================
# PROCESSAMENTO BASE
# ======================================================
from data.loader import load_data
import pandas as pd


def get_dataframes():

    avaliacoes, vendedoras, lojas, supervisores, supervisores_lojas = load_data()

    avaliacoes.columns         = avaliacoes.columns.str.strip().str.lower()
    vendedoras.columns         = vendedoras.columns.str.strip().str.lower()
    lojas.columns              = lojas.columns.str.strip().str.lower()
    supervisores.columns       = supervisores.columns.str.strip().str.lower()
    supervisores_lojas.columns = supervisores_lojas.columns.str.strip().str.lower()

    vendedoras = vendedoras.rename(columns={'lojaid': 'loja_id', '_id': 'id'})
    lojas = lojas.rename(columns={'_id': 'id'})
    supervisores = supervisores.rename(columns={'_id': 'id'})
    avaliacoes = avaliacoes.rename(columns={
        '_id': 'id',
        'vendedoraid': 'vendedora_id',
        'supervisorid': 'supervisor_id',
        'lojaid': 'loja_id'
    })

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

    meses_disponiveis = sorted(avaliacoes['mes_ano_str'].dropna().unique().tolist())

    return dict(
        avaliacoes=avaliacoes,
        vendedoras=vendedoras,
        lojas=lojas,
        supervisores=supervisores,
        supervisores_lojas=supervisores_lojas,
        aval_vendedoras=aval_vendedoras,
        aval_supervisores=aval_supervisores,
        aval_loja_completa=aval_loja_completa,
        aval_vend_completa=aval_vend_completa,
        meses_disponiveis=meses_disponiveis,
    )