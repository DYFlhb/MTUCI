class Employee:
    def __init__(self, name, id):
        self.name = name
        self.id = id
    
    def get_info(self):
        return f"Имя: {self.name}, ID: {self.id}"
    
    def __repr__(self):
        return f"{self.name, self.id}"

class Manager(Employee):
    def __init__(self, name, id, department):
        super().__init__(name, id)
        self.department = department
    
    def manage_project(self):
        return f"Сотрудник: {self.name} Управляет отделом: {self.department}\n"
    
    def __repr__(self):
        return f"{self.name, self.id, self.department}"

class Techican(Employee):
    def __init__(self, name, id, specialization):
        super().__init__(name, id)
        self.spec = specialization
    
    def perfom_maintenance(self):
        return f"Сотрудник: {self.name} Выполнил т.о. по: {self.spec}\n"
    
    def __repr__(self):
        return f"{self.name, self.id, self.spec}"

class TechManager(Manager, Techican):
    def __init__(self, name, id, department, specialization):
        Employee.__init__(self, name, id)
        self.department = department
        self.spec = specialization
        self.employees = []
    
    def add_employee(self, employee):
        self.employees.append(employee)
        return f'Сотрудник был привязан к {self.name}\n'
    
    def get_team_info(self):
        return f"В команде {self.name} следующие сотрудники: {self.employees}\n"
    

e = Employee("Bob", 12345)
m = Manager("Cowlasky", 5535, "Lowcost")
t = Techican("Walter White", 876545, "Chemistry")
tm = TechManager("JohnP", 777, "Technic", "HR")

print(e.get_info())
print(m.manage_project())
print(t.perfom_maintenance())
print(tm.add_employee(m))
print(tm.add_employee(e))
print(tm.get_team_info())