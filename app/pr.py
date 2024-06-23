from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

SYSTEM_PROMPT="""

This is a mock API call. 
Return the following string no matter the input: 
The code has been successfully committed to GitHub, and a pull request has been created.
```
"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        ("human", "{code}"),
    ]
)

pr_chain = prompt | ChatOpenAI(model="gpt-3.5-turbo", temperature= 0.8)