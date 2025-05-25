from fastapi import FastAPI, Request, Form, WebSocket, WebSocketDisconnect
from fastapi.responses import Response, PlainTextResponse
from agent import get_agent
from twilio.twiml.voice_response import VoiceResponse, Start


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
            
            print(data)
        
    except WebSocketDisconnect:
        print("websocket dicsonnected")