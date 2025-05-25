from openai import OpenAI
import os
from dotenv import load_dotenv
from openai.types.responses.response_text_delta_event import ResponseTextDeltaEvent 
load_dotenv()
# api_key = os.environ["OPENAI_KEY"]



reply = client.responses.create(
        model="gpt-4o-mini",
        instructions="you are an agent that takes the place of the my phone voicemail",
        input="hi i am tim",
        stream=True
    )
    

for stream in reply:
    if isinstance(stream, ResponseTextDeltaEvent):
        print(stream.delta)