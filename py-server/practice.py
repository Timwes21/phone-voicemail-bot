from twilio.rest import Client
import os
from dotenv import load_dotenv
load_dotenv()
import asyncio
            
            
account_sid = os.environ['ACCOUNT_SID']
auth_token = os.environ['AUTH_TOKEN']
twilio_phn_nmbr = os.environ['NUMBER']
my_phn_nmbr = "+17726210972"
client = Client(account_sid, auth_token)


def send_message(body):
    message = client.messages.create(
        body=body,
        from_=twilio_phn_nmbr,  # your Twilio phone number
        to=my_phn_nmbr      # recipient's phone number
    )
    return message.status    
    
