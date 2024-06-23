from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Review this code for its organization and formatting. Any tips on making it better?"),
        ("human", "{input}"),
    ]
)

review_chain = prompt | ChatOpenAI(model="gpt-4o", temperature= 0.7)