from sympy import symbols, sympify

class MakeFunc:
    def __init__(self):
        self.inp = input('Write your function here: ').replace(" ", "")
        self.str = self.inp.split("=")  # Split into left-hand and right-hand sides
        
        if len(self.str) == 2:
            # Case where the function is defined with a variable: f(x) = 2x+5
            self.funcName = self.str[0][0]  # Extract function name
            self.varName = self.str[0][2]  # Extract variable name
            self.var = symbols(self.varName)  # Convert variable to a SymPy Symbol
            self.expr_str = self.str[1]
        else:
            # Case where only an expression is given: 2x+5
            self.expr_str = self.str[0]
            self.var = self.detect_variable(self.expr_str)  # Detect variable automatically
        
        # Convert the expression to a SymPy expression
        self.func = sympify(self.expr_str)

    def yFunc(self, xVal):
        """Evaluate the function at a given value."""
        return self.func.subs({self.var: xVal})

    def detect_variable(self, expression_str):
        """Detect the variable in the expression dynamically."""
        expr = sympify(expression_str)  # Convert string to SymPy expression
        vars_in_expr = list(expr.free_symbols)  # Extract symbols
        return vars_in_expr[0] if vars_in_expr else symbols('x')  # Default to x if no variable found

# Test
t = MakeFunc()
print(f"Detected variable: {t.var}")
print(f"Function: {t.func}")
print(f"Function output at x=3: {t.yFunc(3)}")