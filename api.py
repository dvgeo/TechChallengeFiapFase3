from fastapi import FastAPI,status, HTTPException
import psycopg2
from pydantic import BaseModel, Field
from typing import List, Optional
import pandas as pd
import numpy as np  # Adicione esta linha
import os
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

app = FastAPI(
    title="API de Dados de Pressão de Rede",
    description="API para consulta de dados de medidores IOT de pressão de rede em um banco SCADA.",
    version="1.0.0",
    openapi_tags=[{
        'name': 'Sensores',
        'description': 'Endpoints relacionados a dados de pressão de rede'
    }]
)

# Configurações do PostgreSQL
DB_CONFIG = {
    'dbname': os.getenv('POSTGRES_DB_SCADA'),
    'user': os.getenv('POSTGRES_USER_SCADA'),
    'password': os.getenv('POSTGRES_PASSWORD_SCADA'),
    'host': os.getenv('POSTGRES_HOST_SCADA'),
    'port': os.getenv('POSTGRES_PORT_SCADA')
}

class SensorResponse(BaseModel):
    xid: int = Field(..., description="ID único do sensor", example="DP_060785")
    hora: Optional[str] = Field(
        description="hora atual da média do sensor de pressão", 
        example="16"
    )
    data: Optional[str] = Field(
        description="Data da medição do sensor", 
        example="2025-03-25"
    )
    media_hora: Optional[float] = Field(
        description="Média em metros de coluna de água(mca) do sensor de pressão da rede", 
        example=10.91
    )
    desvio_padrao_30_dias: Optional[float] = Field(
        description="Desvio padrão dos valores do sensor de pressão dos últimos 30 dias", 
        example=0.75
    )
    alerta: Optional[str] = Field(
        description="Anormalidade dos valores do sensor", 
        example="Anormal"
    )
    tipo: Optional[str] = Field(
        description="Tipo do sensor: A=água B=esgoto", 
        example="CASA FECHADA"
    )
    latitude: Optional[float] = Field(
        description="Coordenada geográfica latitude", 
        example=-23.5506507
    )
    longitude: Optional[float] = Field(
        description="Coordenada geográfica longitude", 
        example=-46.6333824
    )
    bairro: Optional[str] = Field(
        description="Localização do bairro do setor",
        example="CENTRO"
    )


    class Config:
        schema_extra = {
            "example": {
                "xid": "DP_060785",
                "latitude": -7.111827,
                "longitude": -34.880774,
                "hora": "16",
                "data": "2025-03-25",
                "media_hora": 10.91,
                "media_hora_30_dias": 10.71,
                "desvio_padrao_30_dias": 0.75,
                "alerta": "---",
                "tipo": "A",
                "bairro": "ROGER"
            }
        }

@app.get("/dados_geral",
    response_model=List[SensorResponse],
    tags=["Sensores"],
    summary="Obter dados completos dos sensores de pressão",
    description="Retorna uma lista completa de dados de sensores de pressão com informações de pressão e localização",
    responses={
        status.HTTP_200_OK: {
            "description": "Dados recuperados com sucesso",
            "content": {
                "application/json": {
                    "example": [SensorResponse.Config.schema_extra["example"]]
                }
            }
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Erro na conexão com o banco de dados",
            "content": {
                "application/json": {
                    "example": {"detail": "Erro ao conectar ao banco de dados"}
                }
            }
        }
    }
)
def get_sensor_data():
    """Endpoint para buscar dados dos sensores no PostgreSQL."""
    conn = psycopg2.connect(**DB_CONFIG)
    query = "SELECT xid, latitude, longitude, hora, DATA, media_hora, media_hora_30_dias, desvio_padrao_30_dias, alerta, tipo, CASE when xid = 'DP_231447' then 'MUMBABA' when xid = 'DP_231257' then 'ILHA DO BISPO' when xid = 'DP_115302' then 'PEDRO GONDIM' when xid = 'DP_105134' then 'CENTRO' when xid = 'DP_518969' then 'CABO BRANCO' when xid = 'DP_545010' then 'AEROCLUBE' when xid = 'DP_135022' then 'ALTO DO CEU' when xid = 'DP_098058' then 'ILHA DO BISPO' when xid = 'DP_860257' then 'JARDIM VENEZA' when xid = 'DP_263306' then 'CABO BRANCO' when xid = 'DP_618968' then 'CENTRO' when xid = 'DP_592918' then 'AEROCLUBE' when xid = 'DP_430022' then 'CENTRO' when xid = 'DP_250442' then 'CRISTO REDENTOR' when xid = 'DP_976588' then 'JARDIM OCEANIA' when xid = 'DP_750296' then 'MANGABEIRA' when xid = 'DP_610188' then 'BESSA' when xid = 'DP_873764' then 'VARADOURO' when xid = 'DP_510643' then 'FUNCIONARIOS' when xid = 'DP_770395' then 'BRISAMAR' when xid = 'DP_844270' then 'MUMBABA' when xid = 'DP_911976' then 'MANGABEIRA' when xid = 'DP_688225' then 'JAGUARIBE' when xid = 'DP_489279' then 'VALENTINA' when xid = 'DP_063873' then 'OITIZEIRO' when xid = 'DP_429086' then 'CRISTO REDENTOR' when xid = 'DP_029384' then 'ALTIPLANO CABO BRANCO' when xid = 'DP_075529' then 'JARDIM OCEANIA' when xid = 'DP_020982' then 'MANGABEIRA' when xid = 'DP_797824' then 'MUMBABA' when xid = 'DP_709130' then 'CRUZ DAS ARMAS' when xid = 'DP_060785' then 'ROGER' when xid = 'DP_801635' then 'MUCUMAGRO' when xid = 'DP_959846' then 'CRISTO REDENTOR' when xid = 'DP_540637' then 'CASTELO BRANCO' END AS bairro FROM iot.pressao_rede WHERE data between CURRENT_DATE - INTERVAL '1 year' AND CURRENT_DATE AND xid in ('DP_231447', 'DP_231257', 'DP_115302','DP_105134','DP_518969','DP_545010','DP_135022','DP_098058', 'DP_860257', 'DP_263306', 'DP_618968','DP_592918','DP_430022','DP_250442','DP_976588','DP_750296', 'DP_610188', 'DP_873764', 'DP_510643','DP_770395','DP_844270','DP_911976','DP_688225','DP_489279', 'DP_063873', 'DP_429086', 'DP_029384','DP_075529','DP_020982','DP_797824','DP_709130','DP_060785', 'DP_801635', 'DP_959846')"
    df = pd.read_sql(query, conn)
    conn.close()
    
    # Substituir NaN por None (JSON-compatível)
    df = df.replace({np.nan: None})
    
    return df.to_dict(orient="records")


    

