from fastapi import FastAPI, Request
from dotenv import load_dotenv
load_dotenv()
from action_graph import graph


app = FastAPI()


@app.post("/")
async def get_agent_reply(req: Request):
    data = await req.json()
    convo = data["convo"]
    caller_id = data["callerId"]
    if len(convo) < 1:
        print("they didnt say anything")
        return
    graph.invoke({"convo": convo, "caller_id": caller_id})

    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=3000)