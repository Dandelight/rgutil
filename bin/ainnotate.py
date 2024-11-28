#!/usr/bin/env python3

"""
Copyright 2024 Chengdu Qingnan Technology Co., Ltd.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import ast
import glob
import os

import astor
import openai


def process_python_files_in_directory(directory_path, dry_run, use_black):
    """Process Python files in a specified directory to add docstrings and optionally format them with Black."""
    python_files = glob.glob(os.path.join(directory_path, "**", "*.py"), recursive=True)
    for file_path in python_files:
        with open(file_path, "r", encoding="utf-8") as file:
            code = file.read()
        updated_code = add_docstrings(code)
        if use_black:
            import black

            updated_code = black.format_str(updated_code, mode=black.FileMode())
        if not dry_run:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(updated_code)
        else:
            print(updated_code)
        print(f"Processed {file_path}")


def add_docstrings(code):
    """Parses a given Python code to identify functions lacking docstrings, generates comprehensive docstrings using an AI model, and inserts these docstrings into the code."""
    tree = ast.parse(code)

    def generate_docstring(function_code):
        """Generate a comprehensive docstring for the given Python function code using OpenAI's language model API."""
        client = openai.OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
            base_url=os.environ.get("OPENAI_BASE_URL", None),
        )
        prompt = f"""Write a comprehensive docstring for the following Python function:

{function_code}

Please write docstring **only** without any other formatting. Please don't wrap the docstring in quotation marks.

Docstring:"""
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant who writes Python docstrings.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=4096,
            n=1,
            stop=["\n\n"],
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()

    def add_docstring_to_node(node):
        """Add a docstring to an AST node if it does not already have one."""
        if not ast.get_docstring(node):
            function_code = astor.to_source(node)
            docstring = generate_docstring(function_code)
            node.body.insert(0, ast.Expr(ast.Constant(docstring)))

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            add_docstring_to_node(node)
    updated_code = astor.to_source(tree)
    return updated_code


def test():
    """The `test` function contains a string of code that includes three different function definitions: `calculate_average`, `greet`, and `fetch_data`. The purpose of this function is to add docstrings to these functions using the `add_docstrings` function and then print the updated code with the added docstrings."""
    code = """
def calculate_average(numbers):
    total = sum(numbers)
    count = len(numbers)
    if count == 0:
        return 0
    return total / count

def greet(name):
    return f"Hello, {name}!"

async def fetch_data(url):
    # Simulating an async operation
    return f"Data from {url}"
    """
    updated_code = add_docstrings(code)
    print(updated_code)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Add docstrings to Python files in a directory."
    )
    parser.add_argument("path", type=str, default="./")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the updated code without altering existing files",
    )
    parser.add_argument(
        "--black",
        action="store_true",
        help="Format the code using Black after adding docstrings",
    )
    args = parser.parse_args()
    process_python_files_in_directory(args.path, args.dry_run, args.black)
