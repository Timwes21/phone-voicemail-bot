from langgraph.graph import StateGraph, START, END # type: ignore
from langchain_core.messages import HumanMessage, SystemMessage
from typing_extensions import TypedDict, Literal
from llm import llm

class State(TypedDict):
    input: str
    output: str
    
class Routes(TypedDict):
    action: Literal["schedule_callback", "pass_message", "no_action"]
    
    
action_router = llm.with_structured_output(Routes)
    
def call_action_action_router(state: State):
    return state['input']

def scheduler(state: State):
    """Scehdules a time to call back"""
    
def pass_message(state: State):
    """Passes a message"""
    
    
builder = (
    StateGraph(State)
    .add_node("call_action_action_router", call_action_action_router)
    .add_node("scheduler", scheduler)
    .add_node("pass_message", pass_message)
    .add_conditional_edges(START, call_action_action_router, {"schedule_callback": "schedule_callback", "pass_message":"pass_message"})
    .add_edge("pass_message", END)
    .add_edge("scheduler", END)
)





