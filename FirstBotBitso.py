#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  2 19:46:18 2021

@author: fernando
"""


import time
import hmac
import hashlib
import requests
import json
import os
from dotenv import load_dotenv


#Load TOKEN
load_dotenv()
token_bitso=os.getenv('TOKEN_BITSO')
token_bitso_key=os.getenv('BITSO_KEY')

#Vamos acceder a la API Privada

bitso_key = token_bitso_key#Clave API
bitso_secret = token_bitso  #API key
http_method = "GET" # Change to POST si queremos mandar una ORDEN por ejemplo
#El get es para pedir cosas y el POST para enviar.
request_path = "/v3/balance/"
parameters = {}     # Needed for POST endpoints requiring data

# Create signature
nonce =  str(int(round(time.time() * 1000)))
message = nonce+http_method+request_path
if (http_method == "POST"):
  message += json.dumps(parameters)
signature = hmac.new(bitso_secret.encode('utf-8'),
                                            message.encode('utf-8'),
                                            hashlib.sha256).hexdigest()

# Build the auth header
auth_header = 'Bitso %s:%s:%s' % (bitso_key, nonce, signature)

# Send request
if (http_method == "GET"):
  response = requests.get("https://api.bitso.com" + request_path, headers={"Authorization": auth_header})
elif (http_method == "POST"):
  response = requests.post("https://api.bitso.com" + request_path, json = parameters, headers={"Authorization": auth_header})

print (response.content)

#------------------------//---------------------------
#------------------------//---------------------------
#------------------------//---------------------------


#Ya que entramos a la API vamos a aprender ha poner una ORDEN en Bitso

http_method = "POST" # Change to POST si queremos mandar una ORDEN por ejemplo
#El get es para pedir cosas y el POST para enviar.
#Vamos a mandar una ORDEN
request_path = "/v3/orders/"
#Ponemos los palametros, (podemos ver la documentacion https://bitso.com/api_info#place-an-order)
#book es la moneda, side es si vendes o compras, type es el tipo de la operacion,
#major es la moneda principal y price el precio al que la quieres comprar o vender
parameters = {'book':'btc_mxn','side':'sell','type':'limit','major':'0.0007','price':'1300000'}     # Needed for POST endpoints requiring data

# Create signature
nonce =  str(int(round(time.time() * 1000)))
message = nonce+http_method+request_path
if (http_method == "POST"):
  message += json.dumps(parameters)
signature = hmac.new(bitso_secret.encode('utf-8'),
                                            message.encode('utf-8'),
                                            hashlib.sha256).hexdigest()

# Build the auth header
auth_header = 'Bitso %s:%s:%s' % (bitso_key, nonce, signature)

# Send request
if (http_method == "GET"):
  response = requests.get("https://api.bitso.com" + request_path, headers={"Authorization": auth_header})
elif (http_method == "POST"):
  response = requests.post("https://api.bitso.com" + request_path, json = parameters, headers={"Authorization": auth_header})

print (response.content)


#-------Para borrar la orden--tenemos que---------------//---------------------------
#-----------quitar el codigo de arriba que crea una orden-------------//---------------------------
#------------------------//---------------------------

#Ahora vamos a CANCELAR UNA ORDEN. 
#Para cancelar una orden necesitamos el oid del ALTA de la ORDEN
#En este caso cancelaremos el de la orden anterior {"oid":"SgX8Yos1Q4kn4zTW"}


http_method = "DELETE" # Change to DELETE si queremos eliminar una ORDEN 
#Aqui ponemos el oid
request_path = "/v3/orders/lQ39F09gKDUboD6E"
#Ponemos los palametros, (podemos ver la documentacion https://bitso.com/api_info#place-an-order)
#book es la moneda, side es si vendes o compras, type es el tipo de la operacion,
#major es la moneda principal y price el precio al que la quieres comprar o vender
parameters = {}     # Needed for POST endpoints requiring data

# Create signature
nonce =  str(int(round(time.time() * 1000)))
message = nonce+http_method+request_path
if (http_method == "POST"):
  message += json.dumps(parameters)
signature = hmac.new(bitso_secret.encode('utf-8'),
                                            message.encode('utf-8'),
                                            hashlib.sha256).hexdigest()

# Build the auth header
auth_header = 'Bitso %s:%s:%s' % (bitso_key, nonce, signature)

# Send request
if (http_method == "GET"):
    response = requests.get("https://api.bitso.com" + request_path, headers={"Authorization": auth_header})
elif (http_method == "POST"):
    response = requests.post("https://api.bitso.com" + request_path, json = parameters, headers={"Authorization": auth_header})
#Aqui agregamos un DELETE
elif (http_method == "DELETE"):
    response = requests.delete("https://api.bitso.com" + request_path, headers={"Authorization": auth_header})

print (response.content)

