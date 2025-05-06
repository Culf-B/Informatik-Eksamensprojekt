from sympy import *

class Function:
    def __init__(self, input, manager, existing_name=None):
        if input:
            self.inp = input.replace(" ", "")
        if not self.inp:
            raise ValueError("Input cannot be empty.")
        
        self.func_name = None
        self.manager = manager

        if "=" in self.inp:
            self.lhs, self.rhs = self.inp.split("=")
            self.var_name = self.lhs[2] if len(self.lhs) > 2 else "x"
            desired_name = self.lhs[0]

            self.func_name = existing_name if existing_name else self.get_unique_name(desired_name)
            self.func = self.rhs
        else:
            self.func = self.inp 
            self.var_name = self.detect_variable(self.func)
            self.func_name = existing_name if existing_name else self.get_unique_name() # Checks if input had existing name in function list

        print(self.func)
        self.var = symbols(self.var_name)
        self.func = self.fix_multiplication(self.func)
        print(self.func)
        
        try:
            self.func = sympify(self.func)
        except Exception as e:
            raise ValueError(f"Failed to parse expression '{self.func}': {e}")


    def yFunc(self, xVal):
        return self.func.subs({self.var: xVal})

    def detect_variable(self, expression_str):
        expr = sympify(self.fix_multiplication(expression_str))
        self.vars_in_expr = list(expr.free_symbols) # Find all possible variables in expression

        # Filter out contants in math
        ignored_symbols = {'e', 'p', 'i'}
        filtered_vars = [v for v in self.vars_in_expr if str(v) not in ignored_symbols]

        return str(filtered_vars[0]) if filtered_vars else "x"


    def fix_multiplication(self, expr):
        known_funcs = ['sin', 'cos', 'tan', 'exp', 'log', 'sqrt', "pi"]
        i = 0
        result = ""
        while i < len(expr):
            # Check for known function in expression
            matched_func = None
            for func in known_funcs:
                if expr[i:i+len(func)] == func: # Checks if any set of consecutive indexes matches a known function
                    matched_func = func
                    break # Stops the current iteration of the while loop

            if matched_func:
                result += matched_func
                i += len(matched_func)
                
                # Check if function is immediately followed by a variable and fix syntax
                if i < len(expr) and expr[i].isalpha():
                    result += "(" + expr[i] + ")"
                    i += 1
                continue

            # Handle implicit multiplication
            current = expr[i]
            result += current

            if i < len(expr) - 1:
                next_char = expr[i + 1]
                if ((current.isdigit() and next_char.isalpha()) or (current.isalpha() and next_char.isdigit()) or (current.isalpha() and next_char.isalpha())): # Fixes multiplication for cases: 2x, x2, xy
                    result += "*"

            i += 1
        return result

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
