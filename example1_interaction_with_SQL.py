#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 18:11:43 2021

@author: jordanlinaresperez

Backtesting strategies

"""

import pandas as pd #Para DB
import requests #Para comunicarnos con servidores y obtener respuesta
import sqlalchemy as sql #Para acceder a MySQL
import datetime #Para las fechas

# Load TOKEN
# load_dotenv()
# token_mysql = os.getenv('token_mysql')

# Conexión a la base de datos en SQL
token_mysql = 'M1/gammaENalph*1.618033'
engine = sql.create_engine(f"mysql://root:{token_mysql}@localhost:3306/bitso_api")

query = """SELECT *
            FROM bitso_trades;
    """
    
ResultProxy = engine.execute(query)

ResultSet = ResultProxy.fetchall()
df = pd.DataFrame(ResultSet)


