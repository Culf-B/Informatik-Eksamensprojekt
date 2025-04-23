import function_script as fs


class Function_Manager:
    def __init__(self):
        self.function_list = []
        
    def make_new_function(self, input):
        func = fs.Function(input)
        self.function_list.append(func)
        
    def change_function(self, func, index):
        self.function_list[index] = self.make_new_function(func)
        
    def get_functions(self):
        return self.function_list
