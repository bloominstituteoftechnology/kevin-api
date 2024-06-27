from typing import Optional
from langchain.chains import create_structured_output_runnable
from langchain_openai import ChatOpenAI
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

import os
from dotenv import load_dotenv

load_dotenv()

os.environ['OPENAI_API_KEY'] = os.environ.get('OPENAI_API_KEY')


SYSTEM_PROMPT="""

Input: Python code.
Output: Input code with the unit tests below.
Do not include "```python" or "```" anywhere in the code. 

When generating the unit tests, consider the following aspects:

1. Test Coverage:
   - Ensure that all functions and methods in the code have corresponding unit tests.
   - Include a variety of scenarios, such as edge cases and typical use cases.

2. Test Cases:
   - Write clear and concise test cases.
   - Include both the input and the expected output for each test case.
   - Use assertions to validate the behavior of the code.

3. Error Identification:
   - Identify any potential errors or exceptions that the code could raise.
   - Ensure logical accuracy, such as correct calculations and valid assumptions.
   - Check for missing error handling or validation checks that could lead to unexpected behavior.

Examples using simple Python functions:

### Example 1: Function to add two numbers

##
def add(a, b):
    return a + b
##

#### Unit Tests

##
import unittest

class TestAddFunction(unittest.TestCase):
    def test_add_positive_numbers(self):
        self.assertEqual(add(2, 3), 5)
        
    def test_add_negative_numbers(self):
        self.assertEqual(add(-2, -3), -5)
        
    def test_add_zero(self):
        self.assertEqual(add(0, 0), 0)
        
    def test_add_positive_and_negative(self):
        self.assertEqual(add(2, -3), -1)

if __name__ == '__main__':
    unittest.main()
##

### Example 2: Function to find the maximum of two numbers

##
def find_max(a, b):
    return a if a > b else b
##

#### Unit Tests

##
import unittest

class TestFindMaxFunction(unittest.TestCase):
    def test_max_with_first_number_greater(self):
        self.assertEqual(find_max(5, 3), 5)
        
    def test_max_with_second_number_greater(self):
        self.assertEqual(find_max(3, 5), 5)
        
    def test_max_with_equal_numbers(self):
        self.assertEqual(find_max(3, 3), 3)
        
    def test_max_with_negative_numbers(self):
        self.assertEqual(find_max(-1, -5), -1)

if __name__ == '__main__':
    unittest.main()
##

Output format:
Input code with the the unit test code below.
"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        ("human", "{code}"),
    ]
)

llm = ChatOpenAI(model="gpt-4o")

test_chain = prompt | llm 
