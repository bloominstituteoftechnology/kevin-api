from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain_openai import ChatOpenAI

SYSTEM_PROMPT = """

Review this code for its organization and formatting. Any tips on making it better?

Specifically, please consider the following aspects:

1. Code Readability:
   - Are variable names clear and descriptive?
   - Are functions and methods logically named and scoped?
   - Is the code easy to follow and understand?

2. Code Structure:
   - Is the code modular with appropriate use of functions or classes?
   - Are there any sections that should be refactored into smaller, more manageable pieces?

3. Best Practices:
   - Does the code follow industry best practices for the language/framework?
   - Are there any potential improvements for performance or maintainability?

4. Comments and Documentation:
   - Are comments used effectively to explain non-obvious parts of the code?
   - Is there sufficient documentation for understanding the purpose and usage of the code?

5. Formatting and Style:
   - Is the code consistently formatted according to a recognized style guide (e.g., PEP 8 for Python, Google JavaScript Style Guide)?
   - Are there any areas where the formatting could be improved for better readability?

Please provide detailed feedback and suggestions for improvement. Thank you!
"""

examples = [
    {"input": "Review this code for its organization and formatting. Any tips on making it better?",
     "output": "The code is generally well-structured, but there are a few areas for improvement. Firstly, consider renaming some of the variables to make them more descriptive. For example, 'x' could be renamed to 'customer_count' to clarify its purpose. Secondly, break down the main function into smaller, more manageable functions to improve modularity. Lastly, ensure that all functions and methods have docstrings explaining their purpose and usage. Consistent use of a style guide, such as PEP 8 for Python, will also enhance readability and maintainability."},
    
    {"input": "Review this code for its organization and formatting. Any tips on making it better?",
     "output": "Upon reviewing the code, I noticed a few key areas for improvement. The use of comments could be enhanced to explain complex sections, making the code easier to understand for others. Additionally, grouping related functions into classes would improve the overall structure and readability. There are some redundant lines of code that could be refactored for efficiency. Lastly, adhering to a consistent indentation style and line length will make the code more visually appealing and easier to maintain."},
]


example_prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "{input}"),
        ("ai", "{output}"),
    ]
)
few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=examples,
)

print(few_shot_prompt.format())

final_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        few_shot_prompt,
        ("human", "{input}"),
    ]
)

review_chain = final_prompt | ChatOpenAI(model="gpt-4o", temperature= 0.7)