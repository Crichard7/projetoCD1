# Projeto 1 — Laboratório de Ciência de Dados — Grupo 1

Análise exploratória das estatísticas por jogo de Los Angeles Lakers e Denver Nuggets, a partir da base `stats_times_regular_final.csv` fornecida para a disciplina.

## Execução (Python 3.10+)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Abra http://localhost:5000 . No Windows, a ativação é `.venv\Scripts\activate`.

## Estrutura

- `app.py`: servidor Flask e endpoints JSON.
- `analytics.py`: preparação, estatísticas e métodos de anomalia.
- `templates/index.html`: relatório web e gráficos Plotly (carregados via CDN; requer internet para os gráficos).
- `data/`: CSV original, preservado.

## Decisões e limites

- Unidade de análise: uma linha por equipe por jogo.
- O recorte mantém as equipes do Grupo 1 e não elimina jogos atípicos.
- `GAME_DATE` vira data; `WL` é 0/1 no arquivo recebido; dados numéricos são convertidos explicitamente.
- Os indicadores são analisados por jogo e por time; não há treino de modelo preditivo.
- Quartis: interpolação linear. Desvio padrão: amostral. Outliers: regra 1,5×IQR.
- A análise de Grubbs testa um único extremo; ECOD implementado como pontuação empírica de caudas em uma dimensão, não a implementação multivariada de biblioteca.
- K-NN, LOF e DBSCAN dependem de parâmetros arbitrados e devem ser interpretados como ferramentas exploratórias.
- O histograma inclui KDE gaussiana, e uma tabela complementar ao boxplot exibe limites, quartis, média, mediana, moda e extremos; os limites e a moda não são desenhados diretamente no boxplot.
- Testes MCAR/MAR/MNAR são discutidos, mas não implementados: não há faltantes nas métricas do recorte, tornando-os não informativos neste caso.
- Recomendado: revisar com o professor a exigência de implementar formalmente testes de missingness mesmo sem ausências observadas.

## API

- `GET /api/overview`: dicionário e qualidade.
- `GET /api/analysis?team=Los%20Angeles%20Lakers&metric=PTS`: medidas, gráficos (dados) e anomalias.
- `GET /api/summary`: matrizes CV, IQR e assimetria.

## Checklist antes da entrega

- [x] Adicionar KDE ao histograma e tabela de apoio ao boxplot.
- [ ] Incluir teste automatizado para medidas e contagem de outliers.
- [ ] Verificar nomenclatura e interpretação dos testes de dados faltantes com referências bibliográficas.
- [ ] Hospedar o projeto ou apresentar execução local conforme a alternativa aceita no enunciado.

## Testes

Após instalar as dependências, execute `python -m unittest discover -s tests -v` na pasta do projeto.


## Versão 4 — Concordância de outliers

A seção **Concordância** reúne os jogos sinalizados pelos sete detectores e mostra quantos métodos identificaram cada observação. Endpoint adicional: `/api/outlier-comparison?team=Los%20Angeles%20Lakers&metric=PTS`. Nenhuma observação é removida.

Execute os testes com `python -m unittest discover -s tests -v`.

## Versão 5 — interpretação crítica de outliers

A seção **Interpretação crítica dos detectores** atualiza-se com a seleção de time e variável. Mostra as contagens por método, três pares com maior índice de Jaccard e uma interpretação contextualizada. O endpoint `GET /api/outlier-interpretation?team=Los%20Angeles%20Lakers&metric=PTS` fornece os mesmos dados em JSON. O índice de Jaccard compara a sobreposição dos conjuntos detectados; não é medida de acurácia, e não há rótulos para avaliação supervisionada.

## Versão 6 — Síntese estatística integrada

A seção **Síntese final** compara Lakers e Nuggets nas sete variáveis e reúne média,
mediana, desvio padrão amostral, coeficiente de variação, quartis, IQR,
assimetria ajustada de Fisher–Pearson e outliers pela regra de Tukey.
A API `GET /api/statistical-synthesis` retorna os mesmos resultados em JSON.
O seletor de variável atualiza a interpretação por equipe. As diferenças são
**descritivas** e não devem ser interpretadas como significância estatística.

Para executar os testes: `python -m unittest discover -s tests -v`.
# projetoCD1
