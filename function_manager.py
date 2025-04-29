import function_script as fs

class Function_Manager:
    def __init__(self):
        self.function_list = []

    def choose_action(self, input):
        input = input.replace(" ", "")
        func_name = None

        if "=" in input and len(input.split("=")[0]) > 2:
            lhs = input.split("=")[0]
            func_name = lhs[0]  # 'f' in "f(x)"

        if func_name:
            for i, func in enumerate(self.function_list):
                if func.func_name == func_name:
                    self.change_function(input, i)
        else:
            self.make_new_function(input)
        
    def make_new_function(self, input):
        func = fs.Function(input, self)
        self.function_list.append(func)
        
    def change_function(self, input, index):
        existing_name = self.function_list[index].func_name
        func = fs.Function(input, self, existing_name)
        self.function_list[index] = func

        
    def get_functions(self):
        return self.function_list

if __name__ == '__main__':
    fm = Function_Manager()
    fm.choose_action("f(x) = 5x")
    print(fm.get_functions())