@app.get("/dados_dia",
    response_model=List[SensorResponse],
    tags=["Sensores"],
    summary="Obter dados diário dos sensores de pressão",
    description="Retorna uma lista completa de dados diários dos sensores de pressão com informações de pressão e localização",
    responses={
        status.HTTP_200_OK: {
            "description": "Dados recuperados com sucesso",
            "content": {
                "application/json": {
                    "example": [SensorResponse.Config.schema_extra["example"]]
                }
            }
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Erro na conexão com o banco de dados",
            "content": {
                "application/json": {
                    "example": {"detail": "Erro ao conectar ao banco de dados"}
                }
            }
        }
    }
)
def get_sensor_data():
    """Endpoint para buscar dados dos sensores no PostgreSQL."""
    conn = psycopg2.connect(**DB_CONFIG)
    query = "SELECT xid, latitude, longitude, hora, DATA, media_hora, media_hora_30_dias, desvio_padrao_30_dias, alerta, tipo, CASE when xid = 'DP_231447' then 'MUMBABA' when xid = 'DP_231257' then 'ILHA DO BISPO' when xid = 'DP_115302' then 'PEDRO GONDIM' when xid = 'DP_105134' then 'CENTRO' when xid = 'DP_518969' then 'CABO BRANCO' when xid = 'DP_545010' then 'AEROCLUBE' when xid = 'DP_135022' then 'ALTO DO CEU' when xid = 'DP_098058' then 'ILHA DO BISPO' when xid = 'DP_860257' then 'JARDIM VENEZA' when xid = 'DP_263306' then 'CABO BRANCO' when xid = 'DP_618968' then 'CENTRO' when xid = 'DP_592918' then 'AEROCLUBE' when xid = 'DP_430022' then 'CENTRO' when xid = 'DP_250442' then 'CRISTO REDENTOR' when xid = 'DP_976588' then 'JARDIM OCEANIA' when xid = 'DP_750296' then 'MANGABEIRA' when xid = 'DP_610188' then 'BESSA' when xid = 'DP_873764' then 'VARADOURO' when xid = 'DP_510643' then 'FUNCIONARIOS' when xid = 'DP_770395' then 'BRISAMAR' when xid = 'DP_844270' then 'MUMBABA' when xid = 'DP_911976' then 'MANGABEIRA' when xid = 'DP_688225' then 'JAGUARIBE' when xid = 'DP_489279' then 'VALENTINA' when xid = 'DP_063873' then 'OITIZEIRO' when xid = 'DP_429086' then 'CRISTO REDENTOR' when xid = 'DP_029384' then 'ALTIPLANO CABO BRANCO' when xid = 'DP_075529' then 'JARDIM OCEANIA' when xid = 'DP_020982' then 'MANGABEIRA' when xid = 'DP_797824' then 'MUMBABA' when xid = 'DP_709130' then 'CRUZ DAS ARMAS' when xid = 'DP_060785' then 'ROGER' when xid = 'DP_801635' then 'MUCUMAGRO' when xid = 'DP_959846' then 'CRISTO REDENTOR' when xid = 'DP_540637' then 'CASTELO BRANCO' END AS bairro FROM iot.pressao_rede WHERE data = CURRENT_DATE AND hora = (select max(hora) from iot.pressao_rede WHERE data = CURRENT_DATE) AND xid in ('DP_231447', 'DP_231257', 'DP_115302','DP_105134','DP_518969','DP_545010','DP_135022','DP_098058', 'DP_860257', 'DP_263306', 'DP_618968','DP_592918','DP_430022','DP_250442','DP_976588','DP_750296', 'DP_610188', 'DP_873764', 'DP_510643','DP_770395','DP_844270','DP_911976','DP_688225','DP_489279', 'DP_063873', 'DP_429086', 'DP_029384','DP_075529','DP_020982','DP_797824','DP_709130','DP_060785', 'DP_801635', 'DP_959846')"
    df = pd.read_sql(query, conn)
    conn.close()
    
    # Substituir NaN por None (JSON-compatível)
    df = df.replace({np.nan: None})
    
    return df.to_dict(orient="records")



