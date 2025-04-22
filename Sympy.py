from sympy import *
from keyboard import is_pressed
import time

functions = {
    "functionList": [],
}

class MakeFunc:
    def __init__(self):
        self.inp = input('Write your function here: ').replace(" ", "")
        if not self.inp:
            raise ValueError("Input cannot be empty.")
        
        self.funcName = None

        # Checks if function is of form f(x) or not and runs accordingly
        if "=" in self.inp:
            self.lhs, self.rhs = self.inp.split("=")
            self.varName = self.lhs[2] if len(self.lhs) > 2 else "x"
            desired_name = self.lhs[0]
            self.funcName = self.get_unique_name(desired_name)
            self.func = self.rhs
        else:
            self.func = self.inp
            self.varName = self.detect_variable(self.func)
            self.funcName = self.get_unique_name()

        self.var = symbols(self.varName)
        self.func = self.fix_multiplication(self.func)

        try:
            self.func = sympify(self.func)
        except Exception as e:
            raise ValueError(f"Failed to parse expression '{self.func}': {e}")

    def yFunc(self, xVal):
        return self.func.subs({self.var: xVal})

    def detect_variable(self, expression_str):
        expr = sympify(self.fix_multiplication(expression_str))
        vars_in_expr = list(expr.free_symbols)
        return str(vars_in_expr[0]) if vars_in_expr else "x"

    def fix_multiplication(self, expr):
        modified_expr = ""
        length = len(expr)

        for i in range(length):
            current = expr[i]
            modified_expr += current

            if i < length - 1:
                next_char = expr[i + 1]
                if (current.isdigit() or current.isalpha()) and (next_char.isalpha() or next_char.isdigit()):
                    modified_expr += "*"

        return modified_expr

    def get_unique_name(self, base="f"):
        existing_names = [func.funcName for func in functions["functionList"] if func.funcName]
    
        # Give next available name to current function
        start_index = ord('f')
        for i in range(start_index, ord('z') + 1):
            letter = chr(i)
            if letter not in existing_names:
                return letter
            
        index = 1
        while True:
            new_name = f"{base}{index}"
            if new_name not in existing_names:
                return new_name
            index += 1

# Action handlers
def add_function():
    try:
        time.sleep(0.3)
        f = MakeFunc()
        functions["functionList"].append(f)
        latest_func = functions["functionList"][-1]
        print(f"\nFunction Name: {latest_func.funcName}")
        print(f"Variable: {latest_func.var}")
        print(f"Function: {latest_func.func}")
        print(f"Function output at {latest_func.var} = 3: {latest_func.yFunc(3)}\n")
    except Exception as e:
        print(f"Error: {e}")

# Keeps the program running, but only acts when there is a callback
while True:
    time.sleep(0.1)

    if is_pressed('backspace'):
        add_function()

    if is_pressed('alt'):
        break

# Output summary of functions
if functions["functionList"]:
    print("\n--- All Functions ---")
    for func in functions["functionList"]:
        print(f"{func.funcName or 'f'}({func.var}) = {func.func}")
