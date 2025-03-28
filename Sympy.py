from sympy import *

class MakeFunc:
    def __init__(self):
        self.inp = input('Write your function here: ').replace(" ", "")
        self.funcName = None  # Initialize function name
        
        # Split on '=', handle function definitions
        if "=" in self.inp:
            lhs, rhs = self.inp.split("=")
            self.funcName = lhs[0]
            self.varName = lhs[2]
            self.func = rhs
        else:
            # Expression without function name
            self.func = self.inp
            self.varName = self.detect_variable(self.func)

        # Ensure variable is set
        self.var = symbols(self.varName)

        # Fix implicit multiplication
        self.func = self.fix_multiplication(self.func)

        # Parse to SymPy expression
        try:
            self.func = sympify(self.func)
        except Exception as e:
            raise ValueError(f"Failed to parse expression '{self.func}': {e}")

    def yFunc(self, xVal):
        """Evaluate the function at a given value."""
        return self.func.subs({self.var: xVal})

    def detect_variable(self, expression_str):
        """Dynamically detect variable if not explicitly provided."""
        expr = sympify(self.fix_multiplication(expression_str))
        vars_in_expr = list(expr.free_symbols)
        return str(vars_in_expr[0]) if vars_in_expr else "x"

    def fix_multiplication(self, expr):
        """Ensure explicit multiplication symbols."""
        modified_expr = ""
        length = len(expr)

        for i in range(length):
            current = expr[i]
            modified_expr += current

            # Insert * when necessary
            if i < length - 1:
                next_char = expr[i + 1]

                # If current is a digit/variable and next is a variable/digit
                if (current.isdigit() or current.isalpha()) and (next_char.isalpha() or next_char.isdigit()):
                    modified_expr += "*"

        return modified_expr

# Test the refactored code
t = MakeFunc()
if t.funcName:
    print(f"Function Name: {t.funcName}")
print(f"Detected variable: {t.var}")
print(f"Function: {t.func}")
print(f"Function output at x=3: {t.yFunc(3)}")
