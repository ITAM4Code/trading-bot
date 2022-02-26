#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 21:09:02 2021

@author: rebe y fernando
"""

from pandas import DataFrame #Para DB
import sqlalchemy as sql #Para acceder a MySQL
from tweepy import OAuthHandler, Stream, StreamListener
import json
import os
from dotenv import load_dotenv

#Load TOKEN
load_dotenv()


token_mysql=os.getenv('TOKEN_MYSQL')

# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key=os.getenv('CONSUMER_KEY')
consumer_secret=os.getenv('CONSUMER_SECRET')


# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token=os.getenv('ACCESS_TOKEN')
access_token_secret=os.getenv('ACCESS_TOKEN_SECRET')



#Esta funcion es para pasar a formato json
def extract_tweet_data(data):
    raw_json = json.loads(data)
     
    
    id_str = raw_json['id_str']
    
    language = raw_json['lang']
    
    timestamp = raw_json['timestamp_ms']
    
    text = raw_json['text']
    
    user = raw_json['user']['screen_name']
    
    user_followers = raw_json['user']['followers_count']
    
    user_friends = raw_json['user']['friends_count']
    
    user_statuses = raw_json['user']['statuses_count']
   
    user_creation = raw_json['user']['created_at']
   
    
    
    return [id_str,language,timestamp,text,user,user_followers,user_friends,
            user_statuses,user_creation]




class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    def on_data(self, data):
        
        engine = sql.create_engine(f"mysql://root:{token_mysql}@localhost:3306/Twitter_API")
        
        try:
            list_data = extract_tweet_data(data)
            
            #test_list = []
            #test_list_origin.append(data)
            #test_list.append(list_data)
            
            #df = DataFrame(test_list,columns = ['id_str','language','timestamp','text','user','user_followers','user_friends','user_statuses','user_creation'])
            
            print('Usuario: {}, Mensaje: {}'.format(list_data[4],list_data[3]))
        
        
            #FUNCION PARA INSERTAR LOS DATOS EN BASE SQL
            initial_q = """INSERT INTO data_usuarios(id_str,language,timestamp,text,user,user_followers,user_friends,user_statuses,user_creation) 
             VALUES("{0}","{1}","{2}","{3}","{4}",{5},{6},{7},"{8}")""".format(
                             #id
                             list_data[0],
                             #row.language
                             list_data[1],
                             #row.timestamp
                             list_data[2],
                             #row.text
                             list_data[3].replace('"',"$").strip(),
                             #row.user
                             list_data[4],                         
                             #row.user_followers
                             int(list_data[5]),
                             #row.user_friends
                             int(list_data[6]),
                             #row.user_statuses
                             int(list_data[7]),                         
                             #row.user_creation
                             list_data[8]) 
         
        
            query = initial_q 
            
            engine.execute(query)
        except:
            print("no se pudo extraer el query")
            
        
        #test_list_origin.append(data)
        #test_list.append(list_data)
        return True


    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    
    #LISTA PARA VER COMO ESTRUCTURAMOS LOS DATOS
    #test_list_origin = []
    #test_list = []
    listener_ = StdOutListener()
   
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, listener_)
    stream.filter(track=['btc'])
    
        
   
    
    
    

