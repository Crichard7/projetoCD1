# Utiliza a versão do Python 3.10 em sua variante mais leve
FROM python:3.10-slim

# Define o diretório dentro do container
WORKDIR /app

# Copia o arquivo de dependências
COPY requirements.txt .

# Instala as dependências listadas no requirements.txt sem manter o cache
RUN pip install --no-cache-dir -r requirements.txt

# Copia todos os arquivos do projeto (app.py, analytics.py, pastas data e templates)
COPY . .

# Indica que o serviço será disponibilizado na porta 5000
EXPOSE 5000

# Executa o servidor Flask forçando a escuta em todas as interfaces de rede (0.0.0.0)
CMD ["flask", "--app", "app.py", "run", "--host=0.0.0.0", "--port=5000"]