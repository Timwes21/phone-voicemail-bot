from fastapi import FastAPI, Request, Form, WebSocket, WebSocketDisconnect
from fastapi.responses import Response, PlainTextResponse
from agent import get_agent
from twilio.twiml.voice_response import VoiceResponse, Start
import asyncio
import base64
import audioop
import websockets
import json
import os
from dotenv import load_dotenv
load_dotenv()


dg_key = os.environ["DEEPGRAM"]

app = FastAPI()



@app.post("/agent")
async def agent(req: Request):
    form = await req.form()
    # user_input = form.get("SpeechResult", "")
    # call_id = form.get("historyid")
    response = VoiceResponse()
    start = Start()
    start.stream(url="wss://phone-voicemail-bot-production.up.railway.app/ws")
    response.append(start)
    response.say("hello this is Tim's Voicemail Assistant")
    response.gather(input="speech", timeout=5)
    return Response(content=str(response), media_type="application/xml")
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
        
        
@app.websocket("/ws")
async def talk_to_agent(ws: WebSocket):
    await ws.accept()
    
    try:
        while True:
            data = await ws.receive_json()
            
            
            async with websockets.connect("wss://api.deepgram.com/v1/listen?encoding=linear16&sample_rate=8000&channels=1",
            extra_headers={"Authorization": f"Token {dg_key}"}) as dg_ws:
                
                async def handle_transcripts():
                    async for message in dg_ws:
                        data = json.loads(message)
                        if "channel" in data:
                            transcript = data["channel"]["alternatives"][0].get("transcript", "")
                            if transcript:
                                print("User said:", transcript)
                                # Get LLM response
                                response = await get_agent(transcript)
                                print("LLM says:", response)
                                return response

            # Start transcript handler
                asyncio.create_task(handle_transcripts())
                
                if data["event"] == "media":
                    decoded_audio = base64.b64decode(data["mdeia"]["payload"])
                    audio = audioop.ulaw2lin(decoded_audio, 2)
                    response = dg_ws.send(audio)
                    print(response)
                    
            
            
            # print(data)
        
    except WebSocketDisconnect:
        print("websocket dicsonnected")