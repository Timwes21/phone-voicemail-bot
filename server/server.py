from fastapi import FastAPI, Request, Form
from fastapi.responses import Response
from dotenv import load_dotenv
import os
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.llm import LLMChain
from twilio.twiml.voice_response import VoiceResponse
load_dotenv()

app = FastAPI()
api_key = os.environ.get("API_KEY")
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", api_key=api_key)
@app.post("/agent")
async def agent(req: Request):
    form = await req.form()
    user_input = form.get("SpeechResult", "")
    
    if not user_input:
        response = VoiceResponse()
        response.say("hello this is Tim's Voicemail Assistant")
        response.gather(input="speech", timeout=5)
        return Response(content=str(response), media_type="application/xml")
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an ai agent that takes the place of a voicemail"),
        MessagesPlaceholder(variable_name="history", return_messages=True),
        ("human", "{input}")
    ])
    memory = ConversationBufferMemory(memory_key="history", return_messages=True)
    chain = LLMChain(
        llm=llm,
        prompt=prompt,
        memory=memory,
        verbose=True 
        
    )
    result = chain.invoke(user_input)
    print(result)
    response = VoiceResponse()
    response.say(result['text'])
    return Response(content=str(response['text']), media_type="application/xml")
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
        