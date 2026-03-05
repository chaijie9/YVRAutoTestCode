class Employee:
    def __init__(self, result_list):
        self.result_list = result_list
        self.result_list = []

    def insert_first(self, first):
        self.result_list.append(first)

    def insert_last(self, last):
        self.result_list.append(last)

    def insert_salary(self, salary):
        self.result_list.append(salary)
