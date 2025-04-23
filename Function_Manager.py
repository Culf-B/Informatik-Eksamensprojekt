import function_script as fs


class Function_Manager:
    def __init__(self):
        self.function_list = []
        
    def make_new_function(self, input):
        func = fs.Function(input)
        self.function_list.append(func)

    def search_function(self):
        # To be made
        d = 1
        
    def change_function(self, func):
        # To be made
        d = 1
