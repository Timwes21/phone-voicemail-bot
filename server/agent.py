from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.output_parsers import PydanticOutputParser
from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client
from llm import llm
from pydantic import BaseModel
from typing_extensions import TypedDict, Literal
import os
from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI
api_key = os.environ["OPENAI_KEY"]
client = OpenAI(api_key=api_key)



history = {}

    


def get_agent(form):
    user_input = form.get("SpeechResult", "")
    call_id = form.get("historyid")
    
    if not user_input:
        response = VoiceResponse()
        response.say("hello this is Tim's Voicemail Assistant")
        response.gather(input="speech", timeout=5)
        return response

    if call_id not in history:
        history[call_id] = []
        
    history[call_id].append({"role": "user", "content": user_input}) 

    reply = client.responses.create(
        model="gpt-4o-mini",
        instructions="you are an agent that takes the place of the my phone voicemail",
        input=history[call_id]
    )
    
    history[call_id] += [{"role": i.role, "content": i.content} for i in reply.output]    

    print(reply.output_text)

    
    response = VoiceResponse()
    response.say(reply.output_text)
    response.gather(input="speech", timeout=5)
    return response