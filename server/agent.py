from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.output_parsers import PydanticOutputParser
from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client
from llm import llm
from pydantic import BaseModel
from typing_extensions import TypedDict, Literal

class State(BaseModel):
    input: str
    output: str
    action: Literal["keep_talking", "hang_up"]



calls = {}
def get_memory(call_id: str):
    if call_id not in calls:
        calls[call_id] = ConversationBufferMemory(
            memory_key="history", return_messages=True
        ).chat_memory
    return calls[call_id]


def get_agent(form):
    print(form)
    print(type(form))
    user_input = form.get("SpeechResult", "")
    call_id = form.get("CallSid")
    
    if not user_input:
        response = VoiceResponse()
        response.say("hello this is Tim's Voicemail Assistant")
        response.gather(input="speech", timeout=5)
        return response

    parser = PydanticOutputParser(pydantic_object=State)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an ai agent that takes the place of a voicemail for my business, tell customers that they can either schedule a call back by me, or you can pass the message to you and you'll pass the message to me " + parser.get_format_instructions()),
        MessagesPlaceholder(variable_name="history", return_messages=True),
        ("human", "{input}")
    ])
    
    chain = prompt | llm | parser
    chain_with_history = RunnableWithMessageHistory(
        chain,
        get_session_history=get_memory,
        input_messages_key="input",
        history_messages_key="history"
    )

    
    response = chain_with_history.invoke(
        {"input": user_input},
        config={"configurable": {"session_id": call_id}}
    )
    print(response.output)
    if response.action == "hang_up":
        del calls[call_id]
    response = VoiceResponse()
    response.say(response.content)
    response.gather(input="speech", timeout=5)
    return response