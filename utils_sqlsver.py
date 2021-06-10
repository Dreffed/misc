import sqlalchemy
import pyodbc 
import logging

logger = logging.getLogger(__name__)

def get_db(config):
    
    conn = None
    try:
        conn = pyodbc.connect('DRIVER={{driver}};SERVER={server};DATABASE={database};UID={username};PWD={password}'.format(**config))
    except Exception as ex:
        logger.error(ex)
    
    return conn

def get_dbengine(config):
    
    conn = None
    try:
        engine = pyodbc.connect('mssql+pyodbc://{username}:{password}@{server}/{database}?driver=SQL+Server'.format(**config))
    except Exception as ex:
        logger.error(ex)
    
    return engine



