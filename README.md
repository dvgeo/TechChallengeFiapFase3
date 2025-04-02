# FIAP Tech Challenge Fase 3 - API para Monitoramento de Pressão em Redes Hidráulicas, Modelo de Machine Learning para Detecção de Anomalias e Aplicação Streamlit com Modelo Treinado 

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![AWS S3](https://img.shields.io/badge/Amazon_S3-569A31?style=for-the-badge&logo=amazon-s3&logoColor=white)
![Google Colab](https://img.shields.io/badge/Colab-F9AB00?style=for-the-badge&logo=googlecolab&color=525252)

API para coleta de dados de sensores *Internet of Things*(*IOT*) de pressão em redes de água medidos em metros de coluna d'água (mca) de um banco de dados PostgreSQL com armazenamento no datalake S3 AWS e treinamento de modelo de machine learning desenvolvido como parte do **FIAP Tech Challenge Fase 3** da pós-graduação em Machine Learning Engineering.

## 👨‍💻👨‍💻 Autores
- *Diego Varela* **rm359642** 
- *Vagner Fábio* **rm358795** 

## 📋 Visão Geral do Projeto

### Contexto do Projeto
Desenvolvido como parte do programa de pós-graduação da FIAP, este projeto integra:
- **API FastAPI**: Para monitoramento em tempo real
- **Armazenamento em Nuvem**: Dados históricos no AWS S3
- **Machine Learning**: Modelos preditivos para detecção de anomalias

## ✨ Principais Funcionalidades

### API
- Consulta de dados históricos (último ano)
- Dados do dia corrente
- Geolocalização dos sensores
- Estatísticas de medições (médias e desvios padrão)
- Sistema de alertas de anomalias

### Arquitetura Integrada
1. **Coleta de Dados**: Sensores IoT enviando dados para PostgreSQL
2. **API de Consulta**: FastAPI para acesso aos dados Postgresql
3. **Armazenamento Cloud**: Script python para armazenamento de dados consolidados em Parquet na AWS S3
4. **Análise Preditiva**: Modelos ML treinados no Google Colab

## 🚀 Instalação

## 1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/repositorio.git
cd repositorio
```
## 2. Crie e ative o ambiente virtual:

```
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate  # Windows
```

## 3. Instale as dependências:

```
pip install -r requirements.tx
```

## 4. Crie um arquivo .env na raiz do projeto com as seguintes variáveis:
## ⚙ Configuração

```
Configurações PostgreSQL 
POSTGRES_DB_SCADA=nome_banco
POSTGRES_USER_SCADA=usuario
POSTGRES_PASSWORD_SCADA=senha
POSTGRES_HOST_SCADA=host
POSTGRES_PORT_SCADA=porta

Configurações AWS
AWS_ACCESS_KEY_ID=sua_chave
AWS_SECRET_ACCESS_KEY=sua_secreta
S3_BUCKET=meu-bucket
```

## 5. Execute a API FastAPI:

```
uvicorn main:app --reload
```

## 📚 Documentação da API
Endpoints disponíveis
### 1. Dados Gerais


http

`GET /dados_geral`

Retorna dados históricos dos últimos 12 meses

**Parâmetros**:

Nenhum

**Exemplo de Resposta**:

```bash
JSON
[
  {
    "xid": "DP_060785",
    "hora": "16",
    "data": "2025-03-25",
    "media_hora": 10.91,
    "desvio_padrao_30_dias": 0.75,
    "alerta": "Anormal",
    "tipo": "A",
    "latitude": -7.5506507,
    "longitude": -35.9333824,
    "bairro": "ROGER"
  }
]
```
### 2. Dados do Dia

http

`GET /dados_dia`

Retorna dados da última hora registrada do dia corrente

**Parâmetros**:

Nenhum

**Resposta**:

```bash
JSON
[
  {
    "xid": "DP_060785",
    "hora": "16",
    "data": "2025-03-31",
    "media_hora": 14.11,
    "desvio_padrao_30_dias": 0.78,
    "alerta": "Anormal",
    "tipo": "A",
    "latitude": -7.524874,
    "longitude": -35.845154,
    "bairro": "MANGABEIRA"
  }
]
```
## Acesse a documentação interativa:

- Swagger UI: `http://localhost:8000/docs`

- Redoc: `http://localhost:8000/redoc`

## 🔄 6. Integração com S3
O script `s3_loader.py` realiza as seguintes operações:

1. Conecta ao bucket S3 configurado.

2. Carrega arquivo Parquet no bucket AWS S3 na pasta `scada/dados_pressao.parquet`

## 🔄 7. Pipeline de Machine Learning para Detecção de Anomalias em Dados SCADA

Este modelo de machine learning realiza a detecção de comportamentos anômalos em sensores de pressão, utilizando dados históricos armazenados em um bucket S3 no formato Parquet. O pipeline inclui o pré-processamento, treinamento de um modelo de Machine Learning (XGBoost), e um dashboard interativo com Streamlit para visualização e predição em tempo real.

---

## 📁 Estrutura do Projeto

- `treinar_modelo_alerta.py` → script de treinamento do modelo com dados reais e sintéticos
- `dashboard.py` → aplicação com Streamlit para predição com o modelo treinado
- `modelo_alerta_xgboost_sintetico.pkl` → modelo salvo após o treinamento

---

## 🔍 Descrição do Treinamento (`treinar_modelo_alerta.py`)

1. **Coleta de dados** do S3 (`.parquet`) com autenticação segura.
2. **Limpeza** de valores nulos e negativos.
3. **Engenharia de features**:
   - `dif_media = media_hora - media_hora_30_dias`
   - `media_hora_relativa = media_hora / (media_hora_30_dias + 1)`
4. **Geração de dados sintéticos** de alerta para balancear a base.
5. **Treinamento com XGBoost**, utilizando `scale_pos_weight` para lidar com desbalanceamento.
6. **Avaliação com métricas** de classificação.
7. **Salvamento do modelo** com `joblib`.

---

## 📊 Aplicação(`app.py`)

- Leitura do modelo `.pkl`
- Interface para entrada de dados manuais ou via API
- Predição do alerta com base nas variáveis de entrada
- Exibição do resultado de forma clara e responsiva

---

## ▶️ Como Executar

### 1. Instalar dependências:

```bash
pip install -r requirements.txt
```

Ou diretamente:

```bash
pip install pandas numpy scikit-learn matplotlib seaborn fastapi uvicorn joblib streamlit imbalanced-learn s3fs pyarrow xgboost
```

### 2. Treinar o modelo (opcional):

```bash
python treinar_modelo_alerta.py
```

### 3. Rodar o Aplicativo:

```bash
streamlit run app.py
```

---

## 📦 Requisitos

- Python 3.8+
- Acesso à AWS com credenciais válidas no Colab ou ambiente local
- Streamlit para rodar o dashboard


