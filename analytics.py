from re import sub

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.neighbors import LocalOutlierFactor, NearestNeighbors
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

TEAMS = ['Los Angeles Lakers', 'Denver Nuggets']
METRICS = {'PTS':'Pontos','REB':'Rebotes','AST':'Assistências','STL':'Roubos de bola','BLK':'Tocos','PF':'Faltas pessoais','FG3M':'Cestas de 3 pontos'}
RENAME = {
    'TEAM_NAME': 'time',
    'GAME_DATE': 'data_jogo',
    'Game_ID': 'id_jogo',
    'MATCHUP': 'confronto',
    'WL': 'vitoria'
}

def load_data(path):
    raw = pd.read_csv(path)
    df = raw[raw['TEAM_NAME'].isin(TEAMS)].copy()
    df['GAME_DATE'] = pd.to_datetime(df['GAME_DATE'], errors='coerce')
    df['WL'] = pd.to_numeric(df['WL'], errors='coerce')
    for c in METRICS:
        df[c] = pd.to_numeric(df[c], errors='coerce')
    df = df.rename(columns=RENAME)
    return raw, df

def describe(df, team, metric):
    x = df.loc[df.time == team, metric].dropna().astype(float)
    if x.empty: return None
    q1,q3 = np.quantile(x,[.25,.75],method='linear'); iqr=q3-q1
    low,high=q1-1.5*iqr,q3+1.5*iqr
    out=x[(x<low)|(x>high)]
    modes=x.mode()
    sd=x.std(ddof=1)
    skew=float(stats.skew(x,bias=False)) if len(x)>2 and sd>0 else None
    return {'n':len(x),'media':x.mean(),'mediana':x.median(),'moda':modes.tolist(), 'minimo':x.min(),'maximo':x.max(),'amplitude':x.max()-x.min(),'desvio':sd,'variancia':x.var(ddof=1),'q1':q1,'q3':q3,'iqr':iqr,'limite_inferior':low,'limite_superior':high,'outliers':out.tolist(),'outlier_count':len(out),'assimetria':skew,'cv':100*sd/x.mean() if x.mean()>0 else None}

def quality(raw, df):
    return {'original_shape':list(raw.shape),'filtered_shape':list(df.shape),'missing_original':raw.isna().sum().to_dict(),'missing_group':df.isna().sum().to_dict(),'duplicates_original':int(raw.duplicated().sum()),'duplicates_group':int(df.duplicated().sum()),'negative_metrics':{m:int((df[m]<0).sum()) for m in METRICS},'dates_invalid':int(df.data_jogo.isna().sum()),'team_counts':df.time.value_counts().to_dict()}

def detectors(df, team, metric):
    sub=df[df.time==team].dropna(subset=[metric]).copy(); x=sub[metric].to_numpy(dtype=float)
    if len(x)<5: return {'error':'Amostra insuficiente'}
    res={}; mu=x.mean(); sd=x.std(ddof=1)
    res['Z-score (|z| > 3)']=np.flatnonzero(abs((x-mu)/sd)>3).tolist() if sd>0 else []
    q1,q3=np.quantile(x,[.25,.75]); iq=q3-q1
    res['IQR (1,5×)']=np.flatnonzero((x<q1-1.5*iq)|(x>q3+1.5*iq)).tolist()
    # Grubbs iterativo: aplica-se uma vez ao extremo mais distante, sob hipótese de normalidade.
    if sd>0 and len(x)>2:
        n=len(x); g=np.max(np.abs(x-mu))/sd; t=stats.t.ppf(1-.05/(2*n),n-2)
        crit=(n-1)/np.sqrt(n)*np.sqrt(t*t/(n-2+t*t))
        res['Grubbs (α=0,05; um extremo)']=[int(np.argmax(abs(x-mu)))] if g>crit else []
    else: res['Grubbs (α=0,05; um extremo)']=[]
    # ECOD univariado: caudas empíricas; quantil superior de pontuação como limiar operacional.
    ranks=pd.Series(x).rank(method='average').to_numpy(); left=ranks/(len(x)+1);right=(len(x)+1-ranks)/(len(x)+1)
    score=-np.log(np.minimum(left,right)); threshold=np.quantile(score,.95)
    res['ECOD empírico (5% maiores escores)']=np.flatnonzero(score>threshold).tolist()
    X=StandardScaler().fit_transform(x.reshape(-1,1)) if sd>0 else np.zeros((len(x),1))
    k=min(5,len(x)-1)
    distances=NearestNeighbors(n_neighbors=k+1).fit(X).kneighbors(X)[0][:,-1]
    res['K-NN (5% maiores distâncias)']=np.flatnonzero(distances>np.quantile(distances,.95)).tolist()
    labels=DBSCAN(eps=.5,min_samples=5).fit_predict(X)
    res['DBSCAN (ruído)']=np.flatnonzero(labels==-1).tolist()
    lof=LocalOutlierFactor(n_neighbors=min(20,len(x)-1),contamination=.05)
    res['LOF (contaminação 5%)']=np.flatnonzero(lof.fit_predict(X)==-1).tolist()
    return {name:{'quantidade':len(indices),'valores':[float(x[i]) for i in indices],'datas':[str(sub.iloc[i].data_jogo.date()) for i in indices], 'jogos':[{'id':str(sub.iloc[i].id_jogo),'data':str(sub.iloc[i].data_jogo.date()),'valor':float(x[i])} for i in indices]} for name,indices in res.items()}

def dictionary(raw):
    desc={'Team_ID':'Identificador da equipe','Game_ID':'Identificador do jogo','GAME_DATE':'Data do jogo','MATCHUP':'Confronto e mando de quadra','WL':'Indicador de vitória (1) ou derrota (0)','W':'Vitórias acumuladas','L':'Derrotas acumuladas','W_PCT':'Proporção de vitórias','MIN':'Minutos jogados','FGM':'Arremessos de quadra convertidos','FGA':'Arremessos de quadra tentados','FG_PCT':'Aproveitamento de arremessos de quadra','FG3M':'Cestas de três convertidas','FG3A':'Arremessos de três tentados','FG3_PCT':'Aproveitamento de três pontos','FTM':'Lances livres convertidos','FTA':'Lances livres tentados','FT_PCT':'Aproveitamento de lances livres','OREB':'Rebotes ofensivos','DREB':'Rebotes defensivos','REB':'Rebotes totais','AST':'Assistências','STL':'Roubos de bola','BLK':'Bloqueios','TOV':'Perdas de bola','PF':'Faltas pessoais','PTS':'Pontos marcados','TEAM_NAME':'Nome da equipe'}
    return [{'coluna':c,'tipo':str(raw[c].dtype),'descricao':desc.get(c,'Não documentado'),'ausentes':int(raw[c].isna().sum())} for c in raw.columns]
