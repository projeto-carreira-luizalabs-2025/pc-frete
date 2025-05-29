# Usa uma imagem base oficial do Python
FROM python:3.12-slim AS constructor

SHELL ["/bin/bash", "-c"]

# Define o diretório de trabalho
WORKDIR /pc-frete

# Copia arquivo de dependências
COPY ./requirements/develop.txt .

# Copia pasta de dependências que possui base.txt
COPY requirements/ requirements/

# Instala as dependências do projeto    
RUN python -m venv venv && \
  venv/bin/pip install --upgrade pip && \
  venv/bin/pip install --no-cache-dir -r ./requirements/develop.txt
  
# Imagem final a ser entregue / conterá a minha aplicação
FROM python:3.12-slim
ENV PATH=/pc-frete/venv/bin:$PATH

# Setando variável ambiente como "dev"
ENV ENV=dev

WORKDIR /pc-frete
COPY --from=constructor /pc-frete/venv /pc-frete/venv

# Verifica se o ambiente virtual foi criado corretamente
RUN /pc-frete/venv/bin/python --version

# Copia o código fonte da aplicação
COPY app /pc-frete/app
COPY ./requirements/develop.txt /pc-frete

RUN python -m compileall app

# Executável padrão
CMD [ "uvicorn", "app.api_main:app", "--host", "0.0.0.0", "--port", "8000" ]

# Build
# docker build -f ./devtools/docker/Dockerfile -t pc/frete .
# Execução
# docker run --rm -p 8000:8000 pc/frete