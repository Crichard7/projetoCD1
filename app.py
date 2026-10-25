from flask import Flask, render_template, request, jsonify
from pathlib import Path
import pandas as pd
import numpy as np
from scipy.stats import gaussian_kde
from data_quality import audit
from outlier_interpretation import interpret_outliers
from statistical_synthesis import synthesize
from analytics import TEAMS, METRICS, load_data, describe, quality, detectors, dictionary

app=Flask(__name__)
raw,df=load_data(Path(__file__).parent/'data/stats_times_regular_final.csv')

def clean(obj):
    if isinstance(obj,dict):return {str(k):clean(v) for k,v in obj.items()}
    if isinstance(obj,list):return [clean(v) for v in obj]
    if isinstance(obj,tuple):return [clean(v) for v in obj]
    if isinstance(obj,pd.Timestamp):return obj.isoformat()
    if hasattr(obj,'item'):return clean(obj.item())
    if isinstance(obj,float) and (pd.isna(obj) or obj==float('inf')):return None
    return obj

@app.route('/')
def index():return render_template('index.html',teams=TEAMS,metrics=METRICS)

@app.route('/api/overview')
def overview():
    return jsonify(clean({'quality':quality(raw,df),'dictionary':dictionary(raw),'teams':TEAMS,'metrics':METRICS}))

@app.route('/api/data-quality')
def data_quality():
    return jsonify(clean(audit(raw)))

@app.route('/api/analysis')
def analysis():
    metric=request.args.get('metric','PTS');team=request.args.get('team',TEAMS[0])
    if metric not in METRICS or team not in TEAMS:return jsonify({'error':'Filtro inválido'}),400
    results={t:describe(df,t,metric) for t in TEAMS}
    rows=[]
    for t in TEAMS:
        sub=df[df.time==t].sort_values('data_jogo')
        rows.extend([{'time':t,'data':r.data_jogo.strftime('%d/%m/%Y') if pd.notna(r.data_jogo) else '', 'valor':float(getattr(r,metric))} for r in sub.itertuples() if pd.notna(getattr(r,metric))])
    values=df.loc[df.time==team,metric].dropna().to_numpy(dtype=float)
    kde=None
    if len(values)>2 and np.std(values)>0:
        try:
            xx=np.linspace(max(0,float(values.min())-2),float(values.max())+2,180)
            yy=gaussian_kde(values)(xx)
            kde={'x':xx.tolist(),'y':yy.tolist()}
        except (ValueError,np.linalg.LinAlgError):
            pass
    return jsonify(clean({'metric':metric,'team':team,'results':results,'rows':rows,'detectors':detectors(df,team,metric),'kde':kde}))

@app.route('/api/outlier-comparison')
def outlier_comparison():
    metric=request.args.get('metric','PTS')
    team=request.args.get('team',TEAMS[0])
    if metric not in METRICS or team not in TEAMS:
        return jsonify({'error':'Filtro inválido'}),400
    methods=detectors(df,team,metric)
    sets={name:{j['id'] for j in result['jogos']} for name,result in methods.items()}
    union=set().union(*sets.values())
    records=[]
    for game_id in sorted(union):
        matches=[name for name,ids in sets.items() if game_id in ids]
        row=next(j for result in methods.values() for j in result['jogos'] if j['id']==game_id)
        records.append({**row,'metodos':matches,'consenso':len(matches)})
    records.sort(key=lambda x:(-x['consenso'],x['data']))
    return jsonify(clean({'time':team,'variavel':metric,'metodos':list(methods),
        'quantidade_unica':len(union),'jogos':records,
        'intersecao_total':len(set.intersection(*sets.values())) if sets else 0}))

@app.route('/api/outlier-interpretation')
def outlier_interpretation():
    metric=request.args.get('metric','PTS')
    team=request.args.get('team',TEAMS[0])
    if metric not in METRICS or team not in TEAMS:
        return jsonify({'error':'Filtro inválido'}),400
    return jsonify(clean(interpret_outliers(df,team,metric)))

@app.route('/api/statistical-synthesis')
def statistical_synthesis():
    return jsonify(clean(synthesize(df)))

@app.route('/api/summary')
def summary():
    return jsonify(clean({'cv':{m:{t:describe(df,t,m)['cv'] for t in TEAMS} for m in METRICS},'iqr':{m:{t:describe(df,t,m)['iqr'] for t in TEAMS} for m in METRICS},'skew':{m:{t:describe(df,t,m)['assimetria'] for t in TEAMS} for m in METRICS}}))

if __name__=='__main__':app.run(host='0.0.0.0',port=5000,debug=False)
