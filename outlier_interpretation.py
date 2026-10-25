"""Interpretações descritivas, sem inferência causal ou validação de anomalias."""
from itertools import combinations
from analytics import detectors, describe, TEAMS


def interpret_outliers(df, team, metric):
    if team not in TEAMS:
        raise ValueError('Equipe inválida')
    methods = detectors(df, team, metric)
    sets = {name: {str(j['id']) for j in result['jogos']} for name, result in methods.items()}
    counts = {name: len(ids) for name, ids in sets.items()}
    pairs = []
    for a, b in combinations(sets, 2):
        intersection = len(sets[a] & sets[b])
        union = len(sets[a] | sets[b])
        pairs.append({'metodo_a': a, 'metodo_b': b, 'comuns': intersection,
                      'jaccard': round(intersection / union, 3) if union else None})
    valid_pairs = [p for p in pairs if p['jaccard'] is not None]
    valid_pairs.sort(key=lambda p: (-p['jaccard'], -p['comuns'], p['metodo_a'], p['metodo_b']))
    n = describe(df, team, metric)['n']
    union = set().union(*sets.values())
    consensus = {game: sum(game in ids for ids in sets.values()) for game in union}
    strong = sum(value >= 3 for value in consensus.values())
    return {
        'time': team, 'variavel': metric, 'n': n,
        'contagens': counts, 'total_unicos': len(union), 'tres_ou_mais': strong,
        'pares_maior_concordancia': valid_pairs[:3],
        'pares_menor_concordancia': list(reversed(valid_pairs[-3:])),
        'interpretacao': (
            f'Em {n} registros de {team}, {len(union)} jogos foram sinalizados por ao menos '
            f'um detector na variável {metric}; {strong} foram sinalizados por três ou mais. '
            'Concordância é apenas uma indicação de estabilidade entre critérios, não de erro '
            'na base nem de probabilidade de anomalia. Diferenças são esperadas porque IQR '
            'e Z-score usam regras globais, Grubbs testa um extremo sob normalidade, '
            'ECOD usa caudas empíricas e K-NN, DBSCAN e LOF usam vizinhança/densidade. '
            'Os detectores são univariados; configurações de 5% impõem sinalizações '
            'exploratórias e não devem ser interpretadas como taxa real de erros.'
        ),
        'ressalvas': [
            'Índice de Jaccard = interseção/união dos jogos sinalizados; quando ambos os métodos não sinalizam jogos, a razão é indefinida.',
            'Grubbs pressupõe normalidade e avalia apenas o extremo mais distante; seus resultados requerem cautela com distribuições assimétricas.',
            'A análise não verifica se a ocorrência é legítima ou erro de registro; investigar contexto esportivo antes de remover qualquer linha.',
            'Um jogo pode apresentar valores extremos por prorrogação, ritmo, adversário ou variação natural; esses fatores não foram controlados.'
        ]
    }
