# 🚚 pc-frete

## 📦 Projeto de Frete para E-commerce

Este projeto representa o **módulo de frete** de um sistema de e-commerce. Ele simula a lógica envolvida no cálculo, exibição e gerenciamento do frete de produtos em uma loja virtual.

## 🎯 Objetivo

Desenvolver um módulo independente e reutilizável para lidar com o frete de pedidos online, de forma flexível e integrada a diferentes plataformas.

## 👥 Participantes

* Maria Cecília
* Guilherme Gabriel
* Victor Hugo
* Felipe Andrade

## 💻 Tecnologias

Este projeto utiliza tecnologias modernas para garantir performance, segurança e escalabilidade:

* **Python 3.12**
* **FastAPI**: Framework moderno e rápido para construção de APIs.
* **Uvicorn**: Servidor ASGI leve e rápido.
* **Make**: Automatização de tarefas.
* **SonarQube**: Ferramenta de análise estática de código.
* **MongoDB**: Banco de dados No-SQL baseado em documentos.
* Outras dependências listadas em `requirements`.

---

## 🚀 Clonando o Repositório

```bash
git clone https://github.com/projeto-carreira-luizalabs-2025/pc-frete
cd pc-frete
```

---

## 🛠️ Configuração do Ambiente Local (Linux)

1. Crie o ambiente virtual:

   ```bash
   make build-venv
   ```

2. Ative o ambiente virtual:

   ```bash
   source venv/bin/activate
   ```

3. Instale as dependências:

   ```bash
   make requirements-dev
   ```

---

## ✨ Lint e Formatação de Código

Para validar o lint:

```bash
make lint
```

---

## ▶️ Execução da API

1. Copie o arquivo `.env`:

   ```bash
   cp devtools/dotenv.dev .env
   ```

2. Rode o servidor:

   ```bash
   make run-dev
   ```

3. Acesse a documentação:

   * Swagger: [http://localhost:8000/api/docs](http://localhost:8000/api/docs)
   * ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🐳 SonarQube com Docker

1. Suba o SonarQube:

   ```bash
   sudo docker-compose -f ./devtools/docker/docker-compose-sonar.yml up
   ```

2. Acesse o SonarQube em: [http://localhost:9000](http://localhost:9000) com login admin e senha admin:

4. Crie um **token de autenticação** no seu perfil. http://localhost:9000/account/security

5. Copie o token gerado e adicione no arquivo `sonar-project.properties`:

   ```properties
   sonar.login=<seu_token_aqui>
   ```

6. Instale o SonarScanner CLI manualmente:

   ```bash
   wget https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-5.0.1.3006-linux.zip
   unzip sonar-scanner-cli-5.0.1.3006-linux.zip
   export PATH="$PWD/sonar-scanner-5.0.1.3006-linux/bin:$PATH"
   ```

5. Execute a análise:

   ```bash
   sonar-scanner
   ```

---

## 🐳 Build e Execução via Docker

### Build da imagem

```bash
sudo docker build -f ./devtools/docker/Dockerfile -t pc/frete .
```

### Rodar a aplicação

```bash
sudo docker run --rm -p 8000:8000 pc/frete
```

---

## 💡 Recursos Úteis

* [Conventional Commits](https://www.conventionalcommits.org)

---

## 👍 Contribuições

* Contribuições devem ser feitas via **Pull Request**.
* Todo PR passará por **Code Review** pela equipe.
* Após aprovação, as mudanças serão integradas ao repositório principal.