from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.environ["OPENAI_KEY"]
client = OpenAI(api_key=api_key)


reply = client.responses.create(
        model="gpt-4o-mini",
        instructions="you are an agent that takes the place of the my phone voicemail",
        input="hi i am tim"
    )
    

print(reply.output_text)