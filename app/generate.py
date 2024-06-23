from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Generate working python code for the task highlighted."),
        ("human", "{input}"),
    ]
)

generate_chain = prompt | ChatOpenAI(model="gpt-4o", temperature= 0.7)