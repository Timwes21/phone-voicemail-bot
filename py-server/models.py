from typing_extensions import TypedDict, Literal, Optional
from pydantic import Field, BaseModel

class State(TypedDict):
    caller_id: str
    convo: list[dict]
    
    
class Routes(BaseModel):
    action: Literal["schedule_callback", "pass_message", "nothing"]

class Callback(BaseModel):
    day_of_week: Optional[str]
    date: str = Field(examples=["01/30"])
    name_of_caller: str
    
class PassedMessage(BaseModel):
    message: str = Field(description="A summarized version of the message the caller wanted to leave")
    name_of_caller: str 
    
    
    
