import requests
import json
import boto3
from urllib import request
from bs4 import BeautifulSoup
import json
from twilio.rest import Client

# Replace YOUR_API_KEY with your actual API key
api_key = "71e53d4ccb5342819619fa6f686c64d4"

# Specify the endpoint for the API call
endpoint = "https://api.football-data.org/v4/competitions/SA/scorers"
endpoint2 = "http://api.football-data.org/v4/competitions/PL/standings"

# Add the API key to the headers
headers = {"X-Auth-Token": api_key}

# Make the GET request
response = requests.get(endpoint, headers=headers)
responsedata=response.json()

response2 = requests.get(endpoint2, headers=headers)
responsedata2=response2.json()

# Print the status code of the response
with open('data.json', 'w') as json_file:
    json.dump(responsedata["scorers"] , json_file)
   
with open('campionat.json', 'w') as json_file:
    json.dump(responsedata2["standings"][0]['table'][8] , json_file)
     #echipa aleasa de noi, puteam face o interfata in care sa alegem exact ce echipa dorim in functie de indexi lor in campionat, locul 1 avand index 0, locul 2 index 1...

# Print the data returned by the API
with open('C:\\Users\\Sebi\\Proiect_IOT\\data.json','r') as datafile:
  records=json.load(datafile)
with open('C:\\Users\\Sebi\\Proiect_IOT\\manifest.json','r') as manifestfile:
  records=json.load(manifestfile)
with open('C:\\Users\\Sebi\\Proiect_IOT\\manifestcampionat.json','r') as manifestcampionatfile:
  records=json.load(manifestcampionatfile)
with open('C:\\Users\\Sebi\\Proiect_IOT\\campionat.json','r') as campionatfile:
  records=json.load(campionatfile)

access_key="AKIAXUPDCWI7F563C36X"
secret_access_key="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"
session=boto3.Session(aws_access_key_id=access_key,aws_secret_access_key=secret_access_key, region_name='eu-central-1')
s3 = session.client('s3')

bucket_name = 'proiectiot'
file_name = "data.json"
  
#Use the S3 client to upload the file
s3.upload_file(datafile.name, bucket_name, file_name,
 ExtraArgs={'ACL': 'public-read'})

file_name2="manifest.json"
s3.upload_file(manifestfile.name, bucket_name, file_name2)

file_name3="manifestcampionat.json"
s3.upload_file(manifestcampionatfile.name, bucket_name, file_name3)

filename4="campionat.json"
s3.upload_file(campionatfile.name, bucket_name, filename4)
a=responsedata["scorers"][0]["player"]["name"]
b=str(responsedata["scorers"][0]["goals"])
c=str(responsedata["scorers"][0]["assists"])
message_text='Golgheter-ul din momentul actual al campionatului Seria A este '+a+' cu un numar de '+b+' goluri'+' si cu un numar de '+c+' assist-uri'
print(message_text)

account_sid = 'AC9818854ac9abecb0c22beeed674d547e'
auth_token = '59acd6a3f4f1445d22fab3ac71166890'
client = Client(account_sid, auth_token)
from_phone_number = '+17622454951'
to_phone_number = '+40748515458'


message = client.messages.create(   
  body=message_text,
  from_=from_phone_number,
  to=to_phone_number
    )

print('Sid-ul mesajului este:', message.sid) 

