from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Generate unit tests for this Python code. Based on the tests created, highlight possible errors."),
        ("human", "{input}"),
    ]
)

test_chain = prompt | ChatOpenAI(model="gpt-4o", temperature= 0.7)