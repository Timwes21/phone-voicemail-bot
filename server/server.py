from fastapi import FastAPI, Request, Form
from fastapi.responses import Response
from agent import agent


app = FastAPI()



@app.post("/agent")
async def agent(req: Request):
    data = req.json()
    print(data)
    form = await req.form()
    response = await agent(form)    
    return Response(content=str(response), media_type="application/xml")
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
        