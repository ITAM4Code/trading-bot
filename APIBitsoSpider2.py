import pandas as pd #Para DB
import requests #Para comunicarnos con servidores y obtener respuesta
import sqlalchemy as sql #Para acceder a MySQL
import datetime #Para las fechas
import time #Lo usaremos para pausar el flujo de datos
import os
from dotenv import load_dotenv

#Load TOKEN
load_dotenv()

token_mysql=os.getenv('TOKEN_MYSQL')
#Lo vamos a meter en un ciclo para que lo vaya actualizando

def extract_bitso_api():
    
    response = requests.get('https://api.bitso.com/v3/trades/?book=btc_mxn') #esto lo podemos modificar de acuerdo a la documentacion, dependiendo de los dato que queramos extraer
    #pasamos un json a un dataframe
    json_response =response.json()
    datos = json_response['payload']
    df = pd.DataFrame(datos)
    

    engine = sql.create_engine(f"mysql://root:{token_mysql}@localhost:3306/Bitso_API")
    #'mysql+mysqlconnector://user:password@localhost/db?auth_plugin=mysql_native_password'
    
    

    #Debemos de hacer en modo de query porque SQL no entiende como tal el dataframe
    #La vamos a decir a SQL que va a insertar en "trades" los valores de las columnas
    initial_q = """INSERT INTO bitso_trades
    (book,created_at,amount,maker_side,price,tid)
    VALUES
    """
    #Formamos los 6 espacios de las columnas y las pegamos con format y el nombre de las columnas agregadas
    values_q = ",".join(["""('{}','{}','{}','{}','{}','{}')""".format(
                         row.book,
                         row.created_at,
                         row.amount,
                         row.maker_side,
                         row.price,
                         row.tid) for idx, row in df.iterrows()])
    
    #En la query quiero meter los datos del dataframe, y luego esto lo paso a SQL y lo paso a la tabla
    
    #Para eliminar los datos que puedan estar duplicados en las columnas escribimos lo siguiente
    end_q = """ ON DUPLICATE KEY UPDATE
             book = values(book),
             created_at = values(created_at),
             amount = values(amount),
             maker_side = values(maker_side),
             price = values(price),
             tid = values(tid);"""
                           
    query = initial_q + values_q + end_q
    
    
    #Ahora haremos que SQL ejecute la query
    #mydb.execute(query)
    engine.execute(query)
    
    return None

#Aqui esta el ciclo
while True:
    extract_bitso_api()
    print('Actualizando DataBase a las {}'.format(datetime.datetime.today()))
    time.sleep(15)