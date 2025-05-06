# 🚚 pc-frete  

## 📦 Projeto de Frete para E-commerce
Este projeto tem como objetivo representar **a parte de frete** dentro de um sistema de e-commerce. Ele simula a lógica envolvida no cálculo, exibição e gerenciamento do frete de produtos em uma loja virtual.

## 🎯 Objetivo
Construir um módulo independente que lida com tudo relacionado ao frete de pedidos online, de forma integrada e flexível, podendo ser usado em diferentes plataformas de e-commerce.

## 👥 Participantes

- Maria Cecília
- Guilherme Gabriel
- Victor Hugo
- Felipe Andrade

## 💻 Tecnologias
Este projeto foi construído usando várias tecnologias chaves para garantir performance, segurança e facilidade de uso:

* **Python 3.12**: Escolhido por sua simplicidade e poderosas capacidades de programação. A versão 3.13 é a mais recente, oferecendo melhorias significativas em eficiência e recursos linguísticos.
* **FastAPI**: Uma moderna e rápida (altas performances) web framework para Python, que é ideal para a construção de APIs.
* Uvicorn: Utilizado para rodar aplicações web assíncronas em Python.
* Make: (Automação de tarefas no Linux)
* Outras dependências listadas em requirements

## 📦 Clonando o Repositório

git clone https://github.com/projeto-carreira-luizalabs-2025/pc-frete

## ✨ Configuração do ambiente local (Linux 🐧)

Todos os comandos serão via terminal.

Depois de clonar o projeto, acesse o diretório:

```sh
cd pc-frete
```

Crie o [ambiente virtual](https://docs.python.org/3.12/tutorial/venv.html)
para instalar as bibliotecas e trabalharmos com o projeto:

```sh
make build-venv
```

Uma vez criado o ambiente virtual do Python, você precisa ativá-lo

```sh
./venv/bin/activate
```

Quaisquer comandos daqui para frente, iremos considerar que você está dentro
do ambiente virtual `(venv)`.

Instale as bibliotecas necessárias para o seu projeto.

```sh
make requirements-dev
```

## ⭐  Formatação de lint e código

Para executar a validação do lint, execute:
```bash
make lint
```

## ▶️ Execução

1️⃣ Configure o arquivo de env:
```bash
$ cp devtools/dotenv.dev .env
```

2️⃣ Rodar a API
```bash
make run-dev
```
## Acesse a documentação da API:
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/redoc

## Contribuições e Atualizações
O projeto está aberto a contribuições e atualizações da comunidade. O processo para contribuições é o seguinte:

* **Pull Requests**: Contribuições devem ser submetidas como pull requests.
* **Code Review**: Cada pull request passará por um code review detalhado pela equipe. Isso garante que o código esteja alinhado com os padrões de qualidade e funcionamento do projeto.
* **Incorporação de Mudanças**: Após a aprovação no code review, as mudanças serão integradas ao código principal.

## 📖 Recursos úteis

- [Conventional Commits](https://www.conventionalcommits.org)

## 👍 Merge Requests

- Fluxo de desenvolvimento e entrega contínua documentado no Kanban.
