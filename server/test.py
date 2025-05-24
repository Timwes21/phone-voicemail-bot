from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
load_dotenv()



import os
api_key = os.environ.get("API_KEY")
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", api_key=api_key)
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables import Runnable
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.output_parsers import PydanticOutputParser
from typing_extensions import Literal
from pydantic import BaseModel



class State(BaseModel):
    input: str
    output: str
    action: Literal["keep_talking", "hang_up"]


# Set up LLM
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", api_key=os.environ["API_KEY"])


parser = PydanticOutputParser(pydantic_object=State)
instructions = parser.get_format_instructions().replace("{", "{{").replace("}", "}}")
# Your prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an AI agent that takes the place of a voicemail for my business. Tell customers they can either schedule a callback or leave a message for you to pass to me.: "  + instructions),
    MessagesPlaceholder(variable_name="history", return_messages=True),
    ("human", "{input}")
])

# Chain using LCEL
chain = prompt | llm | parser

# Memory store (your calls dict)
calls = {}

def get_memory(call_id: str) -> BaseChatMessageHistory:
    if call_id not in calls:
        calls[call_id] = ConversationBufferMemory(
            memory_key="history", return_messages=True
        ).chat_memory
    return calls[call_id]




# Runnable with memory
chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history=get_memory,
    input_messages_key="input",
    history_messages_key="history"
)

# Example usage

while True:
    user_input = input("you: ")
    response = chain_with_history.invoke(
        {"input": user_input},
        config={"configurable": {"session_id": "call123"}}
)
    print(response) 

