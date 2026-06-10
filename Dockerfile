# 1. Usa uma imagem leve do Python como base
FROM python:3.11-slim

# 2. Define a pasta onde o código vai morar no container
WORKDIR /app

# 3. Instala ferramentas do sistema necessárias
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# 4. Copia os arquivos do seu PC para dentro do container
COPY . .

# 5. Instala as dependências do seu projeto Python
RUN pip3 install -r requirements.txt

# 6. Informa ao Docker que o container vai escutar a porta padrão do Streamlit
EXPOSE 8501

# 7. Adiciona um teste para garantir que o container está saudável
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# 8. Comando oficial para iniciar o Streamlit configurado para a nuvem
ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
