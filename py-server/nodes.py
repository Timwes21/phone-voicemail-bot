from langchain.output_parsers import PydanticOutputParser
from models import Callback, State, Routes, PassedMessage
from langchain.prompts import ChatPromptTemplate
from llm import llm
from telegram import send_message
import datetime
import json




def call_action_action_router(state: State):
    parser = PydanticOutputParser(pydantic_object=Routes)
    prompt = ChatPromptTemplate.from_template("Based on this convo, decide whether a the caller wanted to schedule a callback, pass a message, or do nothing: {convo} {format}").partial(format=parser.get_format_instructions())
    chain = prompt | llm | parser
    result = chain.invoke({"convo": json.dumps(state['convo'])})
    print(result)
    return result.action

def scheduler(state: State):
    parser = PydanticOutputParser(pydantic_object=Callback)
    prompt = ChatPromptTemplate.from_template("get the date, day of the week, name of the person, for reference the current date is {date}. {convo} {format}").partial(date=datetime.date.today(), format=parser.get_format_instructions())
    chain = prompt | llm | parser
    result = chain.invoke({"convo": state['convo']})
    body = f"You have a callback with {result.name_of_caller} on {result.day_of_week}, {result.date}. You can call them back at {state['caller_id']}"
    return send_message(body)
    
    
    
def pass_message(state: State):
    parser = PydanticOutputParser(pydantic_object=PassedMessage)
    prompt = ChatPromptTemplate.from_template("The caller wants to leave a message, be sure to summarize the message they are leaving while still outlining important points {convo} {format}").partial(format=parser.get_format_instructions())
    chain = prompt | llm | parser
    result = chain.invoke({"convo": state["convo"]})
    body = f"{result.name_of_caller} wanted to leave a message and i summarized it for you: {result.message}"
    return send_message(body)
    
def nothing(state: State):
    print("there was not an action chosen")
