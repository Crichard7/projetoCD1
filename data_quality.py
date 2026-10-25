"""Auditoria reproduzível de qualidade de dados para o Grupo 1."""
import pandas as pd

COUNT_COLS = ['W','L','MIN','FGM','FGA','FG3M','FG3A','FTM','FTA','OREB','DREB','REB','AST','STL','BLK','TOV','PF','PTS']
PERCENT_COLS = ['W_PCT','FG_PCT','FG3_PCT','FT_PCT']

def audit(raw):
    frame = raw.loc[raw['TEAM_NAME'].isin(['Los Angeles Lakers','Denver Nuggets'])].copy()
    checks = {}
    def record(label, mask, rationale):
        bad = frame.loc[mask.fillna(False)]
        checks[label] = {'quantidade':int(len(bad)), 'exemplos':bad[['TEAM_NAME','Game_ID','GAME_DATE']].head(5).astype(str).to_dict('records'), 'criterio':rationale}
    record('Duplicatas exatas', frame.duplicated(), 'Todas as colunas iguais')
    record('Chave time + jogo repetida', frame.duplicated(['Team_ID','Game_ID'],keep=False), 'Uma linha por time por jogo')
    dates = pd.to_datetime(frame['GAME_DATE'],errors='coerce')
    record('Datas inválidas', dates.isna(), 'Data não convertível')
    record('Vitória fora do domínio', ~frame['WL'].isin([0,1]), 'WL deve ser 0 ou 1')
    for c in COUNT_COLS:
        values = pd.to_numeric(frame[c],errors='coerce')
        record(f'{c}: negativo/não inteiro', values.notna() & ((values<0) | (values%1!=0)), 'Contagem não negativa e inteira')
    for c in PERCENT_COLS:
        values = pd.to_numeric(frame[c],errors='coerce')
        record(f'{c}: fora de [0,1]', values.notna() & ~values.between(0,1), 'Proporção entre zero e um')
    def mismatch(label, lhs, rhs, tolerance=0):
        record(label, lhs.notna() & rhs.notna() & ((lhs-rhs).abs()>tolerance), f'Diferença absoluta superior a {tolerance}')
    mismatch('Rebotes ≠ ofensivos + defensivos',frame['REB'],frame['OREB']+frame['DREB'])
    mismatch('Pontos ≠ 2×FGM + FG3M + FTM',frame['PTS'],2*frame['FGM']+frame['FG3M']+frame['FTM'])
    for made,attempt,pct in [('FGM','FGA','FG_PCT'),('FG3M','FG3A','FG3_PCT'),('FTM','FTA','FT_PCT')]:
        record(f'{made} > {attempt}',frame[made]>frame[attempt],'Acertos não podem superar tentativas')
        expected = frame[made]/frame[attempt].replace(0,float('nan'))
        mismatch(f'{pct}: divergência de proporção',frame[pct],expected,0.001)
        record(f'{pct}: tentativas zero e percentual não zero',(frame[attempt]==0)&(frame[pct]!=0),'Sem tentativas, aproveitamento esperado zero')
    return {
        'n_linhas':int(len(frame)),
        'ausentes_por_coluna':{k:int(v) for k,v in frame.isna().sum().items()},
        'total_ausentes':int(frame.isna().sum().sum()),
        'zeros_metricas':{c:int((frame[c]==0).sum()) for c in ['PTS','REB','AST','STL','BLK','PF','FG3M']},
        'verificacoes':checks,
        'total_ocorrencias_sinalizadas':sum(v['quantidade'] for v in checks.values()),
        'nota':'Ocorrências podem se sobrepor. Zeros em estatísticas de jogo podem ser válidos; inconsistências devem ser verificadas antes de excluir registros.',
        'missing_tests':{'Little MCAR':'Não aplicável: não há ausências no recorte.', 'Jamshidian–Jalal':'Não aplicável: não há padrões de ausência.', 'Listing–Schlittgen (LS)':'Não aplicável: não há padrões de ausência.', 'Regressão logística para indicador de ausência':'Não estimável: indicador de ausência constante (zero).'}
    }
