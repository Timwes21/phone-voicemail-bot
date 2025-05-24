from fastapi import FastAPI, Request, Form
from fastapi.responses import Response, PlainTextResponse
from agent import get_agent


app = FastAPI()



@app.post("/agent")
async def agent(req: Request):
    form = await req.form()
    response = get_agent(form)    
    return Response(content=str(response), media_type="application/xml")
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
        