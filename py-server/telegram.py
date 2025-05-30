import os
import requests
from dotenv import load_dotenv
load_dotenv()
token_id = os.environ['BOT_TOKEN']
chat_id = os.environ['BOT_ID']


url = f"https://api.telegram.org/bot{token_id}/sendMessage"

def send_message(message):
    params = {"chat_id": chat_id, "text": message}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        print("Notification sent successfully!")
        return True
    else:
        print(f"Failed to send notification. Error: {response.text}")
        return False
        
        
