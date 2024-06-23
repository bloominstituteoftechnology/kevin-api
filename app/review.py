from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain_openai import ChatOpenAI

SYSTEM_PROMPT = """

Review this code for its organization and formatting. 
The input will be code, and the output should always be a numbered list of recommendations for improvement.

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

Please provide detailed feedback and suggestions for improvement in a numbered list. Thank you!
"""

examples = [
    {"input": "def calculate_discount(price, discount): return price - (price * discount) def process_order(order): total = sum(item['price'] for item in order) return total / len(order) def fetch_user_data(user_id): response = requests.get(f'https://api.example.com/users/{user_id}') return response.json()",
     "output": "1. Consider renaming some of the variables to make them more descriptive. For example, 'item' in 'process_order' could be renamed to 'product'. 2. Break down the 'process_order' function into smaller, more manageable functions to improve modularity. 3. Ensure that all functions and methods have docstrings explaining their purpose and usage. 4. Consistent use of a style guide, such as PEP 8 for Python, will also enhance readability and maintainability. 5. Add error handling in 'fetch_user_data' for network issues or invalid responses."},

    {"input": "def add_item_to_cart(cart, item): cart.append(item) return cart def calculate_total(prices): return sum(prices) def authenticate_user(username, password): if username == 'admin' and password == 'admin': return True return False",
     "output": "1. Enhance the use of comments to explain complex sections, making the code easier to understand for others. 2. Group related functions into classes to improve the overall structure and readability. 3. Refactor redundant lines of code for efficiency, such as checking user credentials in 'authenticate_user'. 4. Adhere to a consistent indentation style and line length to make the code more visually appealing and easier to maintain. 5. Add validation in 'add_item_to_cart' to check for item availability before adding to the cart."}
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

final_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        few_shot_prompt,
        ("human", "{input}"),
    ]
)

review_chain = final_prompt | ChatOpenAI(model="gpt-4o", temperature= 0.7)