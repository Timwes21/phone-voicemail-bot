from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.llm import LLMChain
from dotenv import load_dotenv

load_dotenv()


import os
api_key = os.environ.get("API_KEY")
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", api_key=api_key)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an ai agent that takes the place of a voicemail so whoever called can still talk to someone helpful"),
    MessagesPlaceholder(variable_name="history", return_messages=True),
    ("human", "{input}")
])
memory = ConversationBufferMemory(memory_key="history", return_messages=True)
chain = LLMChain(
    llm=llm,
    prompt=prompt,
    memory=memory,
    verbose=True 
    
)
while True:
    my_input = input("talk to agent: ")
    result = chain.invoke(my_input)
    print(result['text'])
