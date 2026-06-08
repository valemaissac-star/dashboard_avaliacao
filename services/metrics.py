import pandas as pd

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

    return r.rename(columns={
        'vendedora': 'Vendedora', 'loja': 'Loja',
        'media_estrelas': 'Média Estrelas', 'total': 'Total Avaliações',
        'media_recomendacao': 'Média Recomendação', 'pct_bem': '% Bem Atendimento',
        'volume_normalizado': 'Volume Normalizado', 'score_final': 'Score Final'
    })


def ranking_supervisores_df(aval_sup_df, supervisores):  
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

    return r.rename(columns={
        'nome_supervisor': 'Supervisor',
        'media_estrelas': 'Média Estrelas', 'total': 'Total Avaliações',
        'media_recomendacao': 'Média Recomendação', 'pct_bem': '% Bem Atendimento',
        'volume_normalizado': 'Volume Normalizado', 'score_final': 'Score Final'
    })


def ranking_lojas_df(aval_loja_df, lojas):  
    if len(aval_loja_df) == 0:
        return pd.DataFrame()

    aval_loja_c = aval_loja_df.merge(
        lojas[['id', 'loja']], left_on='loja_id', right_on='id', how='left'
    )

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

    return r.rename(columns={
        'loja': 'Loja',
        'media_estrelas': 'Média Estrelas', 'total': 'Total Avaliações',
        'media_recomendacao': 'Média Recomendação', 'pct_bem': '% Bem Atendimento',
        'volume_normalizado': 'Volume Normalizado', 'score_final': 'Score Final'
    })