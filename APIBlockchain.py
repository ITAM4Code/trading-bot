#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 14:26:31 2021

@author: fernando
"""

import pandas as pd
import requests 
import time

url_list = ['https://api.blockchain.info/charts/total-bitcoins?timespan=all&format=json',
            'https://api.blockchain.info/charts/avg-block-size?timespan=all&format=json',
            'https://api.blockchain.info/charts/difficulty?timespan=all&format=json',
            'https://api.blockchain.info/charts/hash-rate?timespan=all&format=json',
            'https://api.blockchain.info/charts/transaction-fees?timespan=all&format=json',
            'https://api.blockchain.info/charts/n-unique-addresses?timespan=all&format=json',
            'https://api.blockchain.info/charts/n-transactions?timespan=all&format=json',
            'https://api.blockchain.info/charts/transactions-per-second?timespan=all&format=json',
            'https://api.blockchain.info/charts/mempool-count?timespan=all&format=json',
            'https://api.blockchain.info/charts/mempool-size?timespan=all&format=json',
            'https://api.blockchain.info/charts/output-volume?timespan=all&format=json']

url_list_short = ['https://api.blockchain.info/charts/total-bitcoins',
                  'https://api.blockchain.info/charts/avg-block-size',
                  'https://api.blockchain.info/charts/difficulty',
                  'https://api.blockchain.info/charts/hash-rate',
                  'https://api.blockchain.info/charts/transaction-fees',
                  'https://api.blockchain.info/charts/n-unique-addresses',
                  'https://api.blockchain.info/charts/n-transactions',
                  'https://api.blockchain.info/charts/transactions-per-second',
                  'https://api.blockchain.info/charts/mempool-count',
                  'https://api.blockchain.info/charts/mempool-size',
                  'https://api.blockchain.info/charts/output-volume']

#MOSTRAR FUNCIONAMIENTO PARA UNA URL
#url = url_list_short[0]

def load_blockchain_data(url):
    payload = {'timespan': 'all','format':'json'}
    response = requests.get(url, params = payload)
    data = response.json()
    df = pd.DataFrame(data['values'])
    df.rename(columns = {'y':data['name']},inplace=True)
    print(data['name'])
    df['x'] = pd.to_datetime(df['x'],unit='s',)
    df['timestamp'] = df['x'].dt.strftime('%Y-%m-%d')
    df.drop('x',inplace=True,axis=1)
    return df

def join_dataframes(url_list):
    today = pd.Timestamp.today()
    index = pd.date_range(start='2020-01-01',end=today)
    str_index = list(index.strftime('%Y-%m-%d'))
    df_empty = pd.DataFrame({'timestamp':str_index})
    
    for url in url_list:
        df_temp = load_blockchain_data(url)
        time.sleep(5)
        df_empty = df_empty.merge(df_temp, on= 'timestamp', how = 'left')
    return df_empty
        
df_final = join_dataframes(url_list_short)      
 
#Pendiente pasar a SQL por los nan      
        
engine = sql.create_engine(f"mysql://root:{token_mysql}@localhost:3306/Blockchain_API")
    #'mysql+mysqlconnector://user:password@localhost/db?auth_plugin=mysql_native_password'
    
    

    #Debemos de hacer en modo de query porque SQL no entiende como tal el dataframe
    #La vamos a decir a SQL que va a insertar en "trades" los valores de las columnas
    initial_q = """INSERT INTO datos_blockchain
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
        
        
        
        
        
        
        
        
        
    