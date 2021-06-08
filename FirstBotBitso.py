#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Jordán
"""
# We define the libraries
import time
import hmac
import hashlib
import requests
import json
import os
from dotenv import load_dotenv

#Load TOKEN
load_dotenv()
bitso_secret=os.getenv('TOKEN_BITSO') #API key
bitso_key=os.getenv('BITSO_KEY')      #Clave API

class bitso_call:
    """The bitso_call class interacts with the bitso api directly. Within you
    will find methods to get the balance of your aacount, place an order, or
    even cancel an order."""


    def __init__(self, bitso_key, bitso_secret):
        """Initialize main attributes of the class."""
        self.bitso_key = bitso_key
        self.bitso_secret = bitso_secret

    def create_signature(self, http_method, request_path, parameters={}):
        """Function which automatically creates a signature and then pass it
        to create an auth header. It is mandatory for our API calls."""

    # Create signature
        nonce =  str(int(round(time.time() * 1000))) # cadena en milisegundos
        message = nonce+http_method+request_path
        if (http_method == "POST"):
            message += json.dumps(parameters)
        signature = hmac.new(self.bitso_secret.encode('utf-8'),
                             message.encode('utf-8'),
                             hashlib.sha256).hexdigest()

        # Build the auth header
        auth_header = 'Bitso %s:%s:%s' % (self.bitso_key, nonce, signature)

        # Send request
        if (http_method == "GET"):
            response = requests.get("https://api.bitso.com" + request_path,
                                    headers={"Authorization": auth_header})
        elif (http_method == "POST"):
            response = requests.post("https://api.bitso.com" + request_path,
                                     json = parameters, headers={"Authorization": auth_header})
        elif (http_method == "DELETE"):
            response = requests.delete("https://api.bitso.com" + request_path,
                                       headers={"Authorization": auth_header})
        return response

    def get_balance(self):
        """Given certain parameters, the function returns an object with the balance
        of our account."""

        http_method = "GET"
        request_path = "/v3/balance/"
        balance = self.create_signature(http_method, request_path)

        print(balance.content)

    def place_order(self, book, side, _type, major, price):
        """Given certain parameters, the function returns a json object representing the order."""

        http_method = "POST"
        request_path = "/v3/orders/"
        parameters = {'book': book,
                      'side': side,
                      'type': _type,
                      'major': major,
                      'price': price}

        order = self.create_signature(http_method, request_path, parameters).json()

        # Access to the json object
        order_status = order["success"]
        oid = order["payload"]["oid"]

        return (order_status, oid)

        # Under development

    def cancel_order(self, oid):
        """The function returns a json object which contains a list of the
        cancelation Order IDs."""

        http_method = "DELETE" # Change to POST if endpoint requires data
        request_path = "/v3/orders/" + oid + "/"
        order_status = self.create_signature(http_method, request_path).json()

        print("Order status: " + str(order_status["success"]))

        # Under development

# Test of the class
api_object = bitso_call(bitso_key, bitso_secret)  # We make an instance of the bitso call class
print(api_object.get_balance())
