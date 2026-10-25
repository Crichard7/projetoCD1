"""Síntese descritiva reproduzível, sem inferência causal ou testes de hipótese."""
from analytics import TEAMS, METRICS, describe


def _skew_label(value):
    if value is None:
        return 'indeterminada'
    strength = 'aproximadamente simétrica' if abs(value) < .5 else ('moderada' if abs(value) < 1 else 'forte')
    direction = 'positiva (à direita)' if value > 0 else ('negativa (à esquerda)' if value < 0 else 'nula')
    return f'{strength}; {direction}'


def synthesize(df):
    rows = []
    for metric, label in METRICS.items():
        by_team = {team: describe(df, team, metric) for team in TEAMS}
        if any(result is None for result in by_team.values()):
            continue
        a, b = (by_team[team] for team in TEAMS)
        lower_cv = TEAMS[0] if a['cv'] < b['cv'] else TEAMS[1] if b['cv'] < a['cv'] else 'Empate'
        lower_iqr = TEAMS[0] if a['iqr'] < b['iqr'] else TEAMS[1] if b['iqr'] < a['iqr'] else 'Empate'
        higher_mean = TEAMS[0] if a['media'] > b['media'] else TEAMS[1] if b['media'] > a['media'] else 'Empate'
        caution = any(r['media'] < 2 or (r['assimetria'] is not None and abs(r['assimetria']) >= 1) for r in (a, b))
        rows.append({
            'variavel': metric, 'rotulo': label,
            'equipes': {team: {
                'n': int(r['n']), 'media': float(r['media']), 'mediana': float(r['mediana']),
                'desvio': float(r['desvio']), 'amplitude': float(r['amplitude']),
                'q1': float(r['q1']), 'q3': float(r['q3']), 'iqr': float(r['iqr']),
                'cv': float(r['cv']), 'assimetria': float(r['assimetria']) if r['assimetria'] is not None else None,
                'classe_assimetria': _skew_label(r['assimetria']),
                'outliers_iqr': int(r['outlier_count'])
            } for team, r in by_team.items()},
            'maior_media': higher_mean, 'menor_cv': lower_cv, 'menor_iqr': lower_iqr,
            'diferenca_media_absoluta': float(abs(a['media'] - b['media'])),
            'cautela_cv': caution
        })
    return {'equipes': TEAMS, 'linhas': rows, 'metodologia': {
        'cv': '100 × desvio padrão amostral / média (média positiva)',
        'iqr': 'Q3 − Q1; quartis por interpolação linear',
        'assimetria': 'Fisher–Pearson ajustado, scipy.stats.skew(bias=False)',
        'outliers': 'Regra de Tukey: abaixo de Q1 − 1,5 × IQR ou acima de Q3 + 1,5 × IQR',
        'escopo': 'Comparações descritivas por jogo, sem ajuste para adversário, ritmo ou mando de quadra'
    }}
