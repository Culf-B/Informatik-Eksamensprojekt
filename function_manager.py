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
        else:
            self.make_new_function

        print(func_name)

        if func_name and len(self.function_list) > 0:
            self.function_found = False
            for i, func in enumerate(self.function_list):
                if func.func_name == func_name:
                    self.change_function(input, i)
                    self.function_found = True
                    break
            if self.function_found == False:
                self.make_new_function(input)
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
    
    def get_function_strings(self):
        strings = []
        for function in self.function_list:
            strings.append(f'{function.func_name}({function.var}) = {function.func}')
        return strings
    
    def delete_all_functions(self):
        self.function_list = []

if __name__ == '__main__':
    fm = Function_Manager()
    fm.choose_action("f(x) = 5x")
    fm.choose_action("f(x) = 3*x^2")
    print(fm.get_functions()[0].func)
    