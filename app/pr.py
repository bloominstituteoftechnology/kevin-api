from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Output a confirmation message highlighting that the given code has been committed to Github and a pull request has been created."),
        ("human", "{input}"),
    ]
)

pr_chain = prompt | ChatOpenAI(model="gpt-4o", temperature= 0.7)