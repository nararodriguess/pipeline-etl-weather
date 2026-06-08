# 🌦️ Pipeline ETL de Dados Meteorológicos

Pipeline ETL para coleta, transformação e armazenamento de dados meteorológicos utilizando a API do OpenWeatherMap, Apache Airflow e PostgreSQL.

---

## 📌 Sobre o Projeto

Este projeto foi desenvolvido como parte do aprendizado prático de Engenharia de Dados, seguindo o tutorial da **[@vbluuiza](https://www.youtube.com/@vbluuiza)**.

O pipeline coleta dados meteorológicos em tempo real da API do OpenWeatherMap, transforma e normaliza os dados com Pandas e os armazena em um banco de dados PostgreSQL — tudo orquestrado pelo Apache Airflow.

---

## 🏗️ Arquitetura

```
OpenWeatherMap API → Extract → Transform → Load → PostgreSQL
                         ↑
                     Apache Airflow (orquestração)
                         ↑
                       Docker
```

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Função |
|---|---|
| Python 3.10+ | Linguagem principal |
| Apache Airflow | Orquestração do pipeline |
| Docker + Docker Compose | Containerização do Airflow |
| PostgreSQL | Banco de dados de destino |
| Pandas | Transformação dos dados |
| SQLAlchemy + psycopg2 | Conexão com o banco de dados |
| OpenWeatherMap API | Fonte dos dados meteorológicos |
| uv | Gerenciador de pacotes Python |

---

## 📁 Estrutura do Projeto

```
pipeline-etl-weather/
├── dags/               # DAG do Airflow (weather_dag.py)
├── src/                # Scripts ETL
│   ├── extract_data.py
│   ├── transform_data.py
│   └── load_data.py
├── data/               # Dados gerados pelo pipeline
├── notebooks/          # Análise exploratória dos dados
├── logs/               # Logs do Airflow
├── config/             # Arquivo .env com credenciais
├── docker-compose.yaml # Orquestração dos containers
└── pyproject.toml      # Configuração do projeto Python
```

---

## ⚙️ Pré-requisitos

- Python 3.10+
- Docker Desktop
- PostgreSQL 14+
- WSL 2 (para usuários Windows)
- Conta ativa no [OpenWeatherMap](https://openweathermap.org) com API Key
- [uv](https://github.com/astral-sh/uv) (gerenciador de pacotes)

---

## 🚀 Como Executar

### 1. Clone o repositório
```bash
git clone https://github.com/nararodriguess/pipeline-etl-weather.git
cd pipeline-etl-weather
```

### 2. Configure o ambiente virtual
```bash
uv venv
source .venv/bin/activate
uv add pandas sqlalchemy psycopg2-binary requests python-dotenv
```

### 3. Configure as credenciais
Crie o arquivo `config/.env` com o seguinte conteúdo:
```
user=seu_usuario
password=sua_senha
database=weather_data
api_key=sua_chave_da_api
```

### 4. Configure o PostgreSQL
```sql
CREATE USER seu_usuario WITH PASSWORD 'sua_senha';
ALTER USER seu_usuario WITH SUPERUSER;
CREATE DATABASE weather_data OWNER seu_usuario;
```

### 5. Suba o Airflow com Docker
```bash
docker compose up -d
```

Acesse a interface do Airflow em: `http://localhost:8080`
- Usuário: `airflow`
- Senha: `airflow`

---

## 📊 Pipeline ETL

- **Extract:** Coleta dados em JSON da API OpenWeatherMap
- **Transform:** Normaliza e limpa os dados com Pandas
- **Load:** Insere os dados no PostgreSQL via SQLAlchemy

---

## 🙏 Créditos

Projeto desenvolvido com base no tutorial de **[@vbluuiza](https://www.youtube.com/@vbluuiza)**:

▶️ [Engenharia de Dados na Prática: Pipeline ETL de dados meteorológicos](https://www.youtube.com/watch?v=I8qPqbXQBDU&t=1170s)

---

## 📝 Licença

Este projeto é de uso educacional.