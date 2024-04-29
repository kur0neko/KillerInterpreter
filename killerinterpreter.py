import sys
import tokenize
import os
import io
import ast
import subprocess
import os
from tokenizer import Tokenizers

#The ast module helps Python applications to process trees of the Python abstract syntax grammar. 

class Lexer:
    def tokenize_code(self, code):
        tokens = []
        try:
            tokens = list(tokenize.tokenize(io.BytesIO(code.encode('utf-8')).readline))
        except tokenize.TokenError as e:
            print(f"Tokenization error: {e}")
        return tokens

class Parser:
    def parse_code(self, code):
        try:
            tree = ast.parse(code)
            return tree, None  # No error
        except SyntaxError as e:
            error_details = {
                'lineno': e.lineno,
                'msg': e.msg,
                'text': e.text.strip() if e.text else "No text available",
                'offset': e.offset
            }
            return None, error_details  # Return None for tree, and error details


class SemanticAnalyzer(ast.NodeVisitor):
    def __init__(self, memory_stack):
        self.memory_stack = memory_stack
        self.scope = {}

    def visit_FunctionDef(self, node):
        for arg in node.args.args:
            self.scope[arg.arg] = None  # Initialize function arguments in scope
        for body_item in node.body:
            self.visit(body_item)  # Recursively visit all nodes in the function body

    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name):
                value = self.visit(node.value)  # Evaluate the expression to get the value
                self.scope[target.id] = value   # Assign the value in the scope dictionary
                self.memory_stack.push((target.id, value))  # Push to memory stack

    def visit_Name(self, node):
        #if isinstance(node.ctx, ast.Load) and node.id not in self.scope:
            #raise NameError(f"'{node.id}' is not defined")  # Make sure to use quotes for clarity
        return self.scope.get(node.id, None)

    def visit_Constant(self, node):
        return node.value

    def analyze(self, node):
        try:
            self.visit(node)
        except Exception as e:  # Catch all exceptions and handle them
            print(f"Semantic Analysis Error: {e}")

class MemoryStack:
    def __init__(self):
        self.stack = []

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        if self.stack:
            return self.stack.pop()
        else:
            raise IndexError("Memory stack is empty")

        
class PythonInterpreter:
    def __init__(self, filepath):
        self.filepath = filepath
        self.memory_stack = MemoryStack()

    def read_code(self):
        if not os.path.exists(self.filepath) or not os.access(self.filepath, os.R_OK):
            print(f"Error: The file '{self.filepath}' cannot be accessed or does not exist.")
            sys.exit(1)
        with open(self.filepath, 'r') as file:
            code = file.read()
            return code

    def analyze(self):
        code = self.read_code()
        lexer = Lexer()
        tokens = lexer.tokenize_code(code)

        parser = Parser()
        tree, error_details = parser.parse_code(code)
        if tree is not None:
            ##print("\nAST successfully generated.\n")
            semantic_analyzer = SemanticAnalyzer(self.memory_stack)
            semantic_analyzer.analyze(tree)
           ## print("Semantic Analysis completed successfully.")
            return code  # Return code for execution if analysis is successful
        elif error_details:
            print("Syntax Error Detected:")
            print(f"Line {error_details['lineno']}: {error_details['msg']}")
            print(f"Error at text: '{error_details['text']}' near position {error_details['offset']}")
            return None

    def execute(self):
        code = self.analyze()
        if code:
            print("\nExecuting the code...\n")
            try:
                # Set __name__ to __main__ to simulate running the script directly
                exec(code, {'__name__': '__main__'})
                print("\nCode executed successfully.")
            except Exception as e:
                print(f"Execution error: {e}")
    
                
def main():
    if len(sys.argv) != 2:
        print("Usage: python interpreter.py <path_to_python_file>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    if not os.path.exists(filepath) or not os.access(filepath, os.R_OK):
        print(f"Error: The file '{filepath}' cannot be accessed or does not exist.")
        sys.exit(1)
        
     #use tokentizer class to split all token and explain   
    file_tokens= Tokenizers.tokenize_file(filepath)
    with open(filepath, 'r') as file:
        code = file.read()
        
    parser = Parser()
    tree, error_details = parser.parse_code(code)

    if error_details:
        print(f"Syntax Error on Line {error_details['lineno']}: {error_details['error']}")
        print(f"Error at text: '{error_details['line']}'")
        
    print("Token explanations:")
    for token in file_tokens:
        token_id, token_type, token_value = Tokenizers.explain_token(token)
        print(f"ID= {str(token_id):<10s} Type= {token_type:>8s}  '{token_value}'")
    
    fileAnalyze = PythonInterpreter(filepath)
    fileAnalyze.analyze()
    fileAnalyze.execute() 


if __name__ == "__main__":
    main()



