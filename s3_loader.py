import requests
import os
import boto3
from io import BytesIO
import pandas as pd
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

AWS_CONFIG = {
    'aws_access_key_id': os.getenv('AWS_ACCESS_KEY_ID'),
    'aws_secret_access_key': os.getenv('AWS_SECRET_ACCESS_KEY'),
    'region_name': os.getenv('AWS_REGION')
}

S3_BUCKET_NAME = os.getenv('S3_BUCKET')

def upload_parquet_to_s3(df: pd.DataFrame):
    try:
        #print("Começando upload para S3")
        print(AWS_CONFIG)
        # Valida credenciais AWS
        if not all([AWS_CONFIG['aws_access_key_id'], 
                  AWS_CONFIG['aws_secret_access_key'], 
                  AWS_CONFIG['region_name']]):
            raise ValueError("Credenciais AWS incompletas")
        
        print("Credenciais validadas")
            
         # Cria buffer de memória
        parquet_buffer = BytesIO()
        
        # Salva DataFrame diretamente no buffer
        df.to_parquet(parquet_buffer, engine='pyarrow', index=False)
        print("Arquivo .parquet salvo")
        
        # Configura cliente S3
        s3 = boto3.client('s3', **AWS_CONFIG)
        print("Conexão com S3 estabelecida")
        
        # Reset do buffer para leitura
        parquet_buffer.seek(0)
        
        # Upload para S3
        s3.upload_fileobj(
            parquet_buffer,
            S3_BUCKET_NAME,
            #f'scada/{pd.Timestamp.now().strftime("%Y-%m-%d")}/dados.parquet'
            f'scada/dados_pressao.parquet'
        )
        print("Upload para S3 concluido.")
        
    except Exception as e:
        print("error", e)


if __name__ == '__main__':

    url = 'http://127.0.0.1:8000/dados_geral'

    response = requests.get(url)
    df = pd.DataFrame(response.json())

    upload_parquet_to_s3(df)