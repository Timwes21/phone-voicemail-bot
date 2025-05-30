from langgraph.graph import StateGraph, START, END # type: ignore
from langchain_core.messages import HumanMessage, SystemMessage
from models import State, Callback
from nodes import (
    call_action_action_router,
    scheduler,
    pass_message,
    nothing
)
    


    
builder = (
    StateGraph(State)
    .add_node("call_action_action_router", call_action_action_router)
    .add_node("scheduler", scheduler)
    .add_node("pass_message", pass_message)
    .add_node("nothing", nothing)
    .add_conditional_edges(START, call_action_action_router, {"schedule_callback": "scheduler", "pass_message":"pass_message", "": "nothing"})
    .add_edge("pass_message", END)
    .add_edge("scheduler", END)
    .add_edge("nothing", END)
)



graph = builder.compile()

