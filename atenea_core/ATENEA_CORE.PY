import logging
from logging.handlers import RotatingFileHandler
import datetime
import requests
import caja_fuerte as cf

# CONFIGURACIÓN DEL LOG ROTATIVO (50MB)
LOG_FILENAME = "atenea_bridge.log"
MAX_BYTES = 50 * 1024 * 1024 
BACKUP_COUNT = 100

rotator = RotatingFileHandler(LOG_FILENAME, maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT, encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
rotator.setFormatter(formatter)

logger = logging.getLogger("AteneaCore")
logger.setLevel(logging.INFO)
logger.addHandler(rotator)

def registrar_arranque():
    ahora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info("="*60)
    logger.info(f"ARRANQUE SISTEMA ATENEA - SESIÓN: {ahora}")
    logger.info(f"PROYECTO: {cf.PROJECT_NAME} | AGENTE: {cf.AGENT_NAME}")
    logger.info("="*60)

def consultar_atenea(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{cf.MODEL_NAME}:generateContent?key={cf.GEMINI_KEY}"
    headers = {'Content-Type': 'application/json'}
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        res_json = response.json()
        
        texto = res_json['candidates'][0]['content']['parts'][0]['text']
        uso = res_json.get('usageMetadata', {})
        
        # Log de consumo de tokens (Monitorización del Puente)
        logger.info(f"CONSUMO -> Prompt: {uso.get('promptTokenCount', 0)} | Total: {uso.get('totalTokenCount', 0)}")
        return texto
    except Exception as e:
        logger.error(f"ERROR EN MOTOR ATENEA: {e}")
        return "Socio, algo ha fallado en el motor de Atenea. Revisa el log."