from hacksport.problem import ProtectedFile, Remote

class Problem(Remote):
    program_name = 'add_random.py'

    def initialize(self):
        self.value_1 = self.random.randint(1, 10)
        self.value_2 = self.random.randint(1, 10)
