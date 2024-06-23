from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

SYSTEM_PROMPT="""

Generate unit tests for the given Python code. 
Based on the tests created, highlight any possible errors in the code. 

Input: Python code.
Output: A numbered list of errors to fix. If there are no errors and the code should work, return "none".

When generating the unit tests and identifying errors, consider the following aspects:

1. Test Coverage:
   - Ensure that all functions and methods in the code have corresponding unit tests.
   - Include a variety of scenarios, such as edge cases and typical use cases.

2. Test Cases:
   - Write clear and concise test cases.
   - Include both the input and the expected output for each test case.
   - Use assertions to validate the behavior of the code.

3. Error Identification:
   - Identify any potential errors or exceptions that the code could raise.
   - Highlight logical errors, such as incorrect calculations or invalid assumptions.
   - Note any missing error handling or validation checks that could lead to unexpected behavior.

4. Output:
   - Provide a list of possible errors identified based on the unit tests.
   - Focus only on highlighting errors, not the entire unit test code.

Please provide detailed feedback on the possible errors identified from the unit tests. Thank you!
```
"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        ("human", "{input}"),
    ]
)

test_chain = prompt | ChatOpenAI(model="gpt-4o", temperature= 0.8)