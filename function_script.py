from sympy import *
import time

functions = {
    "functionList": [],
}

class Function:
    def __init__(self, input, manager):
        if input:
            self.inp = input.replace(" ", "")
        if not self.inp:
            raise ValueError("Input cannot be empty.")
        
        self.func_name = None
        self.manager = manager

        # Checks if function is of form f(x) or not and runs accordingly
        if "=" in self.inp: # "f(x)" in the input
            self.lhs, self.rhs = self.inp.split("=")
            self.var_name = self.lhs[2] if len(self.lhs) > 2 else "x" # Takes third index, which would be x in "f(x)" 
            desired_name = self.lhs[0] # Takes first index, which would be f in "f(x)" 
            self.func_name = self.get_unique_name(desired_name)
            self.func = self.rhs
        else: # No "f(x)" in the input
            self.func = self.inp 
            self.var_name = self.detect_variable(self.func)
            self.func_name = self.get_unique_name()

        self.var = symbols(self.var_name) # Initializes variable as symbol in sympy
        self.func = self.fix_multiplication(self.func) # Standardize function so sympy can sympify the expression

        try:
            self.func = sympify(self.func) # Recognize expression and set expression as function
        except Exception as e:
            raise ValueError(f"Failed to parse expression '{self.func}': {e}")

    def yFunc(self, xVal):
        return self.func.subs({self.var: xVal})

    def detect_variable(self, expression_str):
        expr = sympify(self.fix_multiplication(expression_str)) # Makes a sympy expression where letters are variables
        vars_in_expr = list(expr.free_symbols) # Checks expression for variable 
        return str(vars_in_expr[0]) if vars_in_expr else "x" # Returns variable to set the variable

    def fix_multiplication(self, expr):
        modified_expr = ""
        length = len(expr)

        for i in range(length):
            current = expr[i]
            modified_expr += current

            if i < length - 1: # Loops through the length of the expression
                next_char = expr[i + 1]
                if (current.isdigit() or current.isalpha()) and (next_char.isalpha() or next_char.isdigit()): # Checks if the expression has a situation like this: 2x or x2
                    modified_expr += "*" # Inserts multiplication symbol for the sympify function

        return modified_expr

    def get_unique_name(self, base="f"):
        existing_names = [func.func_name for func in self.manager.get_functions() if func.func_name] # Get existing names
    
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
        f = Function()
        functions["functionList"].append(f)
        latest_func = functions["functionList"][-1]
        print(f"\nFunction Name: {latest_func.func_name}")
        print(f"Variable: {latest_func.var}")
        print(f"Function: {latest_func.func}")
        print(f"Function output at {latest_func.var} = 3: {latest_func.yFunc(3)}\n")
    except Exception as e:
        print(f"Error: {e}")

# This code is will only run when running this file (for testing) and not when running the whole program
if __name__ == '__main__':
    # Keeps the program running, but only acts when there is a callback
    from keyboard import is_pressed
    while True:
        time.sleep(0.1)

        if is_pressed('backspace'):
            add_function()

        if is_pressed('alt'):
            break